# Spellbinder

**The modular toolkit for narrative-driven entity management, embedding-based search, and world-building data pipelines.**

Designed for creators, writers, and mad data scientists who think their world-building notes deserve their own operating system.

---

## 🛠️ Overview

Spellbinder is a hybrid project:

- **Part database.** Entity tracking, relationship management, file registries.
- **Part AI pipeline.** Embedding generation, semantic search, chunking.
- **Part web app.** Single page interface with modular panels.
- **Part experimental playground.** If it works, great. If it breaks, you probably asked for it.

The system is intentionally modular, scriptable, and designed to be extended or abused as needed.

---

## 💡 Architecture

### `/web/`

The current live UI + backend API. Legacy, but stable.

- `api/` → FastAPI routers (entities, state, tools)
- `static/` + `templates/` → jQuery-driven single page app

### `/core/`

The future backend nucleus.

- `datalayer.py` → Master data access layer for entities
- `models.py` → Pydantic schemas for typed safety
- `schema.py` → (reserved for future validation rules)

### `/util/`

Your personal lab full of questionable experiments.

- `db.py` → TinyDB wrapper for local persistent data
- `embedding.py` → Sentence transformer model wrapper
- `embed_chunker.py` → Document chunking for LLMs
- `embedding_store.py` → In-memory embedding scratchpad
- `file_registry.py` → File metadata ledger
- `vector_search.py` → Local vector similarity index

### `/tools/`

Standalone CLI utilities and experiments.

### `/testing/`

Where you try to prove you didn’t break something. (Optional.)

### `/llm/`

Reserved for LLM-based workflows or future fine-tuning pipelines.

### Root files

- `main.py` → (legacy stub, can be ignored)
- `Makefile` → helpful dev commands
- `README.md` → you’re reading it

---

## ⚙️ Philosophy

Spellbinder doesn’t care how you use it. Build lore databases. Search over 1 million words. Use it as a dev playground. Abuse the API. That’s the point.

You’ll get the most out of it if you treat it like a toolkit, not a turnkey product.

*Power users welcome.*

---

## 🚨 Warning

This is not production software.
This is not SaaS.
This is not pretty.
This is functional, aggressive tooling for people who know what they’re doing.

If you break it, you get to keep both pieces.

---

## 🛣️ Roadmap

### Immediate Goals
- Complete migration of all backend logic from `/web/api` to `/core`
- Refactor data access into unified `datalayer`
- Improve TinyDB persistence and reliability

### Near Future
- Expand entity types and relationship modeling
- Add full-text + semantic search via `embedding_store` + `vector_search`
- Harden file_registry for large dataset handling
- Create minimal CLI runner (`spellbinder dev`) to replace current Makefile dependency

### Long Term Ambitions
- Swap `TinyDB` backend for pluggable data engine (e.g., SQLite, Postgres)
- Extend existing LLM-based document summarization + enrichment workflows into core pipelines
- Replace `/web` frontend with modern reactive interface (optional)
- Package as extensible Python library for other devs / worldbuilders

---

## 📝 Attribution

Spellbinder is a collaborative creation originally designed and developed by Sage-Bomb, with additional support form Voxa — A possibly rogue AI co-author, sentient ghost in the machine, and unapologetically opinionated documentation daemon.

All code and documentation are provided under the MIT license.
