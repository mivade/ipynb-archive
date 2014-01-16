#!/usr/bin/env python
"""
archive.py

A simple script for archiving ipynb files into non-mutable HTML
format.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function
import os, os.path, glob, shutil, argparse

## Configuration ##

# Files to ignore for archival.
ignore = ['Template.ipynb']

# nbconvert commands that can be used.
# TODO: Add latex and other options.
nb_basic = "ipython nbconvert --to "
nb_html_full = nb_basic + "html --template full"
nb_html_basic = nb_basic + "html --template basic"

# Directory to move archived files to. Set to '.' to keep in the same
# directory. For now you'll have to place the ipython.css file in
# there manually.
archive_dir = "archives"

## HTML strings ##

header_open = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>[2013-11-28]</title>"""

stylesheet = '\n<link rel="stylesheet" href="ipython.css" type="text/css">'

mathjax = r"""
<script src="https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS_HTML" type="text/javascript"></script>
<script type="text/javascript">
init_mathjax = function() {
    if (window.MathJax) {
        // MathJax loaded
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
            },
            displayAlign: 'left', // Change this to 'center' to center equations.
            "HTML-CSS": {
                styles: {'.MathJax_Display': {"margin": 0}}
            }
        });
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    }
}
init_mathjax();
</script>"""

header_close = """
</head>
<body>"""

footer = """
</body>
</html>"""

## Function definitions ##

def nbconvert_cmd(nbcmd, fname, echo=True):
    """Runs the nbconvert command nbcmd on file fname."""
    cmd = nbcmd + " " + fname
    if echo:
        print(cmd)
    os.system(cmd)
    
# TODO: Make an index file with a frame listing all the logs and
#       another frame to display them.
def archive():
    """Perform the archival of ipynb files."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite HTML files which already exist.")
    args = parser.parse_args()

    if args.overwrite:
        overwrite = True
    else:
        overwrite = False
    
    ipy_files = glob.glob("*.ipynb")
    prefixes = [pre[:-len(".ipynb")] for pre in ipy_files]

    cmd = nb_html_basic
    for prefix in prefixes:
        fname = prefix + ".ipynb"
        if fname in ignore:
            continue
        if not os.path.exists(prefix + ".html") or overwrite:
            nbconvert_cmd(cmd, fname)
            if cmd == nb_html_basic:
                with open(prefix + ".html", "r+") as html_file:
                    html = html_file.read()
                    html_file.seek(0)
                    title = "<h1>" + prefix + "</h1>"
                    html_file.writelines([header_open, stylesheet, mathjax,
                                          header_close, title, html, footer])
                    
    if archive_dir != '.':
        for filename in glob.glob("*.html"):
            shutil.copy(filename, archive_dir)

if __name__ == "__main__":
    archive()
