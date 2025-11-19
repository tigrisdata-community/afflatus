# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Afflatus is a Flask-based web application that uses HTMX for dynamic frontend interactions and Pixeltable for data operations. The project is in early development stages with a minimal structure.

## Development Setup

The project uses `uv` for dependency management and Python virtual environments.

### Dependencies

- Python >=3.11
- Flask >=3.1.2
- Flask-HTMX >=0.4.0
- Pixeltable >=0.5.0

### Common Commands

**Install dependencies:**

```bash
uv sync
```

**Run the development server:**

```bash
uv run python main.py
```

Or activate the virtual environment first:

```bash
source .venv/bin/activate  # On Unix/macOS
python main.py
```

**Run with Flask's built-in server:**

```bash
flask run
```

## Architecture

The application follows a simple Flask structure:

- `main.py` - Main Flask application entry point with HTMX integration
- `static/` - Static assets (contains htmx.min.js and CSS files)
- `templates/` - Jinja2 templates with organized structure

### Key Components

- **Flask App**: Main web framework handling routing and requests
- **HTMX Integration**: Provides dynamic frontend functionality without writing JavaScript
- **Pixeltable**: Used for data operations and management

## HTMX

The application uses Flask-HTMX for dynamic content loading with partial template rendering. This approach provides a seamless user experience by avoiding full page reloads while maintaining clean separation of concerns.

### Template Structure

The project follows a modular template organization:

- `templates/base.html` - Base shell template containing HTML structure, CSS includes, and HTMX
- `templates/pages/` - Page-specific templates that extend the base template
- `templates/partials/` - Reusable content fragments for HTMX partial rendering

### HTMX Integration Pattern

Routes are structured to detect HTMX requests and return appropriate responses:

```python
@app.route("/")
def index():
    if htmx:
        return render_template("partials/index_content.html")
    return render_template("pages/index.html")
```

**How it works:**

- **Regular Browser Request**: Returns full page (`pages/index.html`) → extends `base.html` + includes partial content
- **HTMX Request**: Returns only partial content (`partials/index_content.html`) → just the content, no HTML shell

### Benefits

- **Performance**: Only sends necessary HTML content for dynamic updates
- **Maintainability**: Single source of truth for content (partials are reused)
- **SEO**: Full pages are properly structured for search engines
- **Accessibility**: Normal browser navigation works seamlessly
- **Progressive Enhancement**: Functions without JavaScript enabled

### Usage Guidelines

When creating new pages:

1. Create content in `templates/partials/` for the actual page content
2. Create page template in `templates/pages/` that extends `base.html` and includes the partial
3. Use the HTMX detection pattern in routes for partial/full rendering

## Development Guidelines

### Commit Guidelines

Commit messages follow **Conventional Commits** format:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

- Add `!` after type/scope for breaking changes or include `BREAKING CHANGE:` in the footer
- Keep descriptions concise, imperative, lowercase, and without a trailing period
- Reference issues/PRs in the footer when applicable

### Attribution Requirements

AI agents must disclose what tool and model they are using in the "Assisted-by" commit footer:

```text
Assisted-by: [Model Name] via [Tool Name]
```

Example:

```text
Assisted-by: GLM 4.6 via Claude Code
```

## Development Notes

- The project is in initial development with basic route structure implemented
- HTMX is fully integrated with partial rendering support
- No database models or API endpoints are currently defined
- Standard Flask conventions apply for future development
