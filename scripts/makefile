# SETTINGS
.PHONY: clear makefile-info type-status howtorelease-status changelog-status setup-status coverage-status all-status
SHELL := /bin/bash
ROOT_DIR := $(shell cd .. && pwd)
MODULE_NAME = "nwshared"
MODULE_VERSION = "1.8.0"
COVERAGE_THRESHOLD = 70

# TARGETS
clear:
	@clear
makefile-info:
	@echo "MODULE_NAME: $(MODULE_NAME)"; \
	echo "MODULE_VERSION: $(MODULE_VERSION)"; \
	echo "COVERAGE_THRESHOLD: $(COVERAGE_THRESHOLD)%"
type-status:
	@value=$$(mypy $(ROOT_DIR)/src/$(MODULE_NAME).py | grep -c "error:"); \
	if [ $$value -eq 0 ]; then echo "[OK] $@: passed!"; else echo "[WARNING] $@: not passed! '$$value' error(s) found!"; fi;
howtorelease-status:
	@value=$$(cat $(ROOT_DIR)/docs/docs-$(MODULE_NAME).md | grep -c "\`v$(MODULE_VERSION)\`;\|$(MODULE_VERSION)#egg"); \
	if [ $$value -eq 2 ]; then echo "[OK] $@: 'How-to Release' updated to current version!"; else echo "[WARNING] $@: 'How-to Release' not updated to current version!"; fi;
changelog-status:
	@value=$$(cat $(ROOT_DIR)/CHANGELOG | grep -c "v$(MODULE_VERSION)$$"); \
	if [ $$value -eq 1 ]; then echo "[OK] $@: 'CHANGELOG' updated to current version!"; else echo "[WARNING] $@: 'CHANGELOG' not updated to current version!"; fi;
setup-status:
	@value=$$(cat $(ROOT_DIR)/src/setup.py | grep -oP 'MODULE_VERSION\s*:\s*str\s*=\s*"v\K[\d.]+'); \
	if [ $$value == "$(MODULE_VERSION)" ]; then echo "[OK] $@: 'setup.py' updated to current version!"; else echo "[WARNING] $@: 'setup.py' not updated to current version!"; fi;
coverage-status:
	@cd $(ROOT_DIR)/tests/; \
	coverage run -m unittest $(MODULE_NAME)tests.py > /dev/null 2>&1; \
	value=$$(coverage report --omit=$(MODULE_NAME)tests.py | grep -oP 'TOTAL\s+\d+\s+\d+\s+\K\d+(?=%)'); \
	if [ $$value -ge $(COVERAGE_THRESHOLD) ]; then echo "[OK] $@: unit test coverage >= $(COVERAGE_THRESHOLD)%."; else echo "[WARNING] $@: unit test coverage < $(COVERAGE_THRESHOLD)%."; fi;
coverage-detailed:
	@cd $(ROOT_DIR)/tests/; \
	coverage run -m unittest $(MODULE_NAME)tests.py > /dev/null 2>&1; \
	rm -rf htmlcov; \
	coverage html --omit=$(MODULE_NAME)tests.py && sed -n '/<table class="index" data-sortable>/,/<\/table>/p' htmlcov/class_index.html | pandoc --from html --to plain; \
	sleep 3; \
	rm -rf htmlcov;

# AGGREGATE TARGETS
all-status: clear makefile-info type-status howtorelease-status changelog-status setup-status coverage-status
