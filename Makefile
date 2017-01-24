install: contents.py
	cp contents.py ~/bin/

pep8.log: contents.py
	pep8 contents.py > pep8.log

pylint.log: contents.py
	pylint contents.py > pylint.log
