#! /usr/bin/python
# -*- coding: utf-8 -*-
# JPxG, 2023 January 17
# Takes a SVG as input and rotates it to produce multiple outputs.
import sys
import os

def spin(input_path="input.svg"):

	input_file = input_path

	while "/" in input_file:
		input_file = input_file[(input_file.find("/")+1):]
		print(input_file)
	input_path = input_path[0:-(len(input_file))]
	# What this whole thing does is create two strings:
	# long/path/to/input/file.svg becomes
	# "long/path/to/input/" and "file.svg"
	
	print(f"Parsing '{input_file}' from '{input_path}'.")

	f = open((input_path + input_file), "r")
	data = f.read()
	f.close()

	# TODO: Write the program.

	exit()
	
	f = open(output, "w")
	f.write(str(stringy))
	f.close()
	print("")
	print(f"Saved to: {output}")
	exit()

if (__name__ == "__main__"):
	print("TSV to Wikitable V1.0, JPxG January 2023")

	if len(sys.argv) == 1:
		spin()
		exit()
	else:
		if (sys.argv[1] == "-h") or (sys.argv[1] == "--help") or (sys.argv[1] == "help"):
			print("> spin(input):")
			print("  Spins colors in the SVG file.")
			print("  Default input is input.svg.")
			print("  Creates five copies with spun hues.")
			print("  Usage should be like this:")
			print("   python3 spin.py inputfile.svg")
			print("")
			exit()
		else:
			if len(sys.argv) == 2:
				spin(str(sys.argv[1]))
				exit()
			if len(sys.argv) == 3:
				spin(str(sys.argv[2]), str(sys.argv[3]))
				exit()
			print("Error: too many arguments provided.")
			print("")
			print("> spin(input):")
			print("  Spins colors in the SVG file.")
			print("  Default input is input.svg.")
			print("  Creates five copies with spun hues.")
			print("  Usage should be like this:")
			print("   python3 spin.py inputfile.svg")
			print("")
			exit()



# I'm pretty sure this covers all the permutations.
# From original hex codes: AA is full, aa is half brightness.
# 
# AABBCC
# aaBBCC
# aabbCC
# aaBBcc
# aabbcc
# AAbbCC
# AABBcc
# AAbbcc
# 
# AACCBB
# aaCCBB
# aaccBB
# aaCCbb
# aaccbb
# AAccBB
# AACCbb
# AAccbb
# 
# BBAACC
# bbAACC
# bbaaCC
# bbAAcc
# bbaacc
# BBaaCC
# BBAAcc
# BBaacc
# 
# BBCCAA
# bbCCAA
# bbccAA
# bbCCaa
# bbccaa
# BBccAA
# BBCCaa
# BBccaa
# 
# CCAABB
# ccAABB
# ccaaBB
# ccAAbb
# ccaabb
# CCaaBB
# CCAAbb
# CCaabb
# 
# CCBBAA
# ccBBAA
# ccbbAA
# ccBBaa
# ccbbaa
# CCbbAA
# CCBBaa
# CCbbaa