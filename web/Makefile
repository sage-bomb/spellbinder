.PHONY: install run clean

VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

install:
	@echo "Creating venv if not exists..."
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@echo "Installing requirements..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m uvicorn app.main:app --reload

clean:
	rm -rf $(VENV_DIR)
	rm -rf __pycache__ */__pycache__ .pytest_cache .mypy_cache .coverage coverage.xml htmlcov
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name ".DS_Store" -delete
