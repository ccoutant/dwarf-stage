#!/usr/bin/python3

import os
import sys
import re
import getopt
import glob
import html

root_dir = ""
version = ""
template_file = ""

issue_column_titles = [
    "Issue #", "Title", "Author", "Champion", "Type", "Status"
]
issue_column_fields = [
    "propid", "title", "author", "champion", "type", "status"
]

try:
    opts, args = getopt.getopt(sys.argv[1:], "r:v:t:")
except getopt.GetoptError as err:
    sys.stderr.write(err + "\n")
    sys.exit(2)
for o, a in opts:
    if o == "-r":
        root_dir = a
    elif o == "-v":
        version = a
    elif o == "-t":
        template_file = a

title = "DWARF Issues"
if version:
    title = "Issues for DWARF Version " + version

source_dir = args[0]
dest_file = args[1]

dest_dir = os.path.dirname(dest_file)
template_dir = os.path.dirname(template_file)
root_path = os.path.relpath(root_dir, dest_dir)

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
    if not version or ("version" in per_file_meta and version == per_file_meta["version"]):
        href = os.path.join(root_path, "issues", os.path.basename(source_file.replace(".md", ".html")))
        issue_table += "  <tr>\n"
        issue_table += "    <td><a href=\"%s\">%s</a></td>\n" % (href, per_file_meta["propid"])
        issue_table += "".join("    <td>%s</td>\n" % html.escape(per_file_meta[s]) for s in issue_column_fields[1:])
        issue_table += "  </tr>\n"
issue_table += "</tbody>\n</table>\n"

with open(template_file, 'r', encoding="utf-8") as f:
    tmpl = f.read()

vars = {
    'root': root_path,
    'title': title,
    'content': issue_table
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
