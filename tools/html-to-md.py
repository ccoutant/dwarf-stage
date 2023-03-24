#! /usr/bin/python3

# html-to-md
# Rudimentary conversion of HTML to Markdown.
# -h
#    Strips the header and footer elements from the page.
#    Looks for the specific patterns used in the DWARF HTML code.
# -p
#    Tailors the conversion to DWARF issue pages, extracting
#    metadata from the start of the file, and using the
#    contents of the <pre> element as the markdown.
#    The metadata is placed at the top of the generated
#    markdown file.
# -v n
#    Specifies the target DWARF version number (for issue metadata).
#    Default: 6.

import sys
import re
import getopt
from html.parser import HTMLParser
from html.entities import name2codepoint

# These tags are treated as block tags; i.e., they are laid out
# as blocks on the page.

block_tags = [
    "__root__",
    "html", "head", "meta", "title", "body",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "div", "p",
    "table", "thead", "tbody", "tr", "th", "td", "caption",
    "pre", "ul", "ol", "li", "dl", "dt", "dd",
    "hr"
    ]

# These tags have a well-defined structure, with specific
# kinds of tags allowed within. Unstructured text inside
# these tags will be ignored.

structured_tags = [
    "table", "thead", "tbody", "tr"
    ]

# These tags are allowed to contain other block tags.
# Used to help decide whether to auto-close the current
# tag or nest the new one inside.

can_contain_block_tags = [
    "html", "head", "body", "div",
    "table", "thead", "tbody", "tr", "th", "td",
    "pre", "ul", "ol", "li", "dl", "dd"
    ]

# These tags are treated as inline content, and may be
# contained inside any other (non-structured) tag.

inline_tags = [
    "i", "b", "em", "strong", "code", "br", "img", "a", "small",
    "button"
    ]

# These tags have optional closing tags, and should be
# automatically closed when we see a starting tag that
# cannot be contained inside it.

auto_closing_tags = [
    "meta", "body", "p", "li", "dt", "dd", "tr", "td", "th", "a"
    ]

# These tags do not require a closing tag.

unbalanced_tags = [
    "br", "hr", "img"
    ]

# We ignore the following tags for the purposes of conversion.

ignored_tags = [
    "html", "head", "thead", "tbody", "hr", "font"
    ]

# These are the heading tags, in order of precedence.

heading_tags = [
    "h1", "h2", "h3", "h4", "h5", "h6"
    ]

# Return True if a tag1 element can contain a tag2 element.

def can_contain(tag1, tag2):
    if tag1 == "a" and tag2 == "a":
        return False
    if tag1 == "li" and tag2 == "li":
        return False
    if tag1 in ["dt", "dd"] and tag2 in ["dt", "dd"]:
        return False
    if tag1 == "table" and tag2 not in ["tr", "caption"]:
        return False
    if tag1 == "tr" and tag2 not in ["th", "td"]:
        return False
    if tag2 == "body":
        return False
    return tag1 in can_contain_block_tags or tag2 in inline_tags

# Create a substitution reference for ref and return the inline text.

def create_sub(ref):
    # TODO: create a unique substitution reference for ref.
    return ref

# Class Tag represents an HTML element.
# tagname is the HTML tag.
# attrs is a dictionary of the element's attributes.
# parent is a pointer to the containing element.
# loc is the line number within the HTML source.
# aux is a list of auxiliary blocks (e.g., substitution definitions) to write
#     at the end of the document.

class Tag:
    def __init__(self, tagname, attrs, parent, loc):
        self.tagname = tagname
        self.attrs = attrs
        self.parent = parent
        self.elements = []
        self.loc = loc
        self.aux = []

    # Return True if we are inside a tagname element.
    def is_inside(self, tagname):
        node = self.parent
        while node:
            if node.tagname == tagname:
                return True
            node = node.parent
        return False

    # Append a new child element.
    def append_element(self, elem):
        if elem.tagname == "body":
            self.elements += elem.elements
        else:
            self.elements.append(elem)

    # Append a new auxiliary block.
    def append_aux(self, elem):
        self.aux.append(elem)

    # Append a new text node.
    def append_data(self, data):
        if self.tagname in structured_tags:
            if data.strip():
                sys.stderr.write("Error: found unstructured data inside %s element at line %d\n" % (self.tagname, self.loc[0]))
            return
        if data:
            self.elements.append(data)

    # Close the current element. If a block tag, append it as a block
    # to the parent; if an inline tag, convert it to inline text and
    # append the text to the parent. Return the parent element.
    def close(self):
        if not self.parent:
            sys.stderr.write("Error: attempted to close root tag\n")
            return self
        if self.tagname in block_tags:
            self.parent.append_element(self)
        else:
            self.parent.append_data(self.to_md_inline())
        for item in self.aux:
            self.parent.append_aux(item)
        return self.parent

    # Write a debug representation of the current subtree.
    def debug(self, level):
        sys.stderr.write(level + self.tagname + "\n")
        for e in self.elements:
            if isinstance(e, Tag):
                e.debug(level + "| ")
            else:
                sys.stderr.write(level + "| " + repr(e) + "\n")

    # Convert the current tag to inline markdown.
    def to_md_inline(self):
        if self.tagname == "br":
            # Ignore <br> tags for now.
            return ""

        elif self.tagname == "img":
            return self.img_to_md()

        elif self.tagname == "i" or self.tagname == "em":
            text = self.collect_inline_elements().strip()
            return "*" + text + "*" if text else ""

        elif self.tagname == "b" or self.tagname == "strong":
            text = self.collect_inline_elements().strip()
            return "**" + text + "**" if text else ""

        elif self.tagname == "code" and self.is_inside("pre"):
            return self.collect_inline_elements()

        elif self.tagname == "code":
            text = self.collect_inline_elements().strip()
            return "``" + text + "``" if text else ""

        elif self.tagname == "a":
            href = self.attrs["href"] if "href" in self.attrs else "#"
            text = self.collect_inline_elements().strip()
            return "[" + text + "](%s)" % href

        else:
            return self.collect_inline_elements()

    # Convert all child elements to inline markdown and collect them into
    # one chunk of text.
    def collect_inline_elements(self):
        text = ""
        for elem in self.elements:
            if isinstance(elem, Tag):
                elem = elem.to_md_inline()
            text += elem
        return text

    # Convert a block element to markdown.
    def to_md(self):
        text = ""

        if self.tagname == "title":
            text = ""

        elif self.tagname == "table":
            text = self.table_to_md()

        elif self.tagname == "pre":
            text = indent(self.pre_to_md())

        elif self.tagname in heading_tags:
            text = self.heading_to_md(heading_tags.index(self.tagname))

        elif self.tagname in ["ul", "ol"]:
            text = self.list_to_md()

        elif self.tagname == "dl":
            text = self.dl_to_md()

        else:
            text = self.block_tag_to_md()

        if not self.parent and self.aux:
            text += "\n\n" + "\n\n".join(self.aux)
        return text

    # Return markdown for a heading element.
    def heading_to_md(self, level):
        blocks = [elem.to_md() if isinstance(elem, Tag) else elem for elem in self.elements]
        text = "".join(blocks)
        return "#" * (level + 1) + " " + text.replace("\n", " ")

    # Return markdown for a <pre> element.
    def pre_to_md(self):
        blocks = [elem.pre_to_md() if isinstance(elem, Tag) else elem for elem in self.elements]
        return "".join(blocks).strip("\n")

    # Return markdown for a <ul> or <ol> element.
    def list_to_md(self):
        marker = "* " if self.tagname == "ul" else "1. "
        elems = []
        for elem in self.elements:
            if isinstance(elem, Tag) and elem.tagname == "li":
                elems.append(hanging_indent(elem.to_md().strip(), marker))
        return "\n\n".join(elems)

    # Return markdown for a <dl> element.
    def dl_to_md(self):
        dl_items = []
        dt_item = ""
        dd_items = []
        text = ""
        for elem in self.elements:
            if isinstance(elem, Tag) and elem.tagname == "dt":
                text = text.strip()
                if dt_item or dd_items or text:
                    dd_items += form_paras(text)
                    dd_items = map(indent, dd_items)
                    dl_items.append(dt_item + "\n" + "\n\n".join(dd_items))
                    dt_item = ""
                    dd_items = []
                    text = ""
                dt_item = elem.to_md()
            else:
                if isinstance(elem, Tag):
                    dd_items += form_paras(text)
                    text = ""
                    block = elem.to_md()
                    if block:
                        dd_items.append(block)
                else:
                    text += elem
        text = text.strip()
        if dt_item or dd_items or text:
            dd_items += form_paras(text)
            dd_items = map(indent, dd_items)
            dl_items.append(dt_item + "\n" + "\n\n".join(dd_items))
        return "\n\n".join(dl_items)

    # Return markdown for an <img> element.
    def img_to_md(self):
        if "src" in self.attrs:
            src = self.attrs["src"]
        else:
            src = "#"
        sub = create_sub(src)
        if "alt" in self.attrs:
            alt = self.attrs["alt"]
        else:
            alt = ""
        return "[!" + src + "]"

    # Convert a table to markdown.
    def table_to_md(self):
        caption = ""
        rows = []
        column_widths = []

        # Find the <caption> (if any) and the <tr> elements.
        header_rows = 0
        for row in self.elements:
            if not isinstance(row, Tag):
                pass
            elif row.tagname == "caption":
                caption = row.to_md()
            elif row.tagname == "tr":
                # Extract the <th> and <td> elements.
                cols = list(filter(lambda e: isinstance(e, Tag) and e.tagname in ["th","td"], row.elements))
                if all([e.tagname == "th" for e in cols]):
                    header_rows += 1
                if cols:
                    cols = list(map(lambda col: col.to_md(), cols))
                    rows.append(cols)
                    # Record the max column width for each column
                    if len(cols) > len(column_widths):
                        column_widths.extend(0 for _ in range(len(column_widths), len(cols)))
                    for i in range(len(cols)):
                        column_widths[i] = max(column_widths[i], longest_line(cols[i]))
            else:
                sys.stderr.write("Found <%s> tag in <table> at %d\n" % (row.tagname, row.loc[0]))

        # Generate single-row and single-column tables as regular paragraphs.
        if len(column_widths) == 1 or len(rows) == 1:
            blocks = []
            for row in rows:
                blocks += row
            return "\n\n".join(blocks)

        # Generate the table, row by row.
        text = ""
        for row in rows:
            col_num = 0
            padded_cells = []
            for cell in row:
                if len(cell) < column_widths[col_num]:
                    cell += " " * (column_widths[col_num] - len(cell))
                padded_cells.append(cell)
                col_num += 1
            text += "|" + "|".join(padded_cells) + "|\n"

        return text

    # Convert child elements to md, and combine the results.
    def block_tag_to_md(self):
        blocks = []
        text = ""
        for elem in self.elements:
            if isinstance(elem, Tag):
                blocks += form_paras(text)
                text = ""
                block = elem.to_md()
                if block:
                    blocks.append(block)
            else:
                text += elem
        blocks += form_paras(text)
        return "\n\n".join(blocks)

# Indent all lines of a paragraph by 4 spaces.
def indent(text):
    lines = []
    for s in text.split("\n"):
        if s:
            lines.append("    " + s)
        else:
            lines.append("")
    return "\n".join(lines)

# Place marker in front of the first line of text, and indent
# all subsequent lines.
def hanging_indent(text, marker):
    prefix = " " * len(marker)
    lines = []
    for s in text.split("\n"):
        if lines:
            lines.append(prefix + s.strip())
        elif s:
            lines.append(marker + s.strip())
        else:
            lines.append("")
    return "\n".join(lines)

# Form paragraphs out of text, with single blank lines between each paragraph.

def form_paras(text):
    lines = [s.strip() for s in text.split("\n")]
    paras = []
    para = []
    for l in lines:
        if l:
            para.append(l)
        elif para:
            paras.append("\n".join(para))
            para = []
    if para:
        paras.append("\n".join(para))
    return paras

# Find longest line in a paragraph.

def longest_line(text):
    lengths = [len(s) for s in text.split("\n")]
    return max(lengths)

# Class HtmlToMD: Parse the HTML source, build an intermediate tree,
# and convert to Markdown.

class HtmlToMD(HTMLParser):
    def __init__(self):
        self.current_tag = Tag("__root__", None, None, (0,0))
        self.title = ""
        HTMLParser.__init__(self)

    def close(self):
        HTMLParser.close(self)
        unclosed = []
        while self.current_tag.parent is not None:
            if self.current_tag.tagname not in auto_closing_tags:
                unclosed.append("%s (%d)" % (self.current_tag.tagname, self.current_tag.loc[0]))
            self.current_tag = self.current_tag.close()
        if unclosed:
            sys.stderr.write("End of file with unclosed tags: %s\n" % ", ".join(unclosed))

    def handle_starttag(self, tagname, attrs):
        if tagname in ignored_tags:
            return

        while (self.current_tag.tagname in auto_closing_tags
               and not can_contain(self.current_tag.tagname, tagname)):
            self.current_tag = self.current_tag.close()

        if not can_contain(self.current_tag.tagname, tagname):
            if self.current_tag.tagname == "table":
                sys.stderr.write("Inserting missing <tr> before <%s> at line %d\n" % (tagname, self.getpos()[0]))
                self.handle_starttag("tr", [])
            elif self.current_tag.tagname == "tr":
                sys.stderr.write("Inserting missing <td> before <%s> at line %d\n" % (tagname, self.getpos()[0]))
                self.handle_starttag("td", [])

        attrs = dict(attrs)
        tag = Tag(tagname, attrs, self.current_tag, self.getpos())
        self.current_tag = tag
        if tagname in unbalanced_tags:
            self.current_tag = self.current_tag.close()

    def handle_endtag(self, tagname):
        if tagname in ignored_tags or tagname in unbalanced_tags:
            return

        if tagname == "title":
            self.title = self.current_tag.to_md_inline()

        if tagname != self.current_tag.tagname and self.current_tag.is_inside(tagname):
            while tagname != self.current_tag.tagname:
                if (self.current_tag.tagname in auto_closing_tags
                        and can_contain(tagname, self.current_tag.tagname)):
                    sys.stderr.write("Auto-closing %s at line %d\n" % (self.current_tag.tagname, self.getpos()[0]))
                else:
                    sys.stderr.write("Force-closing %s at line %d\n" % (self.current_tag.tagname, self.getpos()[0]))
                self.current_tag = self.current_tag.close()

        if tagname == self.current_tag.tagname:
            self.current_tag = self.current_tag.close()
        else:
            sys.stderr.write("Found </%s> at line %d, expected </%s>.\n" % (tagname, self.getpos()[0], self.current_tag.tagname))

    def handle_data(self, data):
        # Convert old troff-style quoting conventions to Unicode quotes.
        data = re.sub(r"``", u"\u201c", data)
        data = re.sub(r"''", u"\u201d", data)
        # Markup code terms like DW_AT_type and .debug_info.
        data = re.sub(r'(?<!\w)([.a-zA-Z]+_[a-zA-Z0-9_]+)\b', r'`\1`', data)
        self.current_tag.append_data(data)

    def handle_entityref(self, name):
        self.current_tag.append_data(unichr(name2codepoint[name]))

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        self.current_tag.append_data(c)

    def debug(self):
        self.current_tag.debug("")

    def to_md(self):
        return self.current_tag.to_md()

# Return a list of all descendent tags with the given tagname.

def find_tags(block, tagname):
    ret = []
    for e in block.elements:
        if isinstance(e, Tag):
            if e.tagname == tagname:
                ret.append(e)
            else:
                ret += find_tags(e, tagname)
    return ret

# The DWARF pages all start with two table elements as the page header,
# and end with a table element as the page footer. Recognize these.

def is_header_footer(elem):
    if not isinstance(elem, Tag):
        return False
    if elem.tagname != "table":
        return False
    for cell in find_tags(elem, "td"):
        text = cell.to_md()
        if "[!dwarf.png]" in text:
            return True
        if "[HOME]" in text:
            return True
        if "All logos and trademarks" in text:
            return True
    return False

strip_header_footer = False
convert_proposal = False
dwarf_version = "6"
debug = False

try:
    opts, args = getopt.getopt(sys.argv[1:], "hdpv:")
except getopt.GetoptError as err:
    sys.stderr.write(err + "\n")
    sys.exit(2)
for o, a in opts:
    if o == "-p":
        convert_proposal = True
    elif o == "-h":
        strip_header_footer = True
    elif o == "-v":
        dwarf_version = a
    elif o == "-d":
        debug = True

parser = HtmlToMD()

for l in sys.stdin:
    parser.feed(l.expandtabs(4).replace("\r\n", "\n"))
parser.close()

if debug:
    parser.debug()

root = parser.current_tag
if strip_header_footer:
    root.elements = list(filter(lambda e: not is_header_footer(e), root.elements))

if convert_proposal:
    table_elems = find_tags(root, "table")
    if len(table_elems) > 0:
        meta_info_tbl = table_elems[0]
        if len(meta_info_tbl.elements) > 0:
            first_row = meta_info_tbl.elements[0]
            meta_info = first_row.elements
            if len(meta_info) >= 6:
                prop_num = meta_info[0].to_md()
                prop_author = meta_info[1].to_md()
                prop_title = meta_info[2].to_md()
                prop_type = meta_info[3].to_md()
                prop_status = meta_info[4].to_md()
                prop_champion = meta_info[5].to_md()
                prop_submit_date = re.sub(r"(\d\d)(\d\d)(\d\d)\..*", r"20\1-\2-\3", prop_num)
                print("Title:       %s" % prop_title)
                print("Author:      %s" % prop_author)
                print("Champion:    %s" % prop_champion)
                print("Submit-Date: %s" % prop_submit_date)
                print("Propid:      %s" % prop_num)
                print("Type:        %s" % prop_type)
                print("Status:      %s" % prop_status)
                print("Version:     %s" % dwarf_version)
                print("")

    pre_elems = find_tags(parser.current_tag, "pre")
    if pre_elems:
        print(pre_elems[0].pre_to_md())

else:
    if parser.title:
        print("Title: %s" % parser.title)
        print("")
    print(root.to_md())
