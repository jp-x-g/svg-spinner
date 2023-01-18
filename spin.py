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
		# print(f"{stringy} ({str(a).zfill(7)} of {str(len(file)).zfill(7)})")
		if (re.match(r'^#[A-Fa-f0-9]{6}$', stringy)):
			file = file[0:a] + "#" + execute_pattern(stringy[1:], places=places, values=values, overlay=overlay, overlay_amount=overlay_amount) + file[a+7:]
		else:
			pass

	# execute_pattern(hex, places=places, values=values, overlay=overlay, overlay_amount=overlay_amount)

	return file



def save_file(contents, path, filename, suffix):
	"""
	Output SVG file, with contents specified, to path + filename + suffix + .svg
	"""
	filename = filename[0:-4] + suffix + filename[-4:]
	savepath = path + filename

	print(f"Saved to: {savepath}")

	f = open(savepath, "w")
	f.write(str(contents))
	f.close()
	print("")

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

	# Spin of forwards hues (123)
	datanew = return_spinned(data, places=[2, 3, 1], values=[1, 1, 1], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "231")
	datanew = return_spinned(data, places=[3, 1, 2], values=[1, 1, 1], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "312")

	# Spin of backwards hues (321)
	datanew = return_spinned(data, places=[3, 2, 1], values=[1, 1, 1], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "321")
	datanew = return_spinned(data, places=[2, 1, 3], values=[1, 1, 1], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "213")
	datanew = return_spinned(data, places=[1, 3, 2], values=[1, 1, 1], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "132")

	# Dark and bright
	datanew = return_spinned(data, places=[1, 2, 3], values=[0.5, 0.5, 0.5], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "dark")
	datanew = return_spinned(data, places=[1, 2, 3], values=[2, 2, 2], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "bright")

	# Dark and bright (via overlays)
	datanew = return_spinned(data, places=[1, 2, 3], values=[1, 1, 1], overlay="000000", overlay_amount=0.5)
	save_file(datanew, input_path, input_file, "dark2")
	datanew = return_spinned(data, places=[1, 2, 3], values=[1, 1, 1], overlay="FFFFFF", overlay_amount=0.5)
	save_file(datanew, input_path, input_file, "bright2")

	# Colors by doubling R, G, and B channels
	datanew = return_spinned(data, places=[1, 2, 3], values=[2, 1, 1], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "2r")
	datanew = return_spinned(data, places=[1, 2, 3], values=[1, 2, 1], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "2g")
	datanew = return_spinned(data, places=[1, 2, 3], values=[1, 1, 2], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "2b")

	# Primary colors (adding 1/3 to one and subtracting 1/6 from two)
	datanew = return_spinned(data, places=[1, 2, 3], values=[1.333, 0.833, 0.833], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "1r")
	datanew = return_spinned(data, places=[1, 2, 3], values=[0.833, 1.333, 0.833], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "1g")
	datanew = return_spinned(data, places=[1, 2, 3], values=[0.833, 0.833, 1.333], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "1b")

	# Compound colors (adding 1/6 to two and subtracting 1/3 from one)
	datanew = return_spinned(data, places=[1, 2, 3], values=[1.166, 1.166, 0.666], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "1y")
	datanew = return_spinned(data, places=[1, 2, 3], values=[0.666, 1.166, 1.166], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "1c")
	datanew = return_spinned(data, places=[1, 2, 3], values=[1.166, 0.066, 1.166], overlay="000000", overlay_amount=0)
	save_file(datanew, input_path, input_file, "1m")



	# print(datanew)
	#print(execute_pattern("1a2b3c", places=[3, 2, 1], overlay="FFFFFF", overlay_amount=0.9))

	#print(data)

	# TODO: Write the program.

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