#!/usr/bin/env python3
"""Stamp developer credit into the PPTX footer and metadata."""

from __future__ import annotations

import shutil
import tempfile
import zipfile
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
PPTX_PATH = ROOT / "outputs" / "loneliness_risk_research_deck.pptx"
CREDIT = "Developed by He Haoze (何昊泽)"
LOGO_NAME = "lrdl_logo_mark.png"
LOGO_REL_ID = "rIdLrdlLogo"
LOGO_TARGET = f"../media/{LOGO_NAME}"


def patch_xml(text: str) -> str:
    return text.replace("Loneliness &amp; Risk Decision Lab", CREDIT)


def patch_slide_xml(text: str) -> str:
    text = patch_xml(text)
    if "LRDL HHZ logo" in text:
        return text
    ids = [int(match) for match in re.findall(r'<p:cNvPr id="(\d+)"', text)]
    shape_id = (max(ids) + 1) if ids else 900
    pic = f'''
      <p:pic>
        <p:nvPicPr>
          <p:cNvPr id="{shape_id}" name="LRDL HHZ logo"/>
          <p:cNvPicPr><a:picLocks noChangeAspect="1" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/></p:cNvPicPr>
          <p:nvPr/>
        </p:nvPicPr>
        <p:blipFill>
          <a:blip r:embed="{LOGO_REL_ID}" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
          <a:stretch xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:fillRect/></a:stretch>
        </p:blipFill>
        <p:spPr>
          <a:xfrm xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:off x="365760" y="6267450"/>
            <a:ext cx="342900" cy="342900"/>
          </a:xfrm>
          <a:prstGeom prst="rect" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:avLst/></a:prstGeom>
        </p:spPr>
      </p:pic>
    '''
    return text.replace("</p:spTree>", f"{pic}</p:spTree>")


def patch_slide_rels(text: str) -> str:
    if LOGO_REL_ID in text or LOGO_TARGET in text:
        return text
    rel = f'<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{LOGO_TARGET}" Id="{LOGO_REL_ID}" />'
    return text.replace("</Relationships>", f"{rel}</Relationships>")


def patch_content_types(text: str) -> str:
    if 'Extension="png"' in text:
        return text
    default = '<Default Extension="png" ContentType="image/png"/>'
    return text.replace("</Types>", f"{default}</Types>")


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
    logo_path = ASSET_DIR / LOGO_NAME
    if not logo_path.exists():
        raise FileNotFoundError(logo_path)

    tmp_dir = Path(tempfile.mkdtemp(prefix="pptx-credit-"))
    patched = tmp_dir / PPTX_PATH.name
    media_written = False
    try:
        with zipfile.ZipFile(PPTX_PATH, "r") as zin, zipfile.ZipFile(patched, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename.startswith("ppt/slides/slide") and item.filename.endswith(".xml"):
                    data = patch_slide_xml(data.decode("utf-8")).encode("utf-8")
                elif item.filename.startswith("ppt/slides/_rels/slide") and item.filename.endswith(".xml.rels"):
                    data = patch_slide_rels(data.decode("utf-8-sig")).encode("utf-8")
                elif item.filename == "docProps/core.xml":
                    data = patch_core(data.decode("utf-8")).encode("utf-8")
                elif item.filename == "[Content_Types].xml":
                    data = patch_content_types(data.decode("utf-8")).encode("utf-8")
                elif item.filename == f"ppt/media/{LOGO_NAME}":
                    data = logo_path.read_bytes()
                    media_written = True
                zout.writestr(item, data)
            if not media_written:
                zout.writestr(f"ppt/media/{LOGO_NAME}", logo_path.read_bytes())
        shutil.copy2(patched, PPTX_PATH)
        print({"pptx": str(PPTX_PATH), "credit": CREDIT, "logo": LOGO_NAME})
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
