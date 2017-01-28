#% define variables
##% user set variables
modul := contents
postfix = _o

##% derived variables
file := ${modul}.py


#% make targets
all: doc analyse output/${modul}${postfix}.html 

##% main
output/${modul}${postfix}.html: ./${modul}/${file} install
	./${modul}/${file} ./${modul}/${file} --pandoc --postfix ${postfix} \
		--formats html; mv ./${modul}/${modul}${postfix}.html ./output/ ;\
		rm ./${modul}/${modul}${postfix}.*

output/${modul}${postfix}.md: ./${modul}/${file} install
	./${modul}/${file} ./${modul}/${file} --postfix ${postfix} ;\
		mv ./${modul}/${modul}${postfix}.md ./output/

install: ./${modul}/${file}
	cp ./${modul}/${file} ~/bin/

##%  analyse code
analyse: log/pep8.log log/pylint.log

log/pep8.log: ./${modul}/${file}
	pep8 ./${modul}/${file} > ./log/pep8.log || true

log/pylint.log: ./${modul}/${file}
	pylint ./${modul}/${file} > ./log/pylint.log || true

##% create documentation
doc: ${modul}.html ./docs/doxygen

log/${modul}.html: ./${modul}/${file}
	python3 -m pydoc -w ${modul}; mv ${modul}.html ./output/

docs/doxygen: ./${modul}/${file}
	doxygen .doxygen.conf > ./log/doxygen.log 2>&1 
	! grep "warning:" ./log/doxygen.log 

##% maintenance
init:
	pip install -r requirements.txt

