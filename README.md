# unchecksum

Quick tool to generate and check hashes of all files in a given directory recursively.

If a file (checked by filename) was never seen before, it will generate a quick checksum. If the file was already encountered (same location and filename) the checksum will be checked against the saved one. You could potentially save both checksums by renaming the directory containing the checksums under `files`.

## How to use
```
python3 ./unchecksum.py "/path/of/directory/to/check"
```

Additional parameters:
```
-hs, --hash      specify an hash between 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2', 'md5' (default is blake2 for speed)
-a, --action     specify what action to take in case of different hashes ('warn' or 'overwrite') (default 'warn')
```


## FAQ
Q: Why docker?

A: I made this to check files being copied on Unraid ¯\\_(ツ)_/¯ (if you actually want to use it in a docker you will have to add the `-t` extra-parameter to keep the docker alive or it will exit after starting)
