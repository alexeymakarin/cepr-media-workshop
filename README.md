# CEPR Workshop on Media, Technology, Politics, and Society — Website

Institutional-memory website for the annual CEPR Workshop on Media, Technology,
Politics, and Society (co-chairs: Alexey Makarin and Andrea Prat). Live at:

**https://alexeymakarin.github.io/cepr-media-workshop/**

Plain HTML + CSS, no build step. Deployed with GitHub Pages from the `main`
branch. Each edition has one page under `editions/`, the official program PDFs
live in `files/`, and photos go in `photos/<year>/`.

## Updating the site

The easiest way is to open Claude Code in this folder and describe the change
("add the 2027 edition", "add these photos to 2026"). The step-by-step playbook
is in [CLAUDE.md](CLAUDE.md).

Two hard rules:

1. **Never commit spreadsheets or participant contact data.** The `.gitignore`
   blocks `.xlsx/.csv/.docx`; the public site shows names + affiliations only,
   never emails.
2. **All internal links must be relative** (`../assets/style.css`, not
   `/assets/style.css`) because the site is served from a `/cepr-media-workshop/`
   subpath.
