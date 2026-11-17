# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Small Flask app for ranked-choice voting on books (Condorcet method). Users drag-and-drop a shuffled list of books into their preferred order and submit it under their name; `/winner` computes the Condorcet result. Deployed on PythonAnywhere at https://tupac.pythonanywhere.com. Code, comments, UI text and data keys are in Spanish — keep new code consistent with that.

## Commands

```bash
python -m venv venv && venv\Scripts\activate   # venv/ is gitignored
pip install -r requirements.txt                # only dependency: Flask
python run.py                                  # dev server with debug=True on http://127.0.0.1:5000
python app/voting_condorcet.py                 # print Condorcet result for app/data/data.txt (run from repo root)
python app/voting_irv.py                       # print Instant-Runoff result for the same data (run from repo root)
```

There are no tests, linter or build step.

## Architecture

- `run.py` → `app.create_app()` (app factory in `app/__init__.py`) → registers the single Blueprint `main` from `app/routes.py`. All routes live there.
- **No database.** Persistence is flat files in `app/data/`, which are committed to git:
  - `data.txt` — the ballots. One line per vote, written by `/submit`, in the exact format
    `Nombre: <name>; Lista: <python repr of list>; fecha: <YYYY-mm-dd HH:MM:SS>`.
    The parser (duplicated in `voting_condorcet.get_condorcet_winner`, the `__main__` block of `voting_condorcet.py`, `voting_irv.py` and `kek.py`) splits on `'; '` and `"', '"` and strips quotes, so changing the write format in `routes.submit` breaks all of them. Titles containing `; ` or `', '` will also break parsing.
  - `books.json` — the candidate list, read via `Book.BooksDAO.load_books()` and fully overwritten by `/submit-book` (the books-manager page sends the whole list each save).
  - `winner.txt`, `winnerHistorico.txt` — not referenced by the code.
- Routes:
  - `/` (index) — shuffled books, SortableJS drag list, POSTs `{name, orderedList}` to `/submit`.
  - `/submit` — rejects a vote if the name string appears *anywhere* in `data.txt` (substring check). The name `kek` is a test name: it returns success without saving.
  - `/books-manager` + `/submit-book` — edit the candidate list.
  - `/votes` + `/submit-data` — raw editor for `data.txt`; overwrites the whole file. "Protected" only by a client-side `prompt()` compared against a hardcoded password passed into the template.
  - `/winner` — `get_condorcet_winner(data.txt)` returns a dict (`candidatos`, `get_votes` pairwise matrix, `half`, `ganador_condorcet`, `respuesta_escrita`, `tabla_enfrentamientos`) consumed by `winner.html`, which colors matrix cells by comparing against `half`.
- `voting_condorcet.condorcet_winner` takes the candidate order from the **first ballot** and assumes every ballot ranks exactly the same set of candidates (a `KeyError` otherwise). Fallback when there's no strict Condorcet winner: most pairwise wins, then tie-break by sum of pairwise votes.
- `routes.py` has a `try: from app import ... except ImportError: import ...` fallback so modules can be imported both as a package and from inside `app/`.

## Known pitfalls

- `/winner` raises `IndexError` when `data.txt` is empty (`ballots[0]`).
- In `condorcet_winner`, the branch with a unique max-wins candidate and `max_wins > half` returns the `respuesta` **string** instead of the `resultado` dict, which breaks `winner.html`.
- `voting_irv.py` and `kek.py` execute their file-reading code at import time using the relative path `app/data/data.txt`; don't import them from the web app.
- Because `app/data/` is tracked in git, pulling/deploying on PythonAnywhere can clobber live votes and books — check before committing changes to those files.
