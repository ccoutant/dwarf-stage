Title: DWARF 5 Standard

# DWARF 5 Standard

The **DWARF Version 5 Debugging Format Standard**
is based on the [**DWARF Version 4 Standard**](dwarf4std.html).
It is an upward compatible extension to the previous version of the standard.

The major enhancements in DWARF Version 5 are:

* Description of the objectives and rationale for the design and
  evolution of the DWARF Standard.

* Merge `.debug_types` into `.debug_info` section.

* Support collecting common debug information into a single
  supplementary object file.

* Replace the line number program header allowing better data
  compression and source validation.

* Support split object file and package representations to allow DWARF
  info to be kept separate from executable files.

* Replace `.debug_macinfo` with `.debug_macro` representation allowing
  much more compact representation of C/C++ macros.

* Replace `.debug_pubnames` and `.debug_pubtypes` with much more
  functional `.debug_names` section.

* Replace location list (`.debug_loc`) and range list (`.debug_ranges`)
  sections with new sections (`.debug_loclists` and `.debug_rnglists`)
  allowing more compact representation and eliminating relocations.

* Add new TAG to describe call site information, including tail call and
  tail recursion.

* Improve support for FORTRAN assumend rank arrays, dynamic rank arrays,
  and co-arrays.

* Add new operators which support a DWARF expression stack containing
  typed values.

* Add support for C++ auto return type, deleted member functions, and
  defaulted constructors and destructors.

* Add new attribute to identify a subprogram which does not return to its caller.

* Add language codes for C 2011, C++ 2003, C++ 2011, C++ 2014, Dylan,
  Fortran 2003, Fortran 2008, Go, Haskell, Julia, Modula 3, Ocaml, OpenCL,
  Rust, Swift, and BLISS.

* Numerous minor additions to improve functionality and performance.

The DWARF Version 5 Standard is compatible with DWARF Version 4 except as follows:

* The compilation unit header (in the `.debug_info` section) has a new `unit_type` field.

* New operand forms for attribute values are defined (`DW_FORM_addrx*`,
  `DW_FORM_data16`, `DW_FORM_implicit_const`, `DW_FORM_line_strp`,
  `DW_FORM_loclistx`, `DW_FORM_rnglistx`, `DW_FORM_ref_sup*`,
  `DW_FORM_strp_sup` and `DW_FORM_strx*`).

* The line number table header is substantially revised.

* A location list entry with the address range (0, maximum-address) is defined
  as the new default location list entry.

* In a string type, the `DW_AT_byte_size` attribute is re-defined to always
  describe the size of the string type. (Previously it described the size of the
  optional string length data field if the `DW_AT_string_length` attribute was
  also present.)

* New representations for macro definitions, symbol lookup, location lists and range lists.

Read the [press release](dwarf5-press-release.html)

[Download DWARF Version 5 Standard (PDF)](doc/DWARF5.pdf)
