#! /usr/bin/python
# -*- coding: utf-8 -*-
# JPxG, 2023 January 17
# Takes a SVG as input and rotates it to produce multiple outputs.
import sys
import os
import colordecode
import re


def execute_pattern(hexc, places=[1, 2, 3], values=[1, 1, 1], overlay="000000", overlay_amount=0):
	"""
	Read a hex code and apply transformations to it based on params.
	Order of transformations is this:
	places = transposition order of hex code (eg. [1, 2, 3] retains order, [3, 2, 1] is reversed)
	values = amount to multiply hex values by (eg. [1, 1, 1] retains values, [0.4, 0.4, 0.4] is 40% of values)
	overlay = hex code of overlay color
	overlay_amount = float between 0 (0% converted to the overlay color) and 1 (100%).
	"""
	output = ""
	hexc = [hexc[0:2], hexc[2:4], hexc[4:6]]
	# Turn "1a2b3c" into ["1a", "2b", "3c"]
	overlay = [overlay[0:2], overlay[2:4], overlay[4:6]]
	# Do the same for the overlay hex.
	hexc = [hexc[places[0]-1], hexc[places[1]-1], hexc[places[2]-1]]
	# Transpose according to the "places" array.
	for i in range(0,3):
		hexc[i] = int(hexc[i], 16)
		overlay[i] = int(overlay[i], 16)
		# Turn ["1a", "2b", "3c"] into [26, 43, 60]
		hexc[i] = hexc[i] * values[i]
		# Multiply according to the "values" array.
		hexc[i] = hexc[i] + ((overlay[i] - hexc[i]) * overlay_amount)
		# Apply overlay.
		# value = initial amount + (overlay amount * difference between initial value and overlay value)
		if hexc[i] > 255:
			hexc[i] = 255
			# Hex codes can't go above FF.
		hexc[i] = int(hexc[i])
		# Convert 254.666 to 254.
		hexc[i] = str(hex(hexc[i]))
		# Convert 254 to "0xFE".
		hexc[i] = hexc[i][2:]
		# Convert "0xFE" to "FE".
		output += hexc[i].zfill(2)
		# Add to output string, padded so that e.g. "8" becomes "08".
	return output
	# Return transformed hex code.


def return_spinned(file, places=[1, 2, 3], values=[1, 1, 1], overlay="000000", overlay_amount=0):
	# Go through entire SVG.
	# Extract every hex code.
	# Perform execute_pattern on that hex code.
	# Reconstitute the SVG.
	# Return it as a string.

	for a in range(0, len(file)):
		stringy = file[a:a+7]
		print(f"{stringy} ({str(a).zfill(7)} of {str(len(file)).zfill(7)})")
		if (re.match(r'^#[A-Fa-f0-9]{6}$', stringy)):
			file = file[0:a] + "#" + execute_pattern(stringy[1:], places=places, values=values, overlay=overlay, overlay_amount=overlay_amount) + file[a+7:]
		else:
			pass

	# execute_pattern(hex, places=places, values=values, overlay=overlay, overlay_amount=overlay_amount)

	return file



def save_file(contents, path, filename, suffix):
	# TODO: Make this do something.
	print("D'oh!")




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

	data = colordecode.decode(data)
	# Convert, like, "fill:moccasin" to "fill:#FFE4B5".

	datanew = return_spinned(data, places=[3, 2, 1], values=[1, 1, 1], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "123")
	print(datanew)
	#print(execute_pattern("1a2b3c", places=[3, 2, 1], overlay="FFFFFF", overlay_amount=0.9))

	#print(data)

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