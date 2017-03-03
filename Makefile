#% define variables
##% user set variables
modul := excerpts
postfix := _o
TEST_FILE := tests/files/some_file.txt

##% derived variables
SOURCE := $(shell find ${modul} -type f -name "*.py")


#% make targets
all: doc analyse package run testing tests 

##% installation
install:
	 pip3 install . --upgrade --user

##% cli
cli:
	~/.local/bin/${modul} tests/files/some_file.txt -o _cli -O output \
		-p --formats html

##% testpypi
.PHONY: testpypi
testpypi: package
	python setup.py register -r https://testpypi.python.org/pypi
	twine upload dist/* -r testpypi

##% packaging
package: dist build

dist: ${SOURCE} ./setup.py
	python3 ./setup.py sdist

build: ${SOURCE} ./setup.py
	python3 setup.py bdist_wheel

##% testing
testing: log/unittest.log log/coverage.log 
log/unittest.log: tests/test_basic.py ${SOURCE}
	python3 ./tests/test_basic.py > log/unittest.log 2>&1
log/coverage.log: tests/test_basic.py ${SOURCE}
	python3-coverage run tests/test_basic.py
	python3-coverage report -m > log/coverage.log
	python3-coverage html

tests: tests/files/glm.md tests/files/phy.md
tests/files/glm.md:
	./bin/${modul} -c '#' -m '%' tests/files/glm.R

tests/files/phy.md: 
	./bin/${modul} -c '///' -m '%' tests/files/phy.c
##%  analyse code
analyse: log/pep8.log log/pylint.log

log/pep8.log: ${SOURCE}
	pep8 ./${modul}/ > ./log/pep8.log || true

log/pylint.log: ${SOURCE}
	pylint ./${modul}/ > ./log/pylint.log || true

##% create documentation
doc: ./docs/${modul}.html ./docs/doxygen doxy_code

docs/${modul}.html: ${SOURCE}
	./utils/pydoc.cl


docs/doxygen: ${SOURCE} .doxygen.conf
	rm -rf docs/doxygen || true
	mkdir docs/ || true
	doxygen .doxygen.conf > ./log/doxygen.log 2>&1 
	! grep "warning:" ./log/doxygen.log 

.PHONY: doxy_code
doxy_code: ${SOURCE}
	./utils/doxygenize.cl 

##% maintenance
init:
	pip3 install --user -r requirements.txt

##% utils
run: install
	python3 ./utils/run.py
