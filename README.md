# OpenCL-source-to-C-string-converter
Converts OpenCL kernel source file into a C/C++ char string.

## Run as follows
```batch
python oclProgramFileToString.py inputFileName.cl outputFileName.cpp
```

Input file contains OpenCL kernel soure code. Output file contains the same code, but in form of a const char* C/C++ string.

## Optional switches
- ```-v``` turn on verbose mode
- ```-c``` convert into compact form - remove all comments, redundant spaces and empty lines

## Requirements
- installed Python3 interpreter
