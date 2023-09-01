#!/bin/bash


FNAME=$(echo $RANDOM | sha256sum | head -c 16; echo).php
VALID_EXT="pdf"
PAYLOAD='payloads/payload_example1.php'
#PAYLOAD='payloads/payload_example2.php'
OUTPUT_FNAME='b4d.zip'

# LAUNCH B4Dzip
python3 main.py \
    --file $FNAME \
    --ext $VALID_EXT \
    --payload $PAYLOAD \
    --output $OUTPUT_FNAME

if [ -e $OUTPUT_FNAME ]; then
    printf "\n\n*********** SUMMARY ***********\n\n"
    unzip -l $OUTPUT_FNAME
    printf "\n\n"
    hexdump -C  $OUTPUT_FNAME
else
    echo "[ERROR] The zip file has not been generated due to errors."
fi