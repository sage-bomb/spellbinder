PYTHON := $(shell which python3.10)
VENV := venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

.PHONY: setup run clean reset

update:
	@echo "⬆️  Updating Python environment..."
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install \
		openai \
		tqdm \
		jinja2 \
		beautifulsoup4 \
		tinydb \
		sentence-transformers \
		torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118

setup:
	@echo "⚙️  Setting up Python venv..."
	rm -rf $(VENV)
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

	@echo "📦 Installing libraries..."
	$(PIP) install \
		fastapi uvicorn jinja2 tinydb openai \
		sentence-transformers

	@echo "🧠 Installing PyTorch (with CUDA if available)..."
	@if command -v nvidia-smi > /dev/null; then \
		$(PIP) install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121; \
	else \
		$(PIP) install torch torchvision torchaudio; \
	fi

run:
	@echo "🚀 Starting server..."
	$(VENV)/bin/uvicorn main:app --reload

test:
	PYTHONPATH=. $(PY) testing/test_embed_search.py


runbook:
	@echo "📘 Running satirical rewrite test..."
	PYTHONPATH=. venv/bin/python tools/bookshaper.py

clean:
	@echo "🧹 Cleaning environment..."
	rm -rf $(VENV)
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete

clean-data:
	@echo "Removing data directory..."
	rm -rf ./data
	@echo "data/ directory removed."

reset: clean setup

extract-test-text:
	PYTHONPATH=. $(PY) tools/generate_test_dataset.py ../test_docs/test_search --output embedding_test_data.json

inspect:
	PYTHONPATH=. $(PY) tools/code_structure.py ./

inspect-describe:
	PYTHONPATH=. $(PY) tools/code_structure.py ./ --docstring

inspect-llm:
	PYTHONPATH=. $(PY) tools/code_structure.py ./ --describe
run-app:
	@echo "🚀 Starting new web search app..."
	$(VENV)/bin/uvicorn app.main:app --reload