#!/usr/bin/python3

import os
import sys
import re
import getopt
import markdown
import html

is_proposal = False
root_dir = ""
template_file = ""

try:
    opts, args = getopt.getopt(sys.argv[1:], "pr:t:")
except getopt.GetoptError as err:
    sys.stderr.write(err + "\n")
    sys.exit(2)
for o, a in opts:
    if o == "-p":
        is_proposal = True
    if o == "-r":
        root_dir = a
    elif o == "-t":
        template_file = a

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

if is_proposal and not "markdown" in vars:
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
