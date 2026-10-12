#!/usr/bin/env python3
"""Validate independent ASM handbook content, routes and quiz integrity (stdlib)."""
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MANIFEST = json.loads((ROOT / "scripts" / "chapter_manifest.json").read_text(encoding="utf-8"))
QUIZZES = json.loads((DOCS / ".vitepress" / "quizzes.json").read_text(encoding="utf-8"))
ERRORS = []


def fail(msg):
    ERRORS.append(msg)


if len(MANIFEST) != 11 or len({ch["slug"] for ch in MANIFEST}) != 11:
    fail("Expected 11 distinct chapter slugs")

if set(QUIZZES) != {str(ch["id"]) for ch in MANIFEST}:
    fail("Quiz chapters do not match manifest")

for chapter in MANIFEST:
    path = DOCS / "chapters" / chapter["slug"]
    if not path.is_dir():
        fail(f"Missing chapter directory: {path}")
        continue
    for basename in ("index", "concepts", "examples", "workshop", "quiz"):
        page = path / f"{basename}.md"
        if not page.exists():
            fail(f"Missing page: {page.relative_to(ROOT)}")
            continue
        content = page.read_text(encoding="utf-8")
        if len(content) < 400:
            fail(f"Page too short: {page.relative_to(ROOT)}")
    questions = QUIZZES.get(str(chapter["id"]), [])
    if len(questions) != 5:
        fail(f"Chapter {chapter['id']} should have exactly 5 quiz questions")
    for n, question in enumerate(questions, start=1):
        if len(question.get("options", [])) != 4 or question.get("answer") not in range(4):
            fail(f"Invalid answer/options: chapter={chapter['id']} question={n}")
        if not question.get("why"):
            fail(f"Missing explanation: chapter={chapter['id']} question={n}")

# Validate absolute internal Markdown/VitePress links (no anchor/URL fetch required).
for page in DOCS.rglob("*.md"):
    content = page.read_text(encoding="utf-8")
    links = re.findall(r"\]\((/[^)#\s]+)(?:#[^)]*)?\)", content)
    links += re.findall(r'href="(/asm-handbook-th/[^\"]+)"', content)
    for href in links:
        url = unquote(href).split("?", 1)[0]
        if url.startswith("/asm-handbook-th/"):
            url = url[len("/asm-handbook-th/"):]
        else:
            url = url.lstrip("/")
        if url.endswith("/") or not Path(url).suffix:
            choices = [DOCS / url / "index.md", DOCS / (url.rstrip("/") + ".md")]
        elif url.endswith(".html"):
            choices = [DOCS / (url.removesuffix(".html") + ".md")]
        elif url.endswith(".md"):
            choices = [DOCS / url]
        else:
            choices = [DOCS / "public" / url]
        if not any(p.exists() for p in choices):
            fail(f"Broken internal link {href} in {page.relative_to(ROOT)}")

if ERRORS:
    print("\n".join("ERROR: " + e for e in ERRORS))
    raise SystemExit(f"Validation failed with {len(ERRORS)} errors")

pages = list(DOCS.rglob("*.md"))
print(f"Validation OK: {len(MANIFEST)} chapters, {len(pages)} Markdown pages, {sum(map(len, QUIZZES.values()))} quiz questions")
