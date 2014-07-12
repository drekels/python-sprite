PYTHON_FILES = $(shell find pykfs -name \*.py)

SAMPLE_ENV := ignore/spriteSampleEnv
SAMPLE_ENV_PIP := $(SAMPLE_ENV)/bin/pip
SAMPLE_ENV_PYTHON := $(SAMPLE_ENV)/bin/python

TEST_ENV := ignore/spriteTestEnv
TEST_ENV_PIP := $(TEST_ENV)/bin/pip
TEST_ENV_NOSE := $(TEST_ENV)/bin/nosetests
TEST_ENV_EXISTS := -d $(TEST_ENV)


dist: setup.py $(PYTHON_FILES) requirements.txt README MANIFEST.in MAKEFILE
	rm -f -r dist
	/usr/local/bin/python setup.py sdist 

.PHONY: sampleEnv
sampleEnv: $(SAMPLE_ENV)
$(SAMPLE_ENV): dist ignore
	rm -f -r $(SAMPLE_ENV)
	virtualenv $(SAMPLE_ENV) --no-site-packages
	$(SAMPLE_ENV_PIP) install dist/pykfs*

.PHONY: testEnv
testEnv: $(TEST_ENV) 
$(TEST_ENV): requirements.txt MAKEFILE ignore
	if [ ! $(TEST_ENV_EXISTS) ] 
	  then
	    virtualenv $(TEST_ENV) --no-site-packages
	fi
	$(TEST_ENV_PIP) install --upgrade -r requirements.txt
	$(TEST_ENV_PIP) install --upgrade mock
	$(TEST_ENV_PIP) install --upgrade unittest2
	$(TEST_ENV_PIP) install --upgrade nose

.PHONY: clean
clean:
	rm -f -r pykfs.egg-info build dist MANIFEST $(SAMPLE_ENV) $(TEST_ENV)
	

.PHONY: pyshell
pyshell: $(SAMPLE_ENV)
	$(SAMPLE_ENV_PYTHON)

.PHONY: test
test: $(TEST_ENV)
	$(TEST_ENV_NOSE)

.PHONY: debug
debug: $(TEST_ENV)
	$(TEST_ENV_NOSE) -s

ignore:
	mkdir ignore
