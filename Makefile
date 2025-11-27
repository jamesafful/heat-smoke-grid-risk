SHELL := /bin/bash

PY := python

.PHONY: setup test run-sample lint

setup:
	@echo 'No setup needed for stdlib sample.'

test:
	PYTHONPATH=. pytest -q


run-sample:
	$(PY) -m src.hsg.etl.build_panel_stdlib --sample
