# === Top-level Makefile for Spellbinder ===

PYTHON := $(shell which python3.10)
VENV := venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

MODULES := spellbinder-util spellbinder-llm spellbinder-tools spellbinder-monolith

.PHONY: all setup update install test run clean reset doctor

all: setup

setup:
	@echo "⚙️ Creating virtual environment..."
	rm -rf $(VENV)
	$(PYTHON) -m venv $(VENV)
	$(MAKE) install

install:
	@test -x $(PIP) || (echo "❌ Virtualenv not found. Run 'make setup' first."; exit 1)
	@echo "📦 Installing all submodules in editable mode..."
	for mod in $(MODULES); do \
		echo "🔗 Installing $$mod..."; \
		$(PIP) install -e $$mod ; \
	done
	@echo "🧩 Installing runtime dependencies..."
	$(PIP) install fastapi uvicorn

update:
	@echo "⬆️ Upgrading pip..."
	$(PIP) install --upgrade pip

test:
	@echo "🧪 Running tests..."
	PYTHONPATH=. $(PY) -m pytest spellbinder-monolith/testing

run:
	@echo "🚀 Running FastAPI server..."
	$(PY) -m uvicorn spellbinder-monolith.web.app.main:app --reload

clean:
	@echo "🧹 Cleaning environment..."
	rm -rf $(VENV)
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete

reset: clean setup

doctor:
	@echo "🔍 Verifying editable installs..."
	for mod in $(MODULES); do \
		if [ ! -f "$$mod/pyproject.toml" ]; then \
			echo "❌ Missing pyproject.toml in $$mod"; \
		else \
			echo "✅ $$mod is present and ready"; \
		fi \
	done
