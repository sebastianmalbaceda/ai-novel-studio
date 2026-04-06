# A.I. Novel Studio

## Build & Run

- Install deps: `pip install -r requirements.txt`
- Run researcher: `cd src && python researcher.py`
- Run writer: `cd src && python writer.py`
- Check syntax: `python -m py_compile src/utils.py && python -m py_compile src/researcher.py && python -m py_compile src/writer.py`
- Run tests: `python -m pytest tests/`

## Stack

Python 3.10+, requests, GitHub Actions (cron workflows), Any OpenAI-compatible API (configurable via config.json)

## Project Structure

```
src/              ← Python scripts (researcher, writer, utils)
data/             ← Runtime data (config, biblia, resúmenes, research log)
chapters/         ← Output: generated novel chapters (cap_XXX.md)
.github/workflows/← GitHub Actions cron jobs
docs/             ← Extended documentation
.agents/          ← AI agent skills, rules, config
```

## Conventions

- Language: Python source in English variable names, Spanish user-facing strings
- Files in `data/` use UTF-8 encoding with `ensure_ascii=False` for JSON
- Chapters follow `cap_XXX.md` naming (3-digit zero-padded)
- Config changes go in `data/config.json`, NEVER hardcoded in scripts
- All API calls go through `utils.call_ai_api()` — never call APIs directly
- Paths in scripts are relative from `src/` directory (e.g., `../data/config.json`)

## Git Workflow

- Branch: `feature/<short-description>`, `fix/<short-description>`, `docs/<short-description>`
- Commits: conventional commits format (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`)
- GitHub Actions bot uses: `github-actions[bot]` as author
- Automated commits use emoji prefixes: `🤖` (research), `📖` (chapters)

## Boundaries

### Always Do
- Read `data/config.json` for all dynamic parameters
- Use `utils.py` functions for API calls and config I/O
- Maintain UTF-8 encoding in all file operations
- Handle API errors gracefully (no raw exceptions to stdout)
- Keep the research_log.txt in append mode during research phase

### Ask First
- Before changing the API provider or endpoint URL
- Before modifying workflow cron schedules
- Before changing the Biblia (world rules) structure
- Before adding new Python dependencies

### Never Do
- Never commit API keys, tokens, or secrets to the repository
- Never hardcode API URLs or model names in scripts (use config.json)
- Never delete existing chapters in `chapters/`
- Never modify `data/research_log.txt` outside of the defined append/clear cycle
- Never push directly to `main` from local — let GitHub Actions handle it
- Never add `__pycache__/`, `.env`, or `venv/` to version control
