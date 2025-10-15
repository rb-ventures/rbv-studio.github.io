# rbv-studio.github.io

## Optimize collection images

Generate WebP versions (significantly smaller) and optional resize to max width 1600px:

```bash
python3 tools/optimize_collections.py
```

Outputs go to `assets/collections/optimized/`. The site will automatically use these WebP images when available via `<picture>` fallbacks.