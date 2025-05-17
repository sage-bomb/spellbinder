PYTHON := $(shell which python3.10)
VENV := venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

MODULES := spellbinder-util spellbinder-llm spellbinder-tools spellbinder-monolith

.PHONY: all setup update install test run clean reset

all: setup

setup:
	@echo "⚙️ Creating virtual environment..."
	rm -rf $(VENV)
	$(PYTHON) -m venv $(VENV)
	$(MAKE) install

install:
	@echo "📦 Installing all submodules in editable mode..."
	for mod in $(MODULES); do \
		$(PIP) install -e ../$$mod ; \
	done

update:
	@echo "⬆️ Upgrading pip..."
	$(PIP) install --upgrade pip

test:
	@echo "🧪 Running tests..."
	PYTHONPATH=. $(PY) -m pytest testing

run:
	@echo "🚀 Running FastAPI server..."
	$(PY) -m uvicorn web.app.main:app --reload

clean:
	@echo "🧹 Cleaning environment..."
	rm -rf $(VENV)
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete

reset: clean setup
