####################################
# Author: Austin White
# Email: austinw@csu.fullerton.edu
# Class: CPSC 456
# Professor: Mikhail Gofman
# Assignment: #2
# Date: November 30, 2014
####################################

import sys
import os
from subprocess import call
from subprocess import Popen, PIPE

OUTPUT_FILE = "bound"

###########################################################
# Returns the hexidecimal dump of a particular binary file
# @exec_path - the executable path
# @return - returns the hexidecimal string representing
# the bytes of the program. The string has format:
# byte1,byte2,byte3....byten,
# For example, 0x19,0x12,0x45,0xda,
##########################################################
def get_hex_dump(exec_path):
	
	# The return value
	ret_val = None
	
	# TODO:
	# 1. Use popen() in order to run hexdump and grab the hexadecimal bytes of the program.
	# 2. If hexdump ran successfully, return the string retrieved. Otherwise, return None.
	# The command for hexdump to return the list of bytes in the program in C++ byte format
	# the command is hexdump -v -e '"0x" 1/1 "%02X" ","' progName

	# (a) "hexdump", "-v", "-e", '"0x" 1/1 "%02X" ","', /usr/bin/ls
	process = Popen(["hexdump", "-v", "-e", "\"0x\" 1/1 \"%02X\" \",\"", exec_path], stdout=PIPE)
	
	# Grab the stdout and the stderr streams
	(output, err) = process.communicate()

	# Wait for the process to finish and get the exit code
	exit_code = process.wait()

	# If the process exited with a code of 0, then it ended normally.
	# Otherwise, it terminated abnormally
	if exit_code == 0:
		ret_val = output
	
	return ret_val

###########################################################
# Compiles the binary programs into a single output file
# @o_file - output file
# @return - None
##########################################################
def compile_header_file(o_file):

	# (c) Invoke the g++ compiler
	process = Popen(["g++", "binderbackend.cpp", "-o", o_file, "-std=gnu++11"], stdout=PIPE)

	# Grab the stdout and the stderr streams
	(output, err) = process.communicate()

	# Wait for the process to finish and get the exit code
	exit_code = process.wait()

	# If the process exited with a code of 0, then it ended normally.
	# Otherwise, it terminated abnormally
	if exit_code != 0:
		raise Exception("Error compiling binary")

def main():
	argv = sys.argv[1:]

	if len(argv) == 0:
		raise Exception("Insufficient number of arguments supplied. Format: python binder.py [PROG1] [PROG2]...[PROGn]")

	# Make sure all programs exist
	for program in argv:
		if not os.path.isfile(program):
			print "ERROR: %s cannot be found." % program
			sys.exit(1)

	# (b) Open the header file
	code_array_file = open("codearray.h", "w")

	code_array_file.write("#include <string>\n\nusing namespace std;\n\n")

	# Start writing the header file
	code_array_file.write("unsigned char* codeArray[" + str(len(argv)) + "] = {\n")

	program_lengths = []

	for program in argv:
		
		# Get the program's hexdump
		prog_output = get_hex_dump(program)

		# Get number of bits of hex output
		num_bits = prog_output.count(",") + 1 # counting number of commas, so account for extra bit at the end

		# Add the num_bits to an array for later
		program_lengths.append(num_bits)

		# Dump hex into header file
		code_array_file.write("  new unsigned char[" + str(num_bits) + "] {" + prog_output + "},")

		code_array_file.write("\n")

	# Close up the array
	code_array_file.write("};")

	# Add macro
	code_array_file.write("\n\n#define NUM_BINARIES " + str(len(argv)))

	# Add program lengths array
	program_lengths_str = ",".join(map(str, program_lengths))
	code_array_file.write("\n\nint programLengths[NUM_BINARIES] = {" + program_lengths_str + "};")

	# Close the header file
	code_array_file.close()

	compile_header_file(OUTPUT_FILE)

if __name__ == "__main__":
	main()