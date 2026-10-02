"""
Unit Tests for Text Encoding Integrity and Mojibake Prevention.
Ensures no malformed character sequences (?C, W/m?, ' ? ', U+FFFD) exist in codebase.
"""

import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend", "app")

MOJIBAKE_PATTERNS = [
    (re.compile(r"\b\d+\s*\?C\b|\?C\b"), "Mangled degree Celsius (?C)"),
    (re.compile(r"W/m\?"), "Mangled solar irradiance unit (W/m?)"),
    (re.compile(r"\s\?\s"), "Mangled em-dash or punctuation ( ? )"),
    (re.compile(r"\ufffd"), "Unicode replacement character (\\ufffd)"),
]


def test_no_mojibake_in_backend():
    """Scan all backend Python source files to ensure complete absence of mojibake."""
    violations = []

    for root, dirs, files in os.walk(BACKEND_DIR):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                rel_path = os.path.relpath(path, PROJECT_ROOT)
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    for line_idx, line in enumerate(fh, 1):
                        for pat, desc in MOJIBAKE_PATTERNS:
                            if pat.search(line):
                                violations.append(f"{rel_path}:{line_idx} - {desc}: {line.strip()[:80]}")

    assert not violations, "Mojibake detected in backend:\n" + "\n".join(violations)


def test_no_mojibake_in_docs():
    """Scan key documentation markdown files to ensure clean typographic characters."""
    docs_dir = os.path.join(PROJECT_ROOT, "docs")
    violations = []

    target_docs = [
        "MODEL_SPEC.md",
        "RISK_METHODOLOGY.md",
        "METHODOLOGY.md",
        "VALIDATION.md",
        "COVERAGE.md",
        "AUDIT_REMEDIATION.md"
    ]

    for doc_name in target_docs:
        doc_path = os.path.join(docs_dir, doc_name)
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8", errors="replace") as fh:
                for line_idx, line in enumerate(fh, 1):
                    for pat, desc in MOJIBAKE_PATTERNS:
                        if pat.search(line):
                            violations.append(f"docs/{doc_name}:{line_idx} - {desc}: {line.strip()[:80]}")

    assert not violations, "Mojibake detected in key documentation:\n" + "\n".join(violations)
