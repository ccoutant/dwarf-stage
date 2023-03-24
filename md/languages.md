Title: DWARF Language Codes

# DWARF Language Codes

DWARF language codes are documented in Table 7.17 (pages 230-231) of the
DWARF Standard, Version 5, reproduced here for your convenience. 
Between revisions of the Standard, new language codes may be requested
by submitting a request on the [Public Comment](Comment.html) page.

*Note:*
[Issue 210419.1](issues/210419.1.html)
introduced a way to separately specify languages and versions,
which is expected to be adopted for DWARF Version 6.
See [DWARF Version 6 Languages and Version Codes](languages-v6.html)
for the new codes.

## Language Codes in DWARF 5

|Language Name (`DW_AT_language`)|Value |Default Lower Bound|
|:-------------------------------|:----:|:-----------------:|
|`DW_LANG_C89`                   |0x0001|0                  |
|`DW_LANG_C`                     |0x0002|0                  |
|`DW_LANG_Ada83`†                |0x0003|1                  |
|`DW_LANG_C_plus_plus`           |0x0004|0                  |
|`DW_LANG_Cobol74`†              |0x0005|1                  |
|`DW_LANG_Cobol85`†              |0x0006|1                  |
|`DW_LANG_Fortran77`             |0x0007|1                  |
|`DW_LANG_Fortran90`             |0x0008|1                  |
|`DW_LANG_Pascal83`              |0x0009|1                  |
|`DW_LANG_Modula2`               |0x000a|1                  |
|`DW_LANG_Java`                  |0x000b|0                  |
|`DW_LANG_C99`                   |0x000c|0                  |
|`DW_LANG_Ada95`†                |0x000d|1                  |
|`DW_LANG_Fortran95`             |0x000e|1                  |
|`DW_LANG_PLI`†                  |0x000f|1                  |
|`DW_LANG_ObjC`                  |0x0010|0                  |
|`DW_LANG_ObjC_plus_plus`        |0x0011|0                  |
|`DW_LANG_UPC`                   |0x0012|0                  |
|`DW_LANG_D`                     |0x0013|0                  |
|`DW_LANG_Python`†               |0x0014|0                  |
|`DW_LANG_OpenCL`†               |0x0015|0                  |
|`DW_LANG_Go`†                   |0x0016|0                  |
|`DW_LANG_Modula3`†              |0x0017|1                  |
|`DW_LANG_Haskell`†              |0x0018|0                  |
|`DW_LANG_C_plus_plus_03`        |0x0019|0                  |
|`DW_LANG_C_plus_plus_11`        |0x001a|0                  |
|`DW_LANG_OCaml`                 |0x001b|0                  |
|`DW_LANG_Rust`                  |0x001c|0                  |
|`DW_LANG_C11`                   |0x001d|0                  |
|`DW_LANG_Swift`                 |0x001e|0                  |
|`DW_LANG_Julia`                 |0x001f|1                  |
|`DW_LANG_Dylan`                 |0x0020|0                  |
|`DW_LANG_C_plus_plus_14`        |0x0021|0                  |
|`DW_LANG_Fortran03`             |0x0022|1                  |
|`DW_LANG_Fortran08`             |0x0023|1                  |
|`DW_LANG_RenderScript`          |0x0024|0                  |
|`DW_LANG_BLISS`                 |0x0025|0                  |

## Language Codes Added Since Version 5

|Language Name                   |Value |Default Lower Bound|
|:-------------------------------|:----:|:-----------------:|
|`DW_LANG_Kotlin`                |0x0026|0                  |
|`DW_LANG_Zig`                   |0x0027|0                  |
|`DW_LANG_Crystal`               |0x0028|0                  |
|`DW_LANG_C_plus_plus_17`        |0x002a|0                  |
|`DW_LANG_C_plus_plus_20`        |0x002b|0                  |
|`DW_LANG_C17`                   |0x002c|0                  |
|`DW_LANG_Fortran18`             |0x002d|0                  |
|`DW_LANG_Ada2005`               |0x002e|0                  |
|`DW_LANG_Ada2012`               |0x002f|0                  |
|`DW_LANG_HIP`                   |0x0030|0                  |

† These names and their associated values are reserved, but
the languages they represent are not well supported.
