import os
import hashlib
import argparse

parser = argparse.ArgumentParser(
    description="Checksum creation and comparison. More info at: https://github.com/eibex/unchecksum"
)
parser.add_argument("path", type=str, help="Directory to check")
parser.add_argument(
    "-hs",
    "--hash",
    type=str,
    help="Which hash to use (default 'blake2')",
)
parser.add_argument(
    "-a",
    "--action",
    type=str,
    help="What action to take in case of different hashes ('warn' or 'overwrite') (default 'warn')",
)
parser.add_argument(
    "-c",
    "--compare",
    type=str,
    help="Compare the given directory against specified one with the same directory and file structure/names against each other (specified after this argument)",
)
args = parser.parse_args()
hash_algorithms = {
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
    "blake2": hashlib.blake2b,
    "md5": hashlib.md5,
}

different_hashes = {}

def calculate_hash(filepath: str, hash_algorithm: str):
    calculated_hash = hash_algorithms[hash_algorithm]()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            calculated_hash.update(byte_block)
        return calculated_hash.hexdigest()


def hash_exists(filepath, algorithm):
    files = f"{os.path.dirname(os.path.realpath(__file__))}/files"
    return os.path.exists(f"{files}/{filepath.replace(':', '')}.{algorithm}.txt")


def check_hash(file_hash, filepath, algorithm):
    files = f"{os.path.dirname(os.path.realpath(__file__))}/files"
    with open(f"{files}/{filepath.replace(':', '')}.{algorithm}.txt", "r") as f:
        old_hash = f.readlines()[0]

    return old_hash == file_hash, old_hash


def save_hash(file_hash, filepath, filename, algorithm):
    files = f"{os.path.dirname(os.path.realpath(__file__))}/files"
    filepath_directory = filepath.replace(':', '').removesuffix(filename)
    os.makedirs(f"{files}/{filepath_directory}", exist_ok=True)
    with open(f"{files}/{filepath.replace(':', '')}.{algorithm}.txt", "w") as f:
        f.write(file_hash)


def finder(path: str, hash_algorithm: str, action: str):
    for root, directories, files in os.walk(path):
        for file in files:
            filepath = f"{root}/{file}"
            file_hash = calculate_hash(filepath, hash_algorithm=hash_algorithm)
            if not hash_exists(filepath, hash_algorithm):
                print(f"Hash for {file} doesn't exist, saving.")
                save_hash(file_hash, filepath, file, hash_algorithm)

            check = check_hash(file_hash, filepath, hash_algorithm)
            if not check[0]:
                different_hashes[filepath] = (check[1], file_hash)

            if action == "overwrite":
                save_hash(file_hash, filepath, file, hash_algorithm)


def compare_files(filename, hash1, hash2):
    if hash1 != hash2:
        return f"[Mismatch] {filename}\nHash 1: {hash1}\nHash 2: {hash2}\n"


path = args.path
hash_algorithm = args.hash
action = args.action
compare = args.compare

if not os.path.exists(path):
    raise NameError("Specified path does not exist")

if not compare:
    if args.action is None:
        action = "warn"

    if args.hash is None:
        hash_algorithm = "blake2"

    if hash_algorithm not in hash_algorithms:
        raise Exception("Unsupported hash algorithm")

    finder(path, hash_algorithm, action)

    if not different_hashes:
        print("No hash changes found.")

    else:
        for filepath in different_hashes:
            print(f"Filepath: {filepath}\nOld hash: {different_hashes[filepath][0]}\nNew hash: {different_hashes[filepath][1]}")
else:
    mismatches = False
    if not os.path.exists(compare):
        raise NameError("Specified comparison path does not exist")
    for root, directories, files in os.walk(path):
        for file in files:
            filepath = f"{root}/{file}"
            print(filepath)
            print(filepath.replace(path, compare))
            with open(filepath, "r") as f:
                hash1 = f.read()
            with open(filepath.replace(path, compare), "r") as f:
                hash2 = f.read()
            result = compare_files(f"{root}/{file}", hash1, hash2)
            if result:
                print(result)
                mismatches = True
    if not mismatches:
        print("No hash differences found.")
