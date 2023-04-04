# Makefile for building the DWARF website.

# Markdown files are found under $(SOURCE_DIR).
SOURCE_DIR = md

# HTML files are written to $(BUILD_DIR).
BUILD_DIR = htdocs

# Build tools are in $(TOOLS_DIR).
TOOLS_DIR = tools
MD_WRAPPER = $(TOOLS_DIR)/md-wrapper.py
GEN_INDEX = $(TOOLS_DIR)/gen-index.py

# Markdown source files
TOP_SOURCES = $(wildcard $(SOURCE_DIR)/*.md)
ISSUES_SOURCES = $(wildcard $(SOURCE_DIR)/issues/*.md)

# Static files in these directories need to be copied to $(BUILD_DIR).
STATICDIRS = doc images static

# Destination files.
ALL_TOP = $(TOP_SOURCES:$(SOURCE_DIR)/%.md=$(BUILD_DIR)/%.html)
ALL_ISSUES = $(ISSUES_SOURCES:$(SOURCE_DIR)/%.md=$(BUILD_DIR)/%.html)
ALL_INDEXES = $(BUILD_DIR)/issues-v3.html \
              $(BUILD_DIR)/issues-v4.html \
              $(BUILD_DIR)/issues-v5.html \
              $(BUILD_DIR)/issues-closed.html \
              $(BUILD_DIR)/issues.html

# Templates for generating HTML.
DWARF_TEMPLATE = templates/dwarf-template.html
ISSUE_TEMPLATE = templates/issue-template.html
INDEX_TEMPLATE = templates/index-template.html
TEMPLATES = $(DWARF_TEMPLATE) $(ISSUE_TEMPLATE) $(INDEX_TEMPLATE)

# Files included by the templates (indirect dependencies).
OTHER_DEPS = templates/nav.html templates/footer.html

all: all-top all-issues all-indexes all-static

all-top: $(ALL_TOP)

all-issues: $(ALL_ISSUES)

all-indexes: $(ALL_INDEXES)

# Copy static files to the destination directory only if changed.
all-static: 
	@for d in $(STATICDIRS); \
	do \
	  mkdir -p $(BUILD_DIR)/$$d; \
	  for f in $$d/*; \
	  do \
	    if ! cmp -s "$$f" $(BUILD_DIR)/"$$f"; \
	    then \
	      echo COPY "$$f" $(BUILD_DIR)/$$d/; \
	      rm -f $(BUILD_DIR)/"$$f" && \
	        cp "$$f" $(BUILD_DIR)/$$d/; \
	    fi; \
	  done; \
	done

# Every generated file depends on one of the templates and on the included files.
$(ALL_TOP): $(DWARF_TEMPLATE) $(OTHER_DEPS)
$(ALL_ISSUES): $(ISSUE_TEMPLATE) $(OTHER_DEPS)
$(ALL_INDEXES): $(INDEX_TEMPLATE) $(OTHER_DEPS)

# Rule for converting markdown files under $(SOURCE_DIR)/issues.
# (This rule must come before the next one.)
$(BUILD_DIR)/issues/%.html: $(SOURCE_DIR)/issues/%.md
	@mkdir -p $(@D)
	@echo MD_WRAPPER $< $@
	@$(MD_WRAPPER) -r $(BUILD_DIR) -t $(ISSUE_TEMPLATE) $< $@

# Rule for converting top-level markdown files under $(SOURCE_DIR).
$(BUILD_DIR)/%.html: $(SOURCE_DIR)/%.md
	@mkdir -p $(@D)
	@echo MD_WRAPPER $< $@
	@$(MD_WRAPPER) -r $(BUILD_DIR) -t $(DWARF_TEMPLATE) $< $@

# Rules for generating the issue indexes.
$(ALL_INDEXES): $(ISSUES_SOURCES)

$(BUILD_DIR)/issues-v3.html:
	@mkdir -p $(@D)
	@echo GEN_INDEX $@
	@$(GEN_INDEX) -v 3 -r "$(BUILD_DIR)" -t "$(INDEX_TEMPLATE)" "$(SOURCE_DIR)/issues" $@

$(BUILD_DIR)/issues-v4.html:
	@mkdir -p $(@D)
	@echo GEN_INDEX $@
	@$(GEN_INDEX) -v 4 -r "$(BUILD_DIR)" -t "$(INDEX_TEMPLATE)" "$(SOURCE_DIR)/issues" $@

$(BUILD_DIR)/issues-v5.html:
	@mkdir -p $(@D)
	@echo GEN_INDEX $@
	@$(GEN_INDEX) -v 5 -r "$(BUILD_DIR)" -t "$(INDEX_TEMPLATE)" "$(SOURCE_DIR)/issues" $@

$(BUILD_DIR)/issues-closed.html:
	@mkdir -p $(@D)
	@echo GEN_INDEX $@
	@$(GEN_INDEX) -c -v 6 -r "$(BUILD_DIR)" -t "$(INDEX_TEMPLATE)" "$(SOURCE_DIR)/issues" $@

$(BUILD_DIR)/issues.html:
	@mkdir -p $(@D)
	@echo GEN_INDEX $@
	@$(GEN_INDEX) -o -v 6 -r "$(BUILD_DIR)" -t "$(INDEX_TEMPLATE)" "$(SOURCE_DIR)/issues" $@
