#!/usr/bin/env python3
import json
import pathlib
import re

DOCS_DIR = pathlib.Path("/home/kami/sentinel-docs/docs")
MKDOCS_YML = pathlib.Path("/home/kami/sentinel-docs/mkdocs.yml")


def extract_title(md_path: pathlib.Path) -> str:
    try:
        for line in md_path.read_text(encoding="utf-8", errors="ignore").splitlines()[:15]:
            s = line.strip()
            if s.startswith("# "):
                return s[2:].strip()
    except Exception:
        pass
    name = md_path.stem.replace("-", " ").replace("_", " ").strip()
    return name.title() if name else md_path.name


def build_tree(directory: pathlib.Path, indent: int) -> list[str]:
    lines = []
    pad = " " * indent
    entries = sorted(directory.iterdir(), key=lambda p: (not p.is_file(), p.name.lower()))

    # Put README.md or index.md first
    priority = [p for p in entries if p.is_file() and p.name.lower() in ("readme.md", "index.md")]
    others = [p for p in entries if p not in priority]

    for p in priority + others:
        if p.is_file() and p.suffix.lower() == ".md":
            rel = p.relative_to(DOCS_DIR).as_posix()
            title = "Overview" if p.name.lower() in ("readme.md", "index.md") else extract_title(p)
            lines.append(f"{pad}- {json.dumps(title, ensure_ascii=False)}: {json.dumps(rel, ensure_ascii=False)}")
        elif p.is_dir():
            sub_lines = build_tree(p, indent + 4)
            if sub_lines:
                folder_title = p.name.replace("-", " ").replace("_", " ").title()
                lines.append(f"{pad}- {json.dumps(folder_title, ensure_ascii=False)}:")
                lines.extend(sub_lines)
    return lines


def main():
    raw = MKDOCS_YML.read_text(encoding="utf-8")
    marker = "  - 8. Component Docs (Synced):"
    if marker not in raw:
        marker = "  - 8. Component Docs"
    base_cfg = raw.split(marker, 1)[0].rstrip() + "\n"

    comp_lines = build_tree(DOCS_DIR / "08-components", 6)
    arch_lines = build_tree(DOCS_DIR / "09-archive-business-and-research", 6)

    new_sections = [
        "  - 8. Component Docs (Consolidated):",
        *comp_lines,
        "  - 9. Business & Research Archive:",
        *arch_lines,
    ]
    MKDOCS_YML.write_text(base_cfg + "\n".join(new_sections) + "\n", encoding="utf-8")
    print(f"✓ Rebuilt mkdocs.yml navigation ({len(comp_lines) + len(arch_lines)} entries indexed).")


if __name__ == "__main__":
    main()
