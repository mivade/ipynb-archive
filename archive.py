#!/usr/bin/env python
"""
archive.py

A simple script for archiving ipynb files into non-mutable HTML
format.

TODO: Statistics on files added compared to already existing and
      overwritten
TODO: Message if nothing is done

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
import os, os.path, glob, shutil, argparse, re

# Configuration
# -------------

# Files to ignore for archival.
ignore = ['Template.ipynb']

# nbconvert commands that can be used.
nb_basic = "ipython nbconvert --to "
nb_html_full = nb_basic + "html --template full"
nb_html_basic = nb_basic + "html --template basic"

# Directory to move archived files to. Set to '.' to keep in the same
# directory. For now you'll have to place the ipython.css file in
# there manually.
archive_dir = "archives"

# HTML strings
# ------------

header_open = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">"""

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

index_template = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
"http://www.w3.org/TR/html4/frameset.dtd">
<HTML>
<HEAD>
<TITLE>$INDEX_TITLE</TITLE>
</HEAD>
<FRAMESET cols="10%, 80%">
<FRAME src="_index.html" name="index">
<FRAME src="$FIRST_FILE" name="content">
</FRAMESET>
</HTML>
"""

# Function definitions
# --------------------

def nbconvert_cmd(nbcmd, fname, echo=True):
    """Runs the nbconvert command nbcmd on file fname."""
    cmd = nbcmd + " " + fname
    if echo:
        print(cmd)
    os.system(cmd)

def archive():
    """Perform the archival of ipynb files."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite HTML files which already exist.")
    parser.add_argument("--index-file", default="_NONE_", nargs='?',
                        help="Create an index file. If no filename is given," + \
                        "the index file will be named index.html.")
    parser.add_argument("--index-title", default="Archived ipynb file list",
                        help="Index file title.")
    args = parser.parse_args()

    if args.overwrite:
        overwrite = True
    else:
        overwrite = False

    if args.index_file is None:
        write_index = True
        args.index_file = "index.html"
    elif args.index_file != "_NONE_":
        write_index = True
    else:
        write_index = False
    
    ipy_files = sorted(glob.glob("*.ipynb"))
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
                    html_title = "<title>" + prefix + "</title>"
                    title_line = "<h1>" + prefix + "</h1>"
                    html_file.writelines([header_open, html_title, stylesheet, mathjax,
                                          header_close, title_line, html, footer])
                    
    if archive_dir != '.':
        for filename in glob.glob("*.html"):
            shutil.copy(filename, archive_dir)

    if write_index:
        os.chdir(archive_dir)
        with open("_index.html", "w") as index_list, \
                 open(args.index_file, "w") as index_file:
            index_list.write("<p><b>File list</b></p>\n<p>")
            for prefix in prefixes:
                index_list.write('<a href=%s target="content">%s</a><br/>\n' % \
                                 (prefix + ".html", prefix))
            index_source = re.sub("\$INDEX_TITLE", args.index_title, index_template)
            index_source = re.sub("\$FIRST_FILE", prefixes[0] + ".html", index_source)
            index_file.write(index_source + "\n</p>")

if __name__ == "__main__":
    archive()
