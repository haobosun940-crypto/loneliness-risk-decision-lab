#!/usr/bin/env python3
"""Stamp developer credit into the PPTX footer and metadata."""

from __future__ import annotations

import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PPTX_PATH = ROOT / "outputs" / "loneliness_risk_research_deck.pptx"
CREDIT = "Developed by He Haoze (何昊泽)"


def patch_xml(text: str) -> str:
    return text.replace("Loneliness &amp; Risk Decision Lab", CREDIT)


def patch_core(text: str) -> str:
    replacements = {
        "<dc:creator>Walnut Exporter</dc:creator>": f"<dc:creator>{CREDIT}</dc:creator>",
        "<lastModifiedBy>Walnut Exporter</lastModifiedBy>": f"<lastModifiedBy>{CREDIT}</lastModifiedBy>",
        "<dc:title>Presentation</dc:title>": "<dc:title>Loneliness, Social Connection, and Risk Decisions</dc:title>",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def main() -> None:
    if not PPTX_PATH.exists():
        raise FileNotFoundError(PPTX_PATH)

    tmp_dir = Path(tempfile.mkdtemp(prefix="pptx-credit-"))
    patched = tmp_dir / PPTX_PATH.name
    try:
        with zipfile.ZipFile(PPTX_PATH, "r") as zin, zipfile.ZipFile(patched, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename.startswith("ppt/slides/slide") and item.filename.endswith(".xml"):
                    data = patch_xml(data.decode("utf-8")).encode("utf-8")
                elif item.filename == "docProps/core.xml":
                    data = patch_core(data.decode("utf-8")).encode("utf-8")
                zout.writestr(item, data)
        shutil.copy2(patched, PPTX_PATH)
        print({"pptx": str(PPTX_PATH), "credit": CREDIT})
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
