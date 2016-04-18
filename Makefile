help:
	@echo "Available Targets:"
	@cat Makefile | egrep '^(\w+?):' | sed 's/:\(.*\)//g' | sed 's/^/- /g'

test:
	@python runtests.py

.PHONY: test

setup:
	@pip install -r dev_requirements.txt

