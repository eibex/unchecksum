# unchecksum

Quick tool to generate and check hashes of all files in a given directory recursively.

If a file (checked by filename) was never seen before, it will generate a quick checksum. If the file was already encountered (same location and filename) the checksum will be checked against the saved one. You could potentially save both checksums by renaming the directory containing the checksums under `files`.


## FAQ
Q: Why docker?

A: I made this to check files being copied on Unraid ¯\\_(ツ)_/¯
