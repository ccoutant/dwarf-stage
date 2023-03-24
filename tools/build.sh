#!/bin/sh

SRCDIR="md"
DESTDIR="htdocs"
TEMPLATEDIR="templates"
TOOLSDIR="tools"
STATICDIRS="doc images static"

OLD_DWARF_VERSIONS="3 4 5"
DWARF_VERSION="6"

DWARF_TEMPLATE="$TEMPLATEDIR/dwarf-template.html"
ISSUE_TEMPLATE="$TEMPLATEDIR/issue-template.html"
INDEX_TEMPLATE="$TEMPLATEDIR/index-template.html"

function die() {
  echo "error: $@" >&2
  exit 1
}

test -d "$SRCDIR" || die "Directory $SRCDIR missing."
test -d "$TEMPLATEDIR" || die "Directory $TEMPLATEDIR missing."
test -d "$TOOLSDIR" || die "Directory $TOOLSDIR missing."
for d in $STATICDIRS
do
  test -d "$d" || die "Directory $d missing."
done

set -e

# Convert top-level markdown files
mkdir -p "$DESTDIR"
echo "Generating top-level pages..."
for f in $SRCDIR/*.md
do
  b=$(basename "$f" ".md")
  $TOOLSDIR/md-wrapper.py -r "$DESTDIR" -t "$DWARF_TEMPLATE" "$f" "$DESTDIR/$b.html"
done

# Convert the markdown files under issues/
mkdir -p "$DESTDIR/issues"
echo "Generating issue pages..."
for f in $SRCDIR/issues/*.md
do
  b=$(basename "$f" ".md")
  $TOOLSDIR/md-wrapper.py -p -r "$DESTDIR" -t "$ISSUE_TEMPLATE" "$f" "$DESTDIR/issues/$b.html"
done

# Build the issue indexes
echo "Generating issue indexes..."
for v in $OLD_DWARF_VERSIONS
do
  dest="$DESTDIR/issues-v${v}.html"
  $TOOLSDIR/gen-index.py -v "$v" -r "$DESTDIR" -t "$INDEX_TEMPLATE" "$SRCDIR/issues" "$dest"
done

dest="$DESTDIR/issues.html"
$TOOLSDIR/gen-index.py -v "$DWARF_VERSION" -r "$DESTDIR" -t "$INDEX_TEMPLATE" "$SRCDIR/issues" "$dest"

# Hardlink the static files into the build tree
echo "Hard-linking static files..."
for d in $STATICDIRS
do
  mkdir -p "$DESTDIR/$d"
  ln -f "$d"/* "$DESTDIR/$d/"
done
