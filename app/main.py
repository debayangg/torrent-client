import json
import sys
import hashlib
import requests
from .bencode import bencode_encode, decode_bencode

def main():
    command = sys.argv[1]

    # You can use print statements as follows for debugging, they'll be visible when running tests.

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # Let's convert them to strings for printing to the console.
        def bytes_to_str(data):
            if isinstance(data, bytes):
                return_value= data.decode()
                if return_value.isnumeric() or return_value[1:].isnumeric() :
                    return int(return_value)
                else:    
                    return return_value

            raise TypeError(f"Type not serializable: {type(data)}")

        # Uncomment this block to pass the first stage
        print(decode_bencode(bencoded_value))
        #print(json.dumps(decode_bencode(bencoded_value), default=bytes_to_str))
    elif command == "info":
        with open(sys.argv[2], 'rb') as file:
            torrent_data = file.read()
            #print(json.dumps(decode_bencode(torrent_data)),default=bytes_to_str)
            ben_dict=decode_bencode(torrent_data)
            bencoded_info=bencode_encode(ben_dict['info'])
            # Assuming `bencoded_info` is your bencoded `info` dictionary
            info_hash = hashlib.sha1(bencoded_info).hexdigest()
            print(f"Info Hash: {info_hash}")
            piece_length=ben_dict['info']['piece length']
            pieces_string = ben_dict['info']['pieces']
            hashes = [pieces_string[i:i+20] for i in range(0, len(pieces_string), 20)]
            hex_hashes = [hash.hex() for hash in hashes]
            print(hex_hashes)
    
    elif command == "peers":
        resp=requests.get()


    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
