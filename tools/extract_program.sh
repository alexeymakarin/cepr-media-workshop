#!/usr/bin/env bash
# Extract a workshop program PDF to plain text for transcription into an
# edition page. Strips zero-width spaces (Google-Docs PDFs are full of them).
# Usage: tools/extract_program.sh "path/to/Program 2027.pdf" > /tmp/program.txt
set -euo pipefail
pdftotext -layout "$1" - | perl -CSD -pe 's/\x{200b}//g'
