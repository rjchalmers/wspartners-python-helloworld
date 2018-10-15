.PHONY: all source release local run-local test deploy

# PLEASE CHANGE THE COMPONENT NAME
COMPONENT="wspartners-sandbox-python-helloworld"

all: test local

src/ext: src/requirements.txt
	# Download any PyPI packages listed in src/requirements.txt to the
	# src/ext folder.  The extra shell commands catch any errors and ensure
	# the src/ext folder is not left in a partially complete state.
	( mkdir -p $@ && pip install --download $@ --requirement $< ) || ( rm -rf $@; exit 1 )

source: src/ext
	# Bundle up all the source code into a single .tar.gz file, used in
	# combination with the .spec file to create the RPM(s)
	mkdir -p SOURCES/
	tar --exclude ".svn" --exclude ".*.sw?" --exclude "*.py[co]" -czf SOURCES/src.tar.gz src/

release: source
	# Clean out any old RPMs from previous builds
	rm -rf SRPMS RPMS
	# Build the package in an fresh CentOS 7 build environment, containing
	# just the RPMs listed as build dependencies in the .spec file.  See
	# https://github.com/bbc/bbc-mock-tools for more information.  Also
	# adds an extra part to the version string containing an
	# auto-incrementing build number.
	mock-build --os 7 --define "buildnum $(shell cosmos-release generate-version $(wspartners-sandbox-python-helloworld))"
	# Send the RPM and other release metadata to Cosmos.  See
	# https://github.com/bbc/cosmos-release/ for more information
	cosmos-release service $(wspartners-sandbox-python-helloworld) RPMS/*.rpm

local: source
	# Build the RPMs locally, without any interaction with the Cosmos component
	rm -rf SRPMS RPMS
	mock-build --os 7

venv/%: %/requirements.txt
	type virtualenv >/dev/null
	(virtualenv $@ && $@/bin/pip install -r $<) || rm -rf $@

run-local: venv/src
	PYTHONPATH=src/ venv/src/bin/python -m helloworld.server

test: venv/test
	venv/test/bin/nosetests -v test/

deploy_int:
	cosmos deploy $(wspartners-sandbox-python-helloworld) int -f
	cosmos deploy-progress $(wspartners-sandbox-python-helloworld) int
