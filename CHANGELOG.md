# v0.3.1 (2021-06-25)

- internal api changes

# v0.3.0 (2021-06-24)

- generate download links with tokens

# v0.2.1 (2021-06-23)

- fix staging on CIFS (no : in filenames)
- raise staging threshold

# v0.2.0 (2021-06-22)

- staged uploads for large files (copy to directory shared with Hinkskalle server instead of http upload)
- fix tar for relative paths, strip directories when pulling

# v0.1.1 (2021-06-22)

- fix initial login (no config yet)

# v0.1.0 (2021-06-22)

initial release

- log in to hinkskalle
- push: upload single files and directories (as tar.gz)
- pull: download oras compatible images
