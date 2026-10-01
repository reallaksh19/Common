# Changed-file summary CLI

Test-only utility for Common #486.

## Input

Provide a JSON array of non-empty changed-file path strings. Paths are normalized to `/` separators.

Read from stdin:

```bash
printf '%s\n' '["src/app.py", "docs/guide.md", "README"]' \
  | python changed_file_summary.py
```

Or pass a UTF-8 JSON file:

```bash
python changed_file_summary.py changed-files.json
```

## Output

The CLI writes deterministic JSON containing:

- `total_file_count`;
- `extensions`, counted by lowercase final extension (`<no_extension>` when absent);
- `directories`, the sorted unique direct parent directories of changed files (`.` for repository-root files).

Malformed JSON, a non-array top-level value, non-string/empty path items, and input-file read failures are reported on stderr without a traceback and return exit code `2`.

## Tests

From this directory:

```bash
python -m unittest -v test_changed_file_summary.py
```
