#!/usr/bin/python3

"""
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
import glob
import html

def usage():
    sys.stderr.write("usage: gen-index.py [-r rootdir] [-v dwarf-version] [-t template] source-directory index-file\n")

issue_column_titles = [
    "Issue #", "Title", "Author", "Champion", "Type", "Status"
]
issue_column_fields = [
    "propid", "title", "author", "champion", "type", "status"
]

root_dir = ""
version = ""
template_file = ""
issue_filter = ""

try:
    opts, args = getopt.getopt(sys.argv[1:], "hcor:v:t:")
except getopt.GetoptError as err:
    sys.stderr.write(str(err) + "\n")
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-h":
        usage()
        sys.exit(0)
    elif o == "-c":
        issue_filter = "c"
    elif o == "-o":
        issue_filter = "o"
    elif o == "-r":
        root_dir = a
    elif o == "-v":
        version = a
    elif o == "-t":
        template_file = a

if len(args) < 2:
    usage()
    sys.exit(2)

source_dir = args[0]
dest_file = args[1]

dest_dir = os.path.dirname(dest_file)
template_dir = os.path.dirname(template_file)
root_path = os.path.relpath(root_dir, dest_dir)

title = "DWARF Issues"
if version:
    title = "Issues for DWARF Version " + version
if issue_filter == "c":
    title = "Closed " + title
elif issue_filter == "o":
    title = "Current " + title

for f in [source_dir, dest_dir, template_file]:
    if f and not os.path.exists(f):
        sys.stderr.write("error: %s does not exist\n" % f)
        sys.exit(1)

issue_files = sorted(glob.glob(source_dir + "/*.md"))

issue_table = "<table class=\"issueindex\">\n<thead>\n"
issue_table += "  <tr>\n" + "".join(["    <th>%s</th>\n" % s for s in issue_column_titles]) + "  </tr>\n"
issue_table += "</thead>\n<tbody>\n"
for source_file in issue_files:
    per_file_meta = { }
    with open(source_file, 'r', encoding="utf-8") as f:
        while True:
            l = f.readline().strip()
            if not l:
                break
            m = re.match(r"([^:]+):\s*(.*)", l)
            if m:
                per_file_meta[m.group(1).lower()] = m.group(2)
    if version and "version" in per_file_meta and version != per_file_meta["version"]:
        continue
    if issue_filter:
        is_closed = False
        if "status" in per_file_meta:
            is_closed = re.match(r"accepted|approved|closed|duplicate|deferred|rejected|withdrawn|lang", per_file_meta["status"], re.I)
        if issue_filter == "c" and not is_closed:
            continue
        if issue_filter == "o" and is_closed:
            continue
    href = os.path.join(root_path, "issues", os.path.basename(source_file.replace(".md", ".html")))
    issue_table += "  <tr>\n"
    issue_table += "    <td><a href=\"%s\">%s</a></td>\n" % (href, per_file_meta["propid"])
    issue_table += "".join("    <td>%s</td>\n" % html.escape(per_file_meta[s]) for s in issue_column_fields[1:])
    issue_table += "  </tr>\n"
issue_table += "</tbody>\n</table>\n"

with open(template_file, 'r', encoding="utf-8") as f:
    tmpl = f.read()

class_self = "self:" + os.path.basename(dest_file.rsplit('.', 1)[0])

vars = {
    'root': root_path,
    'title': title,
    'content': issue_table,
    class_self: "self"
    }

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
