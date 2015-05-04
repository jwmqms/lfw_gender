# Native imports
import os

# Project name
doc_name = 'lfw'

# Extensions to ignore and working directory to use
ignore_list = set(['py', 'bib', 'pdf', 'tex', 'sty', 'gitignore'])
cwd         = os.getcwd()

# List of files to delete
delete_list = [f for f in os.listdir(cwd)
	if os.path.isfile(os.path.join(cwd, f)) and
	f.split('.')[-1] not in ignore_list]

# Delete the files
for f in delete_list: os.remove(f)

# Build process for latex
print '\n###################################################################' \
	'############\n##### Build the document\n###############################' \
	'###############################################\n\n'
os.system('pdflatex ' + doc_name)
os.system('pdflatex ' + doc_name)

print '\n###################################################################' \
	'############\n##### Add the citations\n################################' \
	'###############################################\n\n'
os.system('bibtex ' + doc_name)

print '\n###################################################################' \
	'############\n##### Build the document\n###############################' \
	'###############################################\n\n'
os.system('pdflatex ' + doc_name)

print '\n###################################################################' \
	'############\n##### Finalize the document\n############################' \
	'###################################################\n\n'
os.system('pdflatex ' + doc_name)