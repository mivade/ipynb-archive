ipynb-archive
=============

A simple tool for archiving IPython notebook files into non-mutable
formats. In other words, this tool creates static HTML copies of all
IPython notebook files in a given directory for archival purposes so
as to avoid accidental changes to the original content.

## Usage ##

```
usage: nbarchive.py [-h] [--overwrite] [--index-file [INDEX_FILE]]
                    [--index-title INDEX_TITLE]

optional arguments:
  -h, --help            show this help message and exit
  --overwrite           Overwrite HTML files which already exist.
  --index-file [INDEX_FILE]
                        Create an index file. If no filename is given, the
                        index file will be named index.html.
  --index-title INDEX_TITLE
                        Index file title.
```

## Requirements ##

* Python (tested on 2.7.3, but should work in Python 3)
* IPython >= 1.0.0 (tested on 1.1.0)
