#!/usr/bin/env python3
"""Small dependency-free checks for the Orbit 3DS browser shell."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = ROOT / "index.html"
REQUIRED_IDS = {
    "topScreen", "bottomScreen", "gameInput", "saveInput", "accountButton",
    "signInBtn", "registerBtn", "uploadCloudBtn", "downloadCloudBtn",
    "corePill", "coreStatusDetail", "engineMessage", "runBtn"
}


class InspectHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.scripts: list[tuple[str, str]] = []
        self._script_type: str | None = None
        self._script_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs_dict = dict(attrs)
        element_id = attrs_dict.get("id")
        if element_id:
            if element_id in self.ids:
                raise ValueError(f"Duplicate HTML id: {element_id}")
            self.ids.add(element_id)
        if tag.lower() == "script":
            self._script_type = attrs_dict.get("type", "text/javascript").lower()
            self._script_parts = []

    def handle_data(self, data: str) -> None:
        if self._script_type is not None:
            self._script_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._script_type is not None:
            source = "".join(self._script_parts)
            if source.strip() and self._script_type in {"text/javascript", "application/javascript", "module"}:
                self.scripts.append((self._script_type, source))
            self._script_type = None
            self._script_parts = []


def main() -> int:
    if not HTML_FILE.is_file():
        print("ERROR: index.html is missing", file=sys.stderr)
        return 1

    parser = InspectHTML()
    try:
        parser.feed(HTML_FILE.read_text(encoding="utf-8"))
        parser.close()
    except Exception as exc:
        print(f"ERROR: HTML parsing failed: {exc}", file=sys.stderr)
        return 1

    missing = sorted(REQUIRED_IDS - parser.ids)
    if missing:
        print("ERROR: required interface elements are missing: " + ", ".join(missing), file=sys.stderr)
        return 1

    for number, (script_type, source) in enumerate(parser.scripts, start=1):
        command = ["node", "--check", "--input-type=module" if script_type == "module" else "--input-type=commonjs"]
        result = subprocess.run(command, input=source, text=True, capture_output=True)
        if result.returncode:
            print(f"ERROR: inline script {number} failed Node syntax checking:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return result.returncode

    if not (ROOT / "core" / "adapter-contract.json").is_file():
        print("ERROR: core adapter contract is missing", file=sys.stderr)
        return 1

    print(f"OK: index.html parsed; {len(parser.ids)} unique IDs; {len(parser.scripts)} inline script(s) passed Node syntax checks.")
    print("NOTE: this workflow validates and deploys the web shell. It does not compile or bundle a 3DS emulator core.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
