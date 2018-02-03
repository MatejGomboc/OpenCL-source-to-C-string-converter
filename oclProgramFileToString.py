#!/usr/bin/python

import sys, argparse, re

def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


def empty_string_remover(text):
	new_text = text
	new_text_prev = ""
	while (new_text != new_text_prev):
		new_text_prev = new_text
		new_text = new_text.replace(" \"", "\"")
		new_text = new_text.replace("\t\"", "\"")
	return new_text


def empty_line_remover(text):
	new_text = text
	new_text_prev = ""
	while (new_text != new_text_prev):
		new_text_prev = new_text
		new_text = new_text.replace("\n\n", "\n") # remove empty lines
	return new_text


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	parser.add_argument("-c", "--compact", help="remove all comments and empty lines", action="store_true")
	parser.add_argument("inputFileName", help="name of input OpenCL file with source", type=str)
	parser.add_argument("outputFileName", help="name of output C++ file with source as char string", type=str)
	args = parser.parse_args()

	if not args.inputFileName.lower().endswith(".cl"):
		sys.exit("invalid input file extension: " + args.inputFileName)
	if not args.outputFileName.lower().endswith(".cpp"):
		sys.exit("invalid output file extension: " + args.outputFileName)

	if args.verbose:
		print("input file: " + args.inputFileName)
		print("output file: " + args.outputFileName)

	stringSource = open(args.inputFileName, 'r').read()

	if args.verbose:
		print("\nOpenCL source:")
		print(stringSource)

	if args.compact:
		stringSource = comment_remover(stringSource) # remove all comments

	stringSource = stringSource.replace("\\", "\\\\") # for multi-line strings
	stringSource = stringSource.replace("\"", "\\\"") # for strings
	stringSource = stringSource.replace("\'", "\\\'") # for chars
	stringSource = stringSource.replace("\\\a", "\\\\\\\a") # if inside a string
	stringSource = stringSource.replace("\\\b", "\\\\\\\b") # if inside a string
	stringSource = stringSource.replace("\\\f", "\\\\\\\f") # if inside a string
	stringSource = stringSource.replace("\\\r", "\\\\\\\r") # if inside a string
	stringSource = stringSource.replace("\\\t", "\\\\\\\t") # if inside a string
	stringSource = stringSource.replace("\\\v", "\\\\\\\v") # if inside a string
	stringSource = stringSource.replace("\\\n", "\\\\\\\n") # if inside a string
	stringSource = stringSource.replace("\n", "\"\n\"") # for correct ending of new multi-line string

	stringSource = "const char* " + args.inputFileName[:-3] + " = \n\"" + stringSource + "\"\n"

	stringSource = empty_string_remover(stringSource) # remove redundant spaces and tabs
	stringSource = stringSource.replace("\"\"", "") # remove empty multi-line string
	stringSource = stringSource[:-1]

	if args.compact:
		stringSource = empty_line_remover(stringSource) # remove empty lines

	if args.verbose:
		print("source as C++ char string:")
		print(stringSource)

	open(args.outputFileName, "w").write(stringSource)
