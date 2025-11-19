# Afflatus

A lightweight Flask app for experimenting with Pixeltable and HTMX-driven UI prototypes.

## Development

### Linting and formatting

The CI workflow runs [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting on every push and pull request targeting `main`. Run the same checks locally before opening a PR:

```bash
ruff format --check .
ruff check .
```
