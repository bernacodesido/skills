#!/usr/bin/env python3
"""
Validates skill folders against the Claude Skills specification.

Rules enforced:
  - Folder names must be kebab-case and must not contain 'claude' or 'anthropic'
  - Each skill folder must contain exactly SKILL.md (case-sensitive)
  - No README.md allowed inside a skill folder
  - SKILL.md must have valid YAML frontmatter (--- delimiters, parseable YAML)
  - frontmatter: 'name' required, kebab-case, must match folder name
  - frontmatter: 'description' required, <1024 chars, no XML tags
  - frontmatter: no XML tags anywhere
  - frontmatter: 'compatibility' if present must be 1-500 chars
  - SKILL.md body should contain at least one ## section heading (warning)
"""

import os
import re
import sys

import yaml

KEBAB_RE = re.compile(r"^[a-z][a-z0-9-]*$")
XML_RE = re.compile(r"<[a-zA-Z/!]")
RESERVED = ("claude", "anthropic")

# Directories at repo root that are not skills
SKIP = {"_template", ".github", ".git", ".claude", "node_modules"}


def scan_wrong_casing(folder_path: str) -> list[str]:
    """Return any SKILL.md variants with wrong casing."""
    wrong = []
    for entry in os.scandir(folder_path):
        if entry.name.lower() == "skill.md" and entry.name != "SKILL.md":
            wrong.append(entry.name)
    return wrong


def parse_frontmatter(content: str) -> tuple[str, str] | None:
    """Return (frontmatter_str, body) or None if malformed."""
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    return parts[1], parts[2]


def validate_skill(folder_name: str, folder_path: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    prefix = f"{folder_name}"

    # --- Folder naming ---
    if not KEBAB_RE.match(folder_name):
        errors.append(
            f"{prefix}: folder name must be kebab-case "
            f"(lowercase letters and hyphens only), got '{folder_name}'"
        )

    for word in RESERVED:
        if word in folder_name.lower():
            errors.append(
                f"{prefix}: folder name must not contain '{word}' (reserved by Anthropic)"
            )

    # --- Wrong-cased SKILL.md variants ---
    for wrong in scan_wrong_casing(folder_path):
        errors.append(
            f"{prefix}/{wrong}: file must be named exactly 'SKILL.md' (case-sensitive)"
        )

    # --- SKILL.md presence ---
    skill_md = os.path.join(folder_path, "SKILL.md")
    if not os.path.isfile(skill_md):
        errors.append(f"{prefix}: missing required SKILL.md file")
        return errors, warnings  # can't validate contents

    # --- No README.md inside skill folder ---
    if os.path.isfile(os.path.join(folder_path, "README.md")):
        errors.append(
            f"{prefix}/README.md: README.md is not allowed inside a skill folder; "
            "use SKILL.md or references/ instead"
        )

    # --- Parse SKILL.md ---
    with open(skill_md, encoding="utf-8") as f:
        content = f.read()

    parsed = parse_frontmatter(content)
    if parsed is None:
        errors.append(
            f"{prefix}/SKILL.md: missing or malformed YAML frontmatter "
            "(file must start with ---)"
        )
        return errors, warnings

    fm_str, body = parsed

    # --- XML tags anywhere in frontmatter ---
    if XML_RE.search(fm_str):
        errors.append(
            f"{prefix}/SKILL.md: frontmatter contains forbidden XML angle brackets (< or >)"
        )

    try:
        fm = yaml.safe_load(fm_str)
    except yaml.YAMLError as exc:
        errors.append(f"{prefix}/SKILL.md: invalid YAML frontmatter — {exc}")
        return errors, warnings

    if not isinstance(fm, dict):
        errors.append(f"{prefix}/SKILL.md: frontmatter must be a YAML mapping")
        return errors, warnings

    # --- name field ---
    if "name" not in fm:
        errors.append(f"{prefix}/SKILL.md: frontmatter missing required 'name' field")
    else:
        name = fm["name"]
        if not isinstance(name, str):
            errors.append(f"{prefix}/SKILL.md: 'name' must be a string")
        else:
            if not KEBAB_RE.match(name):
                errors.append(
                    f"{prefix}/SKILL.md: 'name' must be kebab-case, got '{name}'"
                )
            if name != folder_name:
                errors.append(
                    f"{prefix}/SKILL.md: 'name' value ('{name}') "
                    f"must match the folder name ('{folder_name}')"
                )

    # --- description field ---
    if "description" not in fm:
        errors.append(
            f"{prefix}/SKILL.md: frontmatter missing required 'description' field"
        )
    else:
        desc = fm["description"]
        if not isinstance(desc, str):
            errors.append(f"{prefix}/SKILL.md: 'description' must be a string")
        else:
            desc = desc.strip()
            if not desc:
                errors.append(f"{prefix}/SKILL.md: 'description' is empty")
            if len(desc) > 1024:
                errors.append(
                    f"{prefix}/SKILL.md: 'description' is {len(desc)} characters "
                    f"(limit is 1024)"
                )
            if XML_RE.search(desc):
                errors.append(
                    f"{prefix}/SKILL.md: 'description' contains forbidden "
                    "XML angle brackets (< or >)"
                )
    # --- compatibility field (optional) ---
    if "compatibility" in fm:
        compat = fm["compatibility"]
        if isinstance(compat, str):
            if not 1 <= len(compat) <= 500:
                errors.append(
                    f"{prefix}/SKILL.md: 'compatibility' must be 1–500 characters "
                    f"(got {len(compat)})"
                )

    # --- Body structure (warnings only) ---
    if not re.search(r"^## ", body, re.MULTILINE):
        warnings.append(
            f"{prefix}/SKILL.md: body has no '##' section headings — add at least one"
        )

    return errors, warnings


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    all_errors: list[str] = []
    all_warnings: list[str] = []
    skill_count = 0

    for entry in sorted(os.scandir(root), key=lambda e: e.name):
        if not entry.is_dir():
            continue
        if entry.name in SKIP or entry.name.startswith(".") or entry.name.startswith("_"):
            continue

        skill_count += 1
        errs, warns = validate_skill(entry.name, entry.path)
        all_errors.extend(errs)
        all_warnings.extend(warns)

    if skill_count == 0:
        print("No skill folders found (excluding _template and hidden directories).")
        return 0

    print(f"Validated {skill_count} skill(s).\n")

    if all_warnings:
        print("Warnings:")
        for w in all_warnings:
            print(f"  ⚠  {w}")
        print()

    if all_errors:
        print("Errors:")
        for e in all_errors:
            print(f"  ✗  {e}")
        print(f"\n{len(all_errors)} error(s) found. Fix them before merging.")
        return 1

    print("✓  All skills passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
