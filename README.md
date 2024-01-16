# unchecksum

Quick tool to generate and check hashes of all files in a given directory recursively.

If a file (checked by filename) was never seen before, it will generate a quick checksum. If the file was already encountered (same location and filename) the checksum will be checked against the saved one. You could potentially save both checksums by renaming the directory containing the checksums under `files`.

## How to use
```
python3 ./unchecksum.py "/path/of/directory/to/check"
```

Additional parameters:
```
-hs, --hash                 specify an hash between 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2', 'md5' (default is blake2 for speed)
-a, --action                specify what action to take in case of different hashes ('warn' or 'overwrite') (default 'warn')
-c, --compare               compare the given directory against specified one with the same directory and file structure/names against each other (specified after this argument)
-cc, --calculatecompare     calculate hashes (with threading) and compare the given directory against specified one with the same directory and file structure/names against each other (specified after this argument)
-s, --skip                  skip existing known files and calculate hashes only for new files
```
Note: if using the `--compare` argument the program will *not* calculate hashes, but simply compare two existing sets of hashes against each other.

### Example 1 - Checking the files in-place (same path)
First run:
```
python3 ./unchecksum.py "/disk1"
```

The program will generate hashes of all your files.

Assuming you have not moved the files around, you can re-run the same command to check for silent corruption.

### Example 2 - Checking the files after a copy (different path)
If you have already calculated the hashes for both directories:
```
python3 ./unchecksum.py "files/disk1" -c "files/disk2"
```

If you need to calculate hashes for both directories:
```
python3 ./unchecksum.py "/disk1" -cc "/disk2"
```

## FAQ
Q: Why docker?

A: I made this to check files being copied on Unraid and did not want to install Python outside of a container ¯\\_(ツ)_/¯ (if you actually want to use it in a docker you will have to add the `-t` extra-parameter to keep the docker alive or it will exit after starting)
