# securevault/gui/style.py

from pathlib import Path

# Beolvassuk a style.qss-t ugyanebből a mappából
style_path = Path(__file__).parent / "style.qss"
style_sheet = style_path.read_text(encoding="utf-8")
