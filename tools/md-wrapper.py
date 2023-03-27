#!/usr/bin/python3

"""
md-wrapper

Convert markdown source to HTML using templates.

-r root-dir
   Specifies the root directory of the destination doc tree.
   The {{root}} variable in templates is substituted with the
   relative path to the root directory from the destination doc.

-t template-file
   Specifies the template file to use.

Copyright © 2023 Cary Coutant

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import sys
import re
import getopt
import markdown
import html

def usage():
    sys.stderr.write("usage: md-wrapper.py [-r root-dir] [-t template-file] source.md dest.html\n")

root_dir = ""
template_file = ""

try:
    opts, args = getopt.getopt(sys.argv[1:], "hr:t:")
except getopt.GetoptError as err:
    sys.stderr.write(str(err) + "\n")
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-h":
        usage()
        sys.exit(0)
    if o == "-r":
        root_dir = a
    elif o == "-t":
        template_file = a

if len(args) < 2:
    usage()
    sys.exit(2)

source_file = args[0]
dest_file = args[1]

source_dir = os.path.dirname(source_file)
dest_dir = os.path.dirname(dest_file)
template_dir = os.path.dirname(template_file)

for f in [source_file, dest_dir, template_file]:
    if not os.path.exists(f):
        sys.stderr.write("error: %s does not exist\n" % f)
        sys.exit(1)

vars = {
    'root': os.path.relpath(root_dir, dest_dir),
    }

with open(source_file, 'r', encoding="utf-8") as f:
    while True:
        l = f.readline().strip()
        if not l:
            break
        m = re.match(r"([^:]+):\s*(.*)", l)
        if m:
            vars[m.group(1).lower()] = m.group(2)
    text = f.read()

with open(template_file, 'r', encoding="utf-8") as f:
    tmpl = f.read()

if "format" in vars and vars["format"] != "markdown":
    vars["content"] = '<pre class=\"proposal\">\n' + html.escape(text) + "</pre>\n"
else:
    vars["content"] = markdown.markdown(text, extensions = ['tables'])

# Substitution function for replacing template variables.
# Treats "{{@filename}}" as an include.
# Treats "{{varname}}" as a substitution from the vars dictionary.
def repl_meta(m):
    v = m.group(1)
    if v[0] == '@':
        include_file = os.path.join(template_dir, v[1:])
        with open(include_file, 'r', encoding="utf-8") as f:
            text = f.read()
        return text
    elif v in vars:
        return vars[v]
    return ""

# Run the substitution twice to catch any variable substitutions
# in included files.
html = re.sub(r"{{\s*(\S+)\s*}}", repl_meta, tmpl)
html = re.sub(r"{{\s*(\S+)\s*}}", repl_meta, html)

with open(dest_file, 'w', encoding="utf-8") as f:
    f.write(html)
