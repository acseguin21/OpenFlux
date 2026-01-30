# Installation Fix - tree-sitter-languages

## Issue
The `tree-sitter-languages` package doesn't exist and was causing installation failures.

## Fix Applied
1. ✅ Removed non-existent `tree-sitter-languages` package from `requirements.txt`
2. ✅ Made language-specific parsers optional (moved to `requirements-optional.txt`)
3. ✅ Updated installation script to handle optional packages gracefully
4. ✅ Code already handles missing language parsers with try/except blocks

## Installation

### Standard Installation
```bash
pip install -r requirements.txt
```

### With Language Parsers (Optional)
```bash
pip install -r requirements.txt
pip install -r requirements-optional.txt
```

**Note**: On Python 3.13+, some language parser packages may not have pre-built wheels. The code will work without them, but you'll only be able to index files in languages that have parsers installed.

### If Language Parsers Fail to Install

The code gracefully handles missing parsers. You can:

1. **Skip them** - The indexer will work but only parse files in languages with available parsers
2. **Build from source** - See instructions in `requirements-optional.txt`
3. **Use Python 3.12 or earlier** - If you need all language parsers immediately

## What Changed

- **Before**: `tree-sitter-languages>=1.10.0` (doesn't exist)
- **After**: Removed, language parsers are now optional individual packages

## Verification

Run the debug script to check what's installed:
```bash
python3 scripts/debug_check.py
```

The indexer will automatically detect which language parsers are available and only use those.
