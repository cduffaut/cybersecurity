import os
import sys
import exifread
import shlex # treat input between ""
from datetime import datetime
from PIL import Image as PilImage
from exif import Image as ExifImage

def parse_input(*args):
	
	if not args:
		print("\n📨 Error: No file has been sent.")
		return

	valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
	not_valid = []

	for input_file in args:

		if input_file.startswith(("'", '"')) and input_file.endswith(("'", '"')):
			input_file = input_file[1:-1]

		input_file = input_file.replace('\\ ', ' ')

		if (os.path.exists(input_file) == False):
			print(f'\n❌ The file {input_file} does not exist.')
			continue
		
		extension = extension = os.path.splitext(input_file)[1].lower()

		if extension not in valid_extensions:
			not_valid.append(input_file)
			continue

		stat_info = os.stat(input_file)
		date_creation = datetime.fromtimestamp(stat_info.st_birthtime).strftime('%Y-%m-%d %H:%M:%S')
		print(f"\n🗂️{input_file}:\nDate of creation: {date_creation}\n")

		try:
			image_file = open(input_file, 'rb')
			tags = exifread.process_file(image_file)
			for tag in tags.keys():
				print("%s, value %s" % (tag, tags[tag]))
		except IOError:
			print(f"The file {input_file} could not be opened.")

	if not not_valid:
		print('\n✅ All files are in the right format and have been treated!')
	else:
		print('\n🤖 Error: Some files are not in the right format and have been ignored: ')
		for file in not_valid:
			print(file)

processed_arguments = []
for arg in sys.argv[1:]:
	if arg.startswith(("'", '"')) and arg.endswith(("'", '"')):
	# Using shlex.split to treat correctly the paths between ""
		processed_arguments.extend(shlex.split(arg))
	else:
		processed_arguments.append(arg)

parse_input(*processed_arguments)