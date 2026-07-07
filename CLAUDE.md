# Claude Working Notes — CEPR Media Workshop Website

Public website for the CEPR Workshop on Media, Technology, Politics, and
Society. Live at **https://alexeymakarin.github.io/cepr-media-workshop/**
(GitHub Pages, repo `alexeymakarin/cepr-media-workshop`, deploys from `main`
branch root automatically on push — allow 1–2 minutes).

This working copy lives inside Dropbox at
`/mnt/c/Users/makarin/Dropbox (Personal)/Conferences and Seminars/CEPR Media Workshop/Website/`,
next to the per-edition source folders (programs, spreadsheets): `../<year> CEPR ... Workshop/`.
Two settings make git safe here: the `.git` folder carries the
`com.dropbox.ignored` attribute so Dropbox does not sync it (Dropbox syncing
git internals corrupts repos — GitHub is the backup), and `core.filemode` is
off because NTFS reports every file as executable. If the repo ever looks
broken: re-clone from GitHub into this location and re-apply both settings.

## Hard rules

1. **Privacy — this repo is public and its history is forever.**
   - Participant listings show **name + affiliation only**. Never emails, phone
     numbers, hotel/rooming, dietary, travel, or payment information.
   - Never commit `.xlsx/.xls/.csv/.tsv/.docx` (gitignored as belt-and-braces).
   - Extract participant data with `tools/extract_participants.py` (prints
     name + affiliation to stdout only, aborts if output contains `@`).
   - Before every push run the audit greps (see below).
2. **All internal links must be relative** (`../assets/style.css`, never
   `/assets/style.css`). The site is served from the `/cepr-media-workshop/`
   subpath, so absolute paths work locally but 404 in production.
3. Program pages are faithful transcriptions of the official PDF programs.
   Fix only obvious typos (missing diacritics, impossible times) and flag every
   such fix to the user.

## Annual update playbook (new edition YYYY)

1. Copy `tools/edition-template.html` → `editions/YYYY.html`.
2. Extract the program text: `tools/extract_program.sh "<program.pdf>" > /tmp/program.txt`
   (strips the zero-width characters that Google-Docs PDFs contain), transcribe
   into the page, then verify names/titles line by line against the PDF —
   diacritics are the known failure mode (Strömberg, Cagé, Padró i Miquel,
   Jiménez-Durán, Szűcs, Ro’ee).
3. Copy the official PDF to `files/program-YYYY.pdf`.
4. Participants: `python3 tools/extract_participants.py <attendees.xlsx>
   --name-col Name --aff-col Affiliation [--status-col Status]` (drops
   declined/cancelled rows), clean typos, sort by surname, insert as
   `<li>Name <span class="aff">— Affiliation</span></li>`.
5. `mkdir photos/YYYY && touch photos/YYYY/.gitkeep`.
6. Add the YYYY nav link on **every** page: `index.html`, `committee.html`,
   all `editions/*.html`.
7. `index.html`: add an edition card, update the next-edition banner, and
   update any counts in the prose.
8. `committee.html`: refresh the scientific committee if it changed.
9. Run the checks below, get user approval on the participant list, push.

## Adding photos

Drop files in `photos/<year>/` (JPEG, reasonable web size — resize if >500 KB:
`mogrify -resize 1600x1600\> -quality 82 photos/<year>/*.jpg`), then in that
edition's Photos section remove the `coming-soon` paragraph (if present) and
add one line per photo:
`<figure><a href="../photos/<year>/01.jpg"><img src="../photos/<year>/01.jpg" alt="..." loading="lazy"></a></figure>`

## Checks before any push

```bash
# 1. No emails in HTML (must print nothing)
grep -rEn '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' --include='*.html' .
# 2. No logistics strings (review any hit; "Newsroom" in a paper title is a known false positive)
grep -rinE 'hotel|room(ing)?|payment|reimburs|invoice|dietary|€[0-9]|phone' --include='*.html' .
# 3. No data files tracked (must print nothing)
git ls-files | grep -iE '\.(xlsx?|csv|tsv|docx)$'
# 4. Local link check + preview
python3 -m http.server 8877 --directory . &   # then browse / screenshot
```

After pushing, verify https://alexeymakarin.github.io/cepr-media-workshop/
loads and spot-check the new page.

## Design notes

Single stylesheet `assets/style.css`. Editorial-academic look: warm paper
background, Palatino-family system serif, accent blue `#191988` (the color of
the printed program titles — keep this constant across years). No JavaScript,
no webfonts, no build step; keep it that way unless the user asks otherwise.
Breaks use `session break`, keynotes/round tables use `session special` with a
`<span class="kind">` label.

## Known gaps / pending

- 2023 and 2025 pages list program participants only; full attendee lists
  requested from EIEF (Susana) and the 2025 Bocconi organizers. Swap in when
  they arrive (keep the "Affiliations as of <month year>" note).
- No photos yet for any edition; galleries show a "coming soon" placeholder.
- 2027 (5th edition, Bocconi Milan, June 24–25): dates are on the index banner;
  add the call for papers link when it exists.
- Wording: Makarin and Prat are described as workshop **co-founders** on the
  site (not "co-chairs") — organization rotates to the host institution each
  year, and Bocconi leads the Milan editions. Keep this phrasing. The
  "(co-chair)" tags inside the Scientific Committee list are from the official
  2026 program (they co-chair the SC specifically) and are fine.
- 2023: the Tinder paper (Xiong) was presented by Makarin because Xiong could
  not attend — the page notes this; Xiong is deliberately absent from the 2023
  participants list.
