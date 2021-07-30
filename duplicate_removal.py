import sys
import os
import hashlib

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def check_for_duplicates(paths, hash=hashlib.sha1):
    initial_files = len(os.listdir(paths[0]))
    hashes = {}
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                print('Processing : ', filename)
                full_path = os.path.join(dirpath, filename)
                hashobj = hash()
                for chunk in chunk_reader(open(full_path, 'rb')):
                    hashobj.update(chunk)
                file_id = (hashobj.digest(), os.path.getsize(full_path))
                duplicate = hashes.get(file_id, None)
                if duplicate:
                    print ("Duplicate found: %s and %s" % (full_path, duplicate))
                    os.remove(full_path)
                else:
                    hashes[file_id] = full_path
    remaining_files = len(os.listdir(paths[0]))
    duplicate_file = int(initial_files) - int(remaining_files)
    print('Total Unique Files : ', remaining_files)
    print('Duplicate Files : ', duplicate_file)
    return remaining_files

if __name__ == "__main__":
    input_folder = 'input_folder_path'

    check_for_duplicates([input_folder])
    

# if sys.argv[1:]:
#     check_for_duplicates(sys.argv[1:])
# else:
#     print "Please pass the paths to check as parameters to the script"
