#% define variables
##% user set variables
modul := contents

##% derived variables
file := ${modul}.py

#% make targets
install: ${file}
	cp ${file} ~/bin/

##%  analyse code
pep8.log: ${file}
	pep8 ${file} > pep8.log

pylint.log: ${file}
	pylint ${file} > pylint.log

##% create documentation
contents.html: ${file}
	python3 -m pydoc -w ${modul}
