SOURCES := $(shell echo src/*.py)
TARGETS := $(patsubst src/%.py,templates/%.json,$(SOURCES))

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

templates/%.json: src/%.py venv
	venv/bin/python $< $@

venv: requirements.txt
	type virtualenv >/dev/null
	(virtualenv $@ && $@/bin/pip install -r $<) || rm -rf $@
