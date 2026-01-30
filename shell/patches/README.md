# Shell Patches

Place patches here that are applied on top of the upstream editor before building.

Typical targets:

- **Product name** – Change the upstream product name to “OpenCode” in window title, About dialog, and `product.json`.
- **Default theme** – Point to a bundled Scarlet & Jade theme.
- **Built-in extensions** – Ensure `extensions/opencode-ai-tools` (and optionally compatible extensions) are included in the build.

Create patches from the upstream clone after making edits, e.g.:

```bash
cd /path/to/upstream-clone
# edit files...
git diff --no-prefix > /path/to/opencode/shell/patches/product-name.patch
```

Apply in build script with:

```bash
git apply --directory=path/to/code patches/product-name.patch
```

See `docs/STANDALONE_IDE_ROADMAP.md` for full workflow.
