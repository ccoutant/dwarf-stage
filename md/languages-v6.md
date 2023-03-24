Title: DWARF Version 6 Language and Version Codes

# DWARF Version 6 Language and Version Codes

[Issue 210419.1](issues/210419.1.html)
introduced a way to separately specify languages and versions which is
expected to be adopted for DWARF Version 6.
As described in the proposal, each supported language has a specified
value for `DW_AT_language_name` and each version of that language has a
unique `DW_AT_language_version`.

New language codes and version codes may be requested by submitting a
request on the [Public Comment](comment.html) page.

|Language                |Language Code (`DW_AT_language_name`)|Value |Default Lower Bound|Version Codes (`DW_AT_language_version`)|
|:-----------------------|:------------------------------------|:----:|:-----------------:|:---------------------------------------|
|ISO Ada †               |`DW_LNAME_Ada`                       |0x0001|1                  |                                        |
|BLISS                   |`DW_LNAME_BLISS`                     |0x0002|0                  |                                        |
|C (K&R and ISO)         |`DW_LNAME_C`                         |0x0003|0                  |K&R 000000                              |
|ISO C++                 |`DW_LNAME_C_plus_plus`               |0x0004|0                  |C++98 199711<br>C++11 201103<br>C++14 201402<br>C++17 201703<br>C++20 202002|
|ISO Cobol †             |`DW_LNAME_Cobol`                     |0x0005|1                  |                                        |
|Crystal                 |`DW_LNAME_Crystal`                   |0x0006|0                  |                                        |
|D                       |`DW_LNAME_D`                         |0x0007|0                  |                                        |
|Dylan                   |`DW_LNAME_Dylan`                     |0x0008|0                  |                                        |
|ISO Fortran             |`DW_LNAME_Fortran`                   |0x0009|1                  |                                        |
|Go †                    |`DW_LNAME_Go`                        |0x000a|0                  |                                        |
|Haskell †               |`DW_LNAME_Haskell`                   |0x000b|0                  |                                        |
|HIP                     |`DW_LNAME_HIP`                       |0x001d|0                  |                                        |
|Java                    |`DW_LNAME_Java`                      |0x000c|0                  |                                        |
|Julia                   |`DW_LNAME_Julia`                     |0x000d|1                  |                                        |
|Kotlin                  |`DW_LNAME_Kotlin`                    |0x000e|0                  |                                        |
|Modula 2                |`DW_LNAME_Modula2`                   |0x000f|1                  |                                        |
|Modula 3 †              |`DW_LNAME_Modula3`                   |0x0010|1                  |                                        |
|Objective C             |`DW_LNAME_ObjC`                      |0x0011|0                  |                                        |
|Objective C++           |`DW_LNAME_ObjC_plus_plus`            |0x0012|0                  |                                        |
|OCaml                   |`DW_LNAME_OCaml`                     |0x0013|0                  |                                        |
|OpenCL †                |`DW_LNAME_OpenCL`                    |0x0014|0                  |                                        |
|ISO Pascal              |`DW_LNAME_Pascal`                    |0x0015|1                  |                                        |
|ANSI PL/I †             |`DW_LNAME_PLI`                       |0x0016|1                  |                                        |
|Python †                |`DW_LNAME_Python`                    |0x0017|0                  |                                        |
|RenderScript            |`DW_LNAME_RenderScript`              |0x0018|0                  |                                        |
|Rust                    |`DW_LNAME_Rust`                      |0x0019|0                  |                                        |
|Swift                   |`DW_LNAME_Swift`                     |0x001a|0                  |                                        |
|Unified Parallel C (UPC)|`DW_LNAME_UPC`                       |0x001b|0                  |                                        |
|Zig                     |`DW_LNAME_Zig`                       |0x001c|0                  |                                        |

† These names and their associated values are reserved, but
the languages they represent are not well supported.
