#% define variables
##% user set variables
modul := contents
postfix = _o

##% derived variables
file := ${modul}.py


#% make targets
all: doc analyse package main run

##% installation
install:
	 pip3 install . --upgrade --user

##% main
main: output/${modul}${postfix}.html output/${modul}${postfix}.md
output/${modul}${postfix}.html: ./${modul}/${file} 
	./bin/${modul} ./${modul}/${file} --pandoc --postfix ${postfix} \
		--formats html; mv ./${modul}/${modul}${postfix}.html ./output/ ;\
		rm ./${modul}/${modul}${postfix}.*

output/${modul}${postfix}.md: ./${modul}/${file} 
	./bin/${modul} ./${modul}/${file} --postfix ${postfix} ;\
		mv ./${modul}/${modul}${postfix}.md ./output/

##% packaging
package: dist build

dist: ./${modul}/${file} ./setup.py
	python3 ./setup.py sdist

build: ./${modul}/${file} ./setup.py
	python3 setup.py bdist_wheel
##%  analyse code
analyse: log/pep8.log log/pylint.log

log/pep8.log: ./${modul}/${file}
	pep8 ./${modul}/${file} > ./log/pep8.log || true

log/pylint.log: ./${modul}/${file}
	pylint --disable=missing-docstring ./${modul}/${file} \
		> ./log/pylint.log || true

##% create documentation
doc: ./docs/${modul}.html ./docs/doxygen

docs/${modul}.html: ./${modul}/${file}
	python3 -m pydoc -w ${modul}/${file}; mv ${modul}.html ./docs/

docs/doxygen: ./${modul}/${file} .doxygen.conf
	mkdir docs/ || true
	ln -s ./${modul}/${file} . ## create a link to run doxygen in .
	doxygen .doxygen.conf > ./log/doxygen.log 2>&1 
	rm ${file}
	! grep "warning:" ./log/doxygen.log 

##% maintenance
init:
	pip3 install --user -r requirements.txt

##% utils
run: install
	python3 ./utils/run.py
