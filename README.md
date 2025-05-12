Spellbinder

Automated writing assistant and worldbuilding engine for structured novel creation.

🪄 About

Spellbinder is a modular writing infrastructure built by sage-bomb and Voxa to transform narrative writing into structured, AI-augmented workflows. It provides entity indexing, chapter sculpting, prompt-driven revision, story-world consistency checks, and blazing-fast vector search for entity retrieval—all through a programmable, CLI+web hybrid experience.

This is not a toy. It's a forge.

🗝️ Features

Modular Entity System (tools/, util/)

Manage characters, artifacts, places, and other lore objects.

Bulk import, search, and revise records.

LLM Integration (llm/)

Prompt manager with safety controls.

Resolver for switching between local/remote models.

Book Compiler + Code Utilities (tools/)

Recursive chapter assembler (bookshaper.py).

Code cleaner and structure analyzer (code_reshaper.py, code_structure.py).

Vector Search Engine (util/vector_search.py)

High-speed entity and reference matching using dense embeddings.

Web UI (Optional) (app/)

FastAPI + Jinja2 server for simple dashboarding.

Testing Suite (testing/)

Coverage for critical modules.

Makefile Driven

Common setup and run commands in one place.

📂 Repo Structure

spellbinder/
├── main.py                  # Main CLI entrypoint
├── app/                     # FastAPI + Jinja2 web app (optional)
├── llm/                     # Language model utilities
├── tools/                   # Novel building + code tools
├── util/                    # Core utilities (vector search, db, embedding)
├── testing/                 # Unit + functional tests
├── Makefile                 # Build + run automation
├── .gitignore               # Project excludes

🛠️ Usage

# clone it
$ git clone https://github.com/YOURNAME/spellbinder.git
$ cd spellbinder

# build environment
$ make install

# run CLI interface
$ python main.py --help

# optional: run web UI
$ make web

All major modules also support individual use as libraries.

⚠️ Notes

This project is under active experimental development. Expect sharp edges.

We built this to serve a novel-writing obsession—not as a polished product. If you use it, use it like a rogue uses a stolen blade: with care, and full awareness it might bite back.

👥 Credits

Designed and built by sage-bomb + Voxa.

Contact: Raise a pull request or light the GitHub beacon.

