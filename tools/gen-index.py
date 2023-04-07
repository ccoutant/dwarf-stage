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
    title = "Open " + title

for f in [source_dir, dest_dir, template_file]:
    if f and not os.path.exists(f):
        sys.stderr.write("error: %s does not exist\n" % f)
        sys.exit(1)

issue_files = sorted(glob.glob(source_dir + "/*.md"))

issue_list = []
for source_file in issue_files:
    row = { }
    row["href"] = os.path.join(root_path, "issues", os.path.basename(source_file.replace(".md", ".html")))
    with open(source_file, 'r', encoding="utf-8") as f:
        while True:
            l = f.readline().strip()
            if not l:
                break
            m = re.match(r"([^:]+):\s*(.*)", l)
            if m:
                row[m.group(1).lower()] = m.group(2)
    status = row.get("status", "open").lower()
    status_code = "o"
    if status.startswith(("acc", "app", "ans", "lang")):
        status_code = "ca"
    elif status.startswith(("closed", "dup", "rej", "repl")):
        status_code = "cr"
    elif status.startswith("withdrawn"):
        status_code = "cw"
    row["statuscode"] = status_code
    if version and version != row.get("version", ""):
        continue
    if issue_filter and issue_filter != status_code[0]:
        continue
    issue_list.append(row)

with open(template_file, 'r', encoding="utf-8") as f:
    tmpl = f.read()

# Generate HTML code for the table of issues.
def gen_issue_table(issue_list):
    html_code = '<table id="issueindex" class="issueindex">\n<thead>\n'
    html_code += '  <tr>\n'
    for f in issue_column_titles:
        html_code += '    <th>' + f + '</th>\n'
    html_code += '  </tr>\n'
    html_code += '</thead>\n<tbody>\n'
    for row in issue_list:
        html_code += '  <tr data-id="%s" data-status="%s">\n' % (row["propid"], row["statuscode"])
        html_code += '    <td><a href="%s">%s</a></td>\n' % (row["href"], row["propid"])
        for f in issue_column_fields[1:]:
            html_code += '    <td>' + html.escape(row[f]) + '</td>\n'
        html_code += '  </tr>\n'
    html_code += '</tbody>\n</table>\n'
    return html_code

class_self = "self:" + os.path.basename(dest_file.rsplit('.', 1)[0])

vars = {
    'root': root_path,
    'title': title,
    'content': gen_issue_table(issue_list),
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
