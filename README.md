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

I Highly recommend to see the `runner.sh` file for getting information about usage examples.
