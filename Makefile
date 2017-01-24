install: contents.py
	cp contents.py ~/bin/

pep8: contents.py
	pep8 contents.py > pep8.log

lint: contents.py
	pylint contents.py > pylint.log
