#% define variables
##% user set variables
modul := contents
postfix = _o

##% derived variables
file := ${modul}.py


#% make targets
all: doc analyse ${modul}${postfix}.pdf 

##% main
${modul}${postfix}.pdf: ${file} install
	${file} ${file} --pandoc --postfix ${postfix}

${modul}${postfix}.md: ${file} install
	${file} ${file} --postfix ${postfix}

install: ${file}
	cp ${file} ~/bin/

##%  analyse code
analyse: pep8.log pylint.log

pep8.log: ${file}
	pep8 ${file} > pep8.log || true

pylint.log: ${file}
	pylint ${file} > pylint.log || true

##% create documentation
doc: ${modul}.html doxygen

${modul}.html: ${file}
	python3 -m pydoc -w ${modul}

doxygen: ${file}
	doxygen .doxygen.conf > doxygen.log 2>&1 
	! grep "warning:" doxygen.log 
