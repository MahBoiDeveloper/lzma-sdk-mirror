<!-- Generated from https://www.7-zip.org/sdk.html -->

<div>

# LZMA SDK (Software Development Kit)

The **LZMA SDK** provides the documentation, samples, header files, libraries, and tools you need to develop applications that use **LZMA** compression.

<table data-cellspacing="1" data-cellpadding="6" data-border="0">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th class="Title" style="text-align: center;" width="80">Link</th>
<th class="Title" style="text-align: center;" width="65">Size</th>
<th class="Title" style="text-align: center;" width="120">Date</th>
<th class="Title" style="text-align: center;" width="60">Version</th>
<th class="Title" style="text-align: center;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td class="Item" style="text-align: center;"><a href="https://github.com/ip7z/7zip/releases/download/26.06/lzma2606.7z">Download</a></td>
<td class="Item" style="text-align: center;">1.7 MB</td>
<td class="Item" style="text-align: center;">2026-11-06</td>
<td class="Item" style="text-align: center;">26.06</td>
<td class="Item">LZMA SDK<br />
C, C++, C#, Java<br />
x86/x64/arm64 binaries for Windows</td>
</tr>
<tr class="even">
<td class="Item" style="text-align: center;"><a href="https://www.7-zip.org/a/lzma-specification.7z">Download</a></td>
<td class="Item" style="text-align: center;">12 KB</td>
<td class="Item" style="text-align: center;">2015-06-14</td>
<td class="Item" style="text-align: center;"></td>
<td class="Item">LZMA Specification</td>
</tr>
</tbody>
</table>

**What's new:**

- **26.06:** Improved support for split files created by "split" utility in Linux..
- **26.05:** minor changes.
- **26.04:** Some bugs and vulnerabilities were fixed.
- **26.03:** Some bugs and vulnerabilities were fixed.
- **26.02:** Some bugs and vulnerabilities were fixed.
- **26.01:** Some minor fixes.
- **26.00:** Some minor fixes.
- **25.01:** The code for handling symbolic links has been changed to provide greater security when extracting files from archives.
- **25.00:** 7-Zip for Windows can now use more than 64 CPU threads for compression.
- **24.09:** The default dictionary size values for LZMA/LZMA2 compression methods were increased.
- **24.05:** New filter for RISC-V executables.
- **23.01:** New filter for ARM64 executables. BCJ2 filter was improved for better compression ratio. Some bugs were fixed.
- **21.07:** Some minor changes and fixes.
- **21.06:** The bug in LZMA encoding function was fixed.
- **21.03 beta:** LZMA dicrionary up to 4 GB. Speed optimizations.
- **21.02 alpha:** macOS and Linux support. Speed optimizations.
- **19.00:** Encryption strength for 7z archives was increased.
- **18.06:** Some speed optimiztions in LZMA/LZMA2 code.
- **18.05:** Some speed optimiztions in LZMA/LZMA2 code.
- **18.01:** Some changes in LZMA2/xz multithreading code for compressing. Some bugs were fixed.
- **9.35:** AES code and SFXs modules were included to SDK.
- **9.20:** New small SFX module for installers.
- **9.11:** PPMd support.
- **9.04:** LZMA2 and XZ support.
- **4.62:** LZMA SDK is placed in the public domain.

**LZMA / LZMA2** are default and general compression methods of [**7z format**](https://www.7-zip.org/7z.html) in the **7-Zip** program provides a high compression ratio and fast decompression, so it is very suitable for embedded applications. For example, it can be used for ROM (firmware) compressing.

**LZMA SDK** includes:

- **C++** source code of **LZMA** Encoder and Decoder
- **C++** source code for **.7z** compression and decompression (reduced version)
- **ANSI-C** compatible source code for **LZMA / LZMA2 / XZ** compression and decompression
- **ANSI-C** compatible source code for **7z** decompression with example
- **C#** source code for **LZMA** compression and decompression
- **Java** source code for **LZMA** compression and decompression
- **lzma.exe** for .lzma compression and decompression
- **7zr.exe** to work with 7z archives (reduced version of 7z.exe from 7-Zip)
- **SFX modules** to create self-extracting packages and installers

**ANSI-C** and **C++** source code in LZMA SDK is subset of source code of 7-Zip.

**LZMA** features:

- Compression speed: 2-8 MB/s on 4 GHz CPU using two cpu threads.
- Decompression speed on single cpu thread:
  - 30-100 MB/s on modern 4 GHz CPU (Intel, AMD, ARM).
  - 5-15 MB/s on simple 1 GHz RISC CPU (ARM, MIPS, PowerPC).
- Small memory requirements for decompression: 8-32 KB + DictionarySize
- Small code size for decompression: 2-8 KB (depending on speed optimizations)

The **LZMA** decoder uses only CPU integer instructions and can be implemented for any modern 32-bit CPU.

## License

**LZMA SDK** is placed in the **public domain.**

Anyone is free to copy, modify, publish, use, compile, sell, or distribute the original LZMA SDK code, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

Note: The abbreviation LZMA originally stood for Lempel - Ziv - Markov chain - Arithmetic coding. Preliminary versions of LZMA used arithmetic coding. But in the final version of LZMA, arithmetic coding was replaced by range coding.

## LZMA Links

- [LZMA at Wikipedia](https://en.wikipedia.org/wiki/LZMA)
- [LZMA Benchmark results for different CPUs](https://www.7-cpu.com/)
- [XZ Utils / LZMA utils](https://tukaani.org/xz/)
- [Port of LZMA SDK for JAVA from independent developer](https://sourceforge.net/projects/p7zip/)
- [Port of LZMA SDK to Pascal (Delphi, Kylix and Freepascal)](https://www.birtles.org.uk/programming/)
- [PyLZMA: Python bindings for LZMA](https://www.joachim-bauch.de/projects/python/pylzma/)
- [LZMA Streams in Java](https://contrapunctus.net/league/haques/lzmajio/)
- [Zip-Ada : LZMA in Ada](https://unzip-ada.sourceforge.io/)

------------------------------------------------------------------------

<span class="small">Copyright (C) 2026 Igor Pavlov.</span>

</div>
