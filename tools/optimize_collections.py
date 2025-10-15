"""
Optimize images under assets/collections into assets/collections/optimized as WebP.

Usage:
  python3 tools/optimize_collections.py

Requirements:
  pip install Pillow
"""

from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'assets' / 'collections'
DST = SRC / 'optimized'


def optimize_image(src_path: Path, dst_path: Path, max_width: int = 1600, quality: int = 78) -> None:
  with Image.open(src_path) as im:
    im.load()
    # Resize to max width keeping aspect ratio if needed
    if im.width > max_width:
      ratio = max_width / im.width
      new_size = (max_width, int(im.height * ratio))
      im = im.resize(new_size, Image.LANCZOS)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst_path, format='WEBP', quality=quality, method=6)
    print(f"Optimized {src_path.relative_to(ROOT)} -> {dst_path.relative_to(ROOT)}")


def main() -> int:
  if not SRC.exists():
    print(f"No collections folder at {SRC}")
    return 1
  for p in SRC.iterdir():
    if p.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
      dst = DST / (p.stem + '.webp')
      try:
        optimize_image(p, dst)
      except Exception as e:
        print(f"Failed for {p}: {e}")
  return 0


if __name__ == '__main__':
  raise SystemExit(main())


