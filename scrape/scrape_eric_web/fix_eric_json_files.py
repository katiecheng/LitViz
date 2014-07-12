import os


for filename in os.listdir('eric_json_files'):

	file = open('eric_json_files/%s' %filename)
	text = file.read()

	new_file = open('eric_json_files_fixed/%s' %filename, 'a')
	new_file.write('{')
	for line in text:
		new_file.write(line)
	new_file.write("""
}""")