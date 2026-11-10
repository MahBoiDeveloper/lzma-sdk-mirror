import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from lxml import html


SDK_PAGE = "https://www.7-zip.org/sdk.html"
README = Path("README.md")
LOCK = Path(".github/lzma-sdk.lock.json")
VERSION = re.compile(r"[0-9]+\.[0-9]+(?:\.[0-9]+)?")
ARCHIVE_URL = re.compile(
    r"https://(?:(?:www\.)?7-zip\.org/a/|"
    r"github\.com/ip7z/7zip/releases/download/(?P<tag>[0-9.]+)/)"
    r"lzma(?P<digits>[0-9]+)\.7z"
)
BOT_NAME = "github-actions[bot]"
BOT_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"


def download(url, destination):
    subprocess.run(
        [
            "curl", "--fail", "--silent", "--show-error", "--location",
            "--proto", "=https", "--proto-redir", "=https", "--max-redirs", "5",
            "--retry", "3", "--connect-timeout", "15", "--max-time", "90",
            "--max-filesize", "52428800", "--output", destination, url,
        ],
        check=True,
    )


def parse_page(page_bytes):
    document = html.fromstring(page_bytes)
    document.make_links_absolute(SDK_PAGE, resolve_base_href=False)
    downloads = {}
    for link in document.xpath("//a[@href]"):
        match = ARCHIVE_URL.fullmatch(link.get("href"))
        if not match:
            continue
        row = next(link.iterancestors("tr"), None)
        if row is None:
            continue
        cells = [cell.text_content().strip() for cell in row.xpath("./td | ./th")]
        versions = [cell for cell in cells if VERSION.fullmatch(cell)]
        if len(versions) != 1:
            raise ValueError("Expected one SDK version in the download row")
        version = versions[0]
        if match["digits"] != version.replace(".", "") or match["tag"] not in (None, version):
            raise ValueError(f"SDK version and archive URL do not match: {version}")
        downloads.setdefault(version, link)

    if not downloads:
        raise ValueError("No LZMA SDK archive found on the official download page")
    version = max(downloads, key=lambda value: tuple(map(int, value.split("."))))
    link = downloads[version]
    archive_url = link.get("href")

    headings = document.xpath("//h1[starts-with(normalize-space(.), 'LZMA SDK')]")
    if len(headings) != 1:
        raise ValueError("Could not identify the LZMA SDK heading")
    link_ancestors = set(link.iterancestors())
    content = next((node for node in headings[0].iterancestors() if node in link_ancestors), None)
    if content is None or content.tag in {"body", "html"}:
        raise ValueError("Could not identify the LZMA SDK content area")
    for element in content.xpath(".//script | .//style | .//nav | .//aside"):
        element.drop_tree()
    content.tag = "div"
    content.attrib.clear()
    markdown = subprocess.run(
        ["pandoc", "--sandbox", "--from=html", "--to=gfm", "--wrap=none"],
        input=html.tostring(content, encoding="utf-8"),
        stdout=subprocess.PIPE,
        check=True,
    ).stdout.decode("utf-8").rstrip()
    readme = f"<!-- Generated from {SDK_PAGE} -->\n\n{markdown}\n"
    return version, archive_url, readme


def validate_root(name):
    if (
        not name
        or name.startswith(".")
        or "/" in name
        or "\\" in name
        or name.casefold() == README.name.casefold()
    ):
        raise ValueError(f"Reserved or invalid SDK root entry: {name!r}")


def mirror(previous):
    with TemporaryDirectory(prefix="lzma-sdk-") as work:
        work = Path(work)
        page = work / "sdk.html"
        download(SDK_PAGE, page)
        version, archive_url, readme = parse_page(page.read_bytes())
        archive = work / "sdk.7z"
        download(archive_url, archive)
        with archive.open("rb") as stream:
            if stream.read(6) != bytes.fromhex("37 7a bc af 27 1c"):
                raise ValueError("The downloaded file is not a 7z archive")
            stream.seek(0)
            sha256 = hashlib.file_digest(stream, "sha256").hexdigest()

        extracted = work / "extracted"
        extracted.mkdir()
        subprocess.run(
            ["bsdtar", "-xf", archive, "-C", extracted, "--no-same-owner", "--no-same-permissions"],
            check=True,
        )
        if not (extracted / "C/LzmaDec.c").is_file():
            raise ValueError("The archive does not contain the expected SDK sources")
        for path in extracted.rglob("*"):
            if (
                path.is_symlink()
                or not (path.is_file() or path.is_dir())
                or any(part.startswith(".") or "\\" in part for part in path.relative_to(extracted).parts)
            ):
                raise ValueError(f"Unsupported archive entry: {path.relative_to(extracted)!s}")

        new_roots = {entry.name for entry in extracted.iterdir()}
        old_roots = set(previous["roots"]) if previous else set()
        for name in sorted(new_roots | old_roots):
            validate_root(name)
        for name in sorted(new_roots - old_roots):
            if os.path.lexists(name):
                raise FileExistsError(f"SDK archive conflicts with existing repository entry: {name}")

        replaced = {name for name in old_roots if os.path.lexists(name)}
        for name in sorted(replaced):
            path = Path(name)
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
        for name in sorted(new_roots):
            shutil.move(extracted / name, name)

        state = {
            "version": version,
            "sha256": sha256,
            "archive_url": archive_url,
            "roots": sorted(new_roots),
        }
        README.write_text(readme, encoding="utf-8")
        LOCK.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        subprocess.run(
            ["git", "--literal-pathspecs", "add", "-A", "-f", "--", README, LOCK, *sorted(new_roots | replaced)],
            check=True,
        )
        return state


def publish_release(state):
    version = state["version"]
    sha256 = state["sha256"]
    tag = f"v{version}-{sha256[:12]}"
    endpoint = f'{os.environ["GITHUB_API_URL"]}/repos/{os.environ["GITHUB_REPOSITORY"]}/releases'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f'Bearer {os.environ["GH_TOKEN"]}',
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        with urlopen(Request(f"{endpoint}/tags/{tag}", headers=headers), timeout=30):
            return
    except HTTPError as error:
        if error.code != 404:
            raise

    commit = subprocess.check_output(
        ["git", "log", "-1", "--format=%H", "--", LOCK], text=True,
    ).strip()
    if not commit:
        raise RuntimeError("Could not find the SDK import commit")
    payload = {
        "tag_name": tag,
        "target_commitish": commit,
        "name": f"LZMA SDK {version}",
        "body": (
            f'[Official SDK page]({SDK_PAGE}) · [Original 7z archive]({state["archive_url"]})\n\n'
            f"SHA-256: `{sha256}`"
        ),
        "make_latest": "true",
    }
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
    )
    with urlopen(request, timeout=30) as response:
        print(f'Published {json.load(response)["html_url"]}')


def main():
    for path in (README, LOCK):
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f"Expected a regular file at {path}")
    previous = json.loads(LOCK.read_text(encoding="utf-8")) if LOCK.exists() else None
    if previous:
        publish_release(previous)

    state = mirror(previous)
    changed = subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode
    if changed == 0:
        print("The SDK and README are up to date")
        return
    if changed != 1:
        raise RuntimeError("Could not inspect staged changes")

    sdk_changed = previous is None or any(state[key] != previous[key] for key in ("version", "sha256"))
    message = f'Sync LZMA SDK {state["version"]}' if sdk_changed else "Refresh the LZMA SDK mirror"
    subprocess.run(
        ["git", "-c", f"user.name={BOT_NAME}", "-c", f"user.email={BOT_EMAIL}", "commit", "-m", message],
        check=True,
    )
    subprocess.run(["git", "push", "origin", f'HEAD:refs/heads/{os.environ["TARGET_BRANCH"]}'], check=True)
    if sdk_changed:
        publish_release(state)


if __name__ == "__main__":
    main()
