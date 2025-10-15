"""Generate favicon files from a square or rectangular logo image.

This script creates optimized favicon PNGs and a multi-size ICO by
scaling the source logo to fit each target size while preserving
aspect ratio and centering it on a transparent square canvas.

Usage:
  python3 tools/generate_favicons.py [--src PATH] [--outdir PATH]

Requirements:
  pip install Pillow
"""

from pathlib import Path
import argparse
import json
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ASSETS = ROOT / 'assets'


OUTPUTS = {
    'favicon.ico': [(16, 16), (32, 32), (48, 48), (64, 64)],
    'favicon-16.png': (16, 16),
    'favicon-32.png': (32, 32),
    'favicon-48.png': (48, 48),
    'favicon-96.png': (96, 96),
    'favicon-192.png': (192, 192),
    'favicon-512.png': (512, 512),
    'apple-touch-icon.png': (180, 180),
}


MANIFEST = {
    "name": "RB-Ventures LLC",
    "short_name": "RB-Ventures",
    "icons": [
        {"src": "/assets/favicon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/assets/favicon-512.png", "sizes": "512x512", "type": "image/png"}
    ],
    "theme_color": "#15c3b8",
    "background_color": "#ffffff",
    "display": "standalone",
}


def make_square_icon(image: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    """Return a square RGBA image of size target_size with the source image
    scaled proportionally and centered on a transparent background.
    """
    w, h = target_size
    target = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    src_w, src_h = image.size
    scale = min(w / src_w, h / src_h)
    new_w = int(round(src_w * scale))
    new_h = int(round(src_h * scale))

    resized = image.copy().resize((new_w, new_h), Image.LANCZOS)
    offset_x = (w - new_w) // 2
    offset_y = (h - new_h) // 2
    target.paste(resized, (offset_x, offset_y), resized)
    return target


def generate(src_path: Path, out_dir: Path) -> int:
    """Generate favicons from src_path and write them to out_dir.

    Returns 0 on success, non-zero on error.
    """
    if not src_path.exists():
        print(f"Source logo not found at {src_path}")
        return 2

    image = Image.open(src_path).convert('RGBA')

    # create output directory if needed
    out_dir.mkdir(parents=True, exist_ok=True)

    for name, size in OUTPUTS.items():
        outpath = out_dir / name
        if name.endswith('.ico'):
            sizes = OUTPUTS[name]
            icons = [make_square_icon(image, s) for s in sizes]
            icons[0].save(outpath, format='ICO', sizes=sizes)
        else:
            icon = make_square_icon(image, size)
            icon.save(outpath, format='PNG')
        print(f"Written {outpath}")

    # write manifest
    manifest_path = out_dir / 'site.webmanifest'
    with open(manifest_path, 'w') as f:
        json.dump(MANIFEST, f, indent=2)
    print(f"Written {manifest_path}")

    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Generate favicon images from a source logo')
    p.add_argument('--src', type=Path, default=DEFAULT_ASSETS / 'logo.png', help='Source logo path')
    p.add_argument('--outdir', type=Path, default=DEFAULT_ASSETS, help='Output directory for favicons')
    return p.parse_args()


def main() -> int:
    args = parse_args()
    return generate(args.src, args.outdir)


if __name__ == '__main__':
    raise SystemExit(main())
