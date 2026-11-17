# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Small Flask app for ranked-choice voting on books (Condorcet method), used by a book club as a **Telegram Mini App**. Voters open it from Telegram, the app identifies them from Telegram's signed `initData` (no typed name), they order a shuffled list of books (▲▼ arrows or drag) and submit. A bot in the club's group posts a "Votar" card, updates it as people vote and announces the winner. Deployed on PythonAnywhere at https://tupac.pythonanywhere.com. Code, comments, UI text and data keys are in Spanish — keep new code consistent with that. UI copy should read naturally (no `·` separators, no angle quotes).

## Commands

```bash
python -m venv venv && venv\Scripts\activate   # venv/ is gitignored
pip install -r requirements.txt                # only dependency: Flask (the bot uses urllib)
python run.py                                  # dev server with debug=True on http://127.0.0.1:5000
python -m app.configurar_bot                   # one-off: setWebhook, setMyCommands, setChatMenuButton
python app/voting_condorcet.py                 # print Condorcet result for app/data/data.txt (run from repo root)
python app/voting_irv.py                       # print Instant-Runoff result for the same data (run from repo root)
```

Tests live in `pruebas/` (plain scripts, no framework; run from repo root with the venv active). They work on temp copies of the data and never call Telegram:

```bash
python pruebas/probar_telegram.py   # routes, initData validation, bot commands (Bot API mocked), counting scripts
python pruebas/probar_flechas.py    # taps the ▲▼ arrows in headless Edge
python pruebas/vista_previa.py      # screenshots of every page, light and dark, into pruebas/capturas/ (gitignored)
```

There is no linter or build step. Outside Telegram `/` only shows "abrí desde Telegram"; to try the Mini App locally use a second (dev) bot whose Mini App URL points at a tunnel (`cloudflared tunnel --url http://localhost:5000`) and set `SITE_URL` to that tunnel.

## Architecture

- `run.py` → `app.create_app()` (app factory in `app/__init__.py`) → registers the single Blueprint `main` from `app/routes.py`. All routes live there.
- **Config and secrets** (`app/__init__.py`, via `_leer_secreto`: env var or gitignored file in `app/`): `SECRET_KEY`, `ADMIN_PASSWORD`, `BOT_TOKEN` (`bot_token.txt`), `BOT_USERNAME` (`bot_username.txt`), `TELEGRAM_WEBHOOK_SECRET` (`webhook_secret.txt`, auto-generated), `ADMIN_TELEGRAM_IDS` (`admin_ids.txt`, comma/newline separated; the bot's `/miid` tells you your id), `SITE_URL` (env only, defaults to the PythonAnywhere URL). `leer_config_telegram()` is shared with `configurar_bot.py`.
- **Identity** (`app/telegram_auth.py`): the client sends `Authorization: tma <initData>`; `usuario_de_request()` validates the HMAC with the bot token (24 h max age) and returns Telegram's `user` dict. Never trust `initDataUnsafe` on the server.
- **No database.** Persistence is flat files in `app/data/`; helpers in `app/votos.py` (`RUTA_VOTOS`, `RUTA_LIBROS`, `RUTA_ESTADO` are read at call time, so tests can repoint them):
  - `data.txt` (tracked in git) — the ballots, one line per vote:
    `Nombre: <telegram name> [tg:<user id>]; Lista: <python repr of list>; fecha: <YYYY-mm-dd HH:MM:SS>`.
    The `[tg:id]` marker is what enforces one vote per account. The counting parsers (duplicated in `voting_condorcet.get_condorcet_winner`, the `__main__` block of `voting_condorcet.py`, `voting_irv.py` and `kek.py`) split on `'; '` into exactly three parts and ignore the name, so names must never contain `; ` (`nombre_para_guardar` strips `;`, brackets and quotes). Titles containing `; ` or `', '` still break parsing.
  - `books.json` (tracked) — the candidate list, read via `Book.BooksDAO.load_books()` and fully overwritten by `/submit-book`.
  - `telegram.json` (gitignored) — bot state: `abierta` and the group card's `chat_id`/`message_id`. Missing file = voting open.
  - `winner.txt`, `winnerHistorico.txt` — not referenced by the code.
- **Bot** (`app/telegram_bot.py`): Bot API calls through `llamar()` (urllib, 5 s timeout, never raises). Telegram POSTs updates to `/telegram/webhook` (checked against `X-Telegram-Bot-Api-Secret-Token`). Commands: `/votacion` (admin, in the group: posts and pins the card, reopens voting), `/cerrar` (admin: closes, announces via `texto_anuncio`, edits the card), `/miid`, `/start` (private: `web_app` button). `web_app` buttons only work in private chats, so the group card uses a `url` button to `https://t.me/<bot>?startapp` (the Main Mini App, enabled in @BotFather).
- Routes:
  - `/` — the Mini App. `app/static/telegram.js` (loaded first in every page's body) sets up `window.App`: theme colors, `BackButton` via `<body data-volver>`, `MainButton` via `App.botonPrincipal`, `showAlert`/`showConfirm`, haptics and `fetchTelegram`.
  - `/sesion-telegram` (POST) — who the user is, their ballot if they already voted, whether voting is open, and whether they're an admin (if so it also sets `session['admin']`).
  - `/submit` (POST `{orderedList}`) — requires valid initData, open voting, exactly the titles in `books.json`, and no previous vote for that Telegram id; then appends the line and updates the group card.
  - `/books-manager` + `/submit-book`, `/votes` + `/submit-data`, full `/winner` — admin only (`session['admin']`, set by Telegram admin id or by `/login` with `ADMIN_PASSWORD`). Without admin, `/winner` shows only who voted (`winner_publico.html`).
- **Styling** (`app/static/styles.css`): Telegram Mini App look: colors only from `--tg-theme-*` variables (with light/dark fallbacks for plain browsers), grouped-list sections (`.seccion`, `.titulo-seccion`, `.pie-seccion`, `.celda`, `.enlaces`), system font, safe-area insets.
- `voting_condorcet.condorcet_winner` takes the candidate order from the **first ballot** and assumes every ballot ranks exactly the same set of candidates (a `KeyError` otherwise; `/submit` validates against `books.json` to prevent it). Fallback when there's no strict Condorcet winner: most pairwise wins, then tie-break by sum of pairwise votes. If that also ties it just picks the first one, so the announcement and `winner.html` use `telegram_bot.definir_ganador()`, which reports a tie instead.
- `routes.py` and `telegram_bot.py` use a `try: from app import ... except ImportError: import ...` fallback so modules can be imported both as a package and from inside `app/`.

## Known pitfalls

- Changing `books.json` while ballots exist makes old ballots disagree with the list; change books before `/votacion`, and clear `data.txt` (via `/votes`) to start a new vote.
- `voting_irv.py` and `kek.py` execute their file-reading code at import time using the relative path `app/data/data.txt`; don't import them from the web app.
- Because `app/data/data.txt` and `books.json` are tracked in git, pulling/deploying on PythonAnywhere can clobber live votes and books — check before committing changes to those files.
- The admin session cookie is `SameSite=Lax`, so it doesn't travel inside Telegram Web's iframe; there the admin should use the site in a normal tab. A Telegram admin's session lasts a year even if their id is removed from `admin_ids.txt` (`/logout` ends it).
- PythonAnywhere free accounts reach `api.telegram.org` through a proxy configured via environment variables; `urllib` honors them. Long polling isn't possible there (always-on tasks are paid) — the bot only works via the webhook.
