# Prompt Manager - Development Guide

This guide is for developers who want to contribute to or extend the Prompt Manager application.

## Project Architecture Overview

### Layer Structure

```
Presentation Layer (pages/)
    ↓ Uses
Component Layer (components.py)
    ↓ Uses
Service Layer (services.py)
    ↓ Uses
Data Layer (database.py)
    ↓ Uses
SQLite Storage (data/prompts.db)
```

### Core Modules

| Module | Responsibility | Key Classes |
|--------|---|---|
| `main.py` | Entry point, page setup | N/A |
| `config.py` | Constants, settings, themes | ThemeMode, VariableType |
| `database.py` | SQLite operations, models | Database, Prompt, Variable |
| `services.py` | Business logic | PromptService, VariableParser, FilterService |
| `components.py` | Reusable UI pieces | Component functions |
| `styles.py` | CSS generation | Theme CSS generators |
| `utils.py` | Helpers | SettingsManager, ClipboardUtil, ValidationUtil |
| `pages/*.py` | Page implementations | Individual page logic |

## Development Environment Setup

### Prerequisites

```bash
# Python 3.10+
python --version

# pip
pip --version

# Git (optional)
git --version
```

### Development Installation

```bash
# 1. Clone repository
git clone <repo_url>
cd prompt-manager

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# 3. Install with dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# 4. Run the app
streamlit run main.py
```

## Code Standards

### Style Guide

```python
# Type hints on all functions
def create_prompt(title: str, content: str) -> Prompt:
    """Docstring on all public functions"""
    pass

# Snake case for functions/variables
def get_all_prompts() -> List[Prompt]:
    pass

# PascalCase for classes
class PromptService:
    pass

# Imports organized
import json
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel

# No global mutable state
# Use st.session_state instead
```

### Documentation Standards

```python
def create_prompt(
    title: str,
    content: str,
    category: str,
) -> Prompt:
    """
    Create a new prompt.
    
    Args:
        title: Prompt title (3-200 chars)
        content: Prompt content with {{variable}} placeholders
        category: Category name
        
    Returns:
        Created Prompt object
        
    Raises:
        ValueError: If title or content is invalid
    """
    pass
```

## Adding New Features

### Example: Add a New Variable Type

1. **Update config.py**:
```python
class VariableType(str, Enum):
    TEXT = "text"
    TEXTAREA = "textarea"
    SELECT = "select"
    NUMBER = "number"
    MULTI_SELECT = "multi-select"  # NEW
```

2. **Update components.py**:
```python
def variable_form(prompt: Prompt) -> Dict[str, str]:
    # ... existing code ...
    elif variable.type == VariableType.MULTI_SELECT:
        values[variable.name] = st.multiselect(
            label=variable.name,
            options=variable.options or [],
            default=variable.default_value,
        )
```

3. **Update variable_editor**:
```python
def variable_editor(...):
    var_type = st.selectbox(
        "Type",
        options=[t.value for t in VariableType],
        # ...
    )
```

4. **Test thoroughly** across all pages

### Example: Add a New Service

1. **Create class in services.py**:
```python
class NewService:
    """Service for new feature"""
    
    def __init__(self, db: Database) -> None:
        self.db = db
    
    def do_something(self) -> Optional[str]:
        """Do something useful"""
        pass
```

2. **Use in pages**:
```python
from services import NewService

def render_page():
    service = NewService(db)
    result = service.do_something()
```

### Example: Add a New Page

1. **Create pages/X_emoji_PageName.py**:
```python
import streamlit as st
from database import Database
from services import PromptService

def initialize_session_state() -> None:
    if "key" not in st.session_state:
        st.session_state.key = None

def render_page() -> None:
    st.title("Page Title")
    # Implementation

if __name__ == "__main__":
    initialize_session_state()
    render_page()
```

2. **Streamlit auto-discovers** pages in `pages/` directory

## Testing

### Manual Testing Checklist

- [ ] Create prompt with all variable types
- [ ] Search and filter functionality
- [ ] Toggle favorite status
- [ ] Edit existing prompt
- [ ] Delete prompt with confirmation
- [ ] Fill variables and copy result
- [ ] Export all prompts
- [ ] Import prompts
- [ ] Theme switching
- [ ] Settings persistence

### Automated Testing (Example)

```python
# tests/test_database.py
import pytest
from database import Database, Prompt

@pytest.fixture
def db():
    """Create in-memory database for testing"""
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(db_path)
        yield db

def test_create_prompt(db):
    prompt = Prompt(
        title="Test",
        content="Content",
        category="Test",
    )
    prompt_id = db.create_prompt(prompt)
    assert prompt_id is not None
    
    retrieved = db.get_prompt(prompt_id)
    assert retrieved.title == "Test"

def test_search_prompts(db):
    # Create test prompts
    # Search and verify results
    pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_database.py
```

## Performance Optimization

### Database Optimization

```python
# Already implemented
# Indexes on frequently searched columns
CREATE INDEX idx_prompts_category ON prompts(category);
CREATE INDEX idx_prompts_is_favorite ON prompts(is_favorite);

# For large databases, consider:
# - Pagination
# - Lazy loading
# - Result caching
```

### Streamlit Optimization

```python
# Use st.cache_data for expensive operations
@st.cache_data
def expensive_computation():
    return result

# Use st.cache_resource for one-time setup
@st.cache_resource
def get_database():
    return Database()

# Clear cache when needed
st.cache_data.clear()
```

## Debugging

### Enable Debug Mode

```python
# In config.py
DEBUG = True

# In services
if DEBUG:
    print(f"Debug: {variable}")
    
# In components
if DEBUG:
    st.write("Debug info", debug_dict)
```

### Common Issues

**Issue**: Database locked
```python
# Solution: Close connections properly
conn.close()
```

**Issue**: Session state not persisting
```python
# Solution: Initialize in st.session_state at top of page
if "key" not in st.session_state:
    st.session_state.key = default_value
```

**Issue**: Changes not reflecting
```python
# Solution: Call st.rerun()
st.rerun()
```

## Git Workflow

### Branch Naming

```
feat/feature-name        # New features
fix/bug-description      # Bug fixes
docs/documentation       # Documentation
refactor/improvement     # Code refactoring
test/test-name           # Tests
```

### Commit Messages

```
[FEATURE] Add dark mode toggle

- Implement theme switching logic
- Add color palettes
- Update settings persistence

Fixes #123
```

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes following code standards
4. Add tests
5. Update documentation
6. Submit PR with description

## Release Process

### Version Numbering

Use semantic versioning: `MAJOR.MINOR.PATCH`

- MAJOR: Breaking changes (1.0.0 → 2.0.0)
- MINOR: New features (1.0.0 → 1.1.0)
- PATCH: Bug fixes (1.0.0 → 1.0.1)

### Release Checklist

- [ ] Update version in config.py
- [ ] Update CHANGELOG
- [ ] Run all tests
- [ ] Test in Streamlit Cloud (if applicable)
- [ ] Create git tag
- [ ] Create release notes
- [ ] Announce update

## Troubleshooting Development Issues

### App not starting

```bash
# Clear Streamlit cache
streamlit cache clear

# Check for syntax errors
python -m py_compile *.py pages/*.py

# Run with verbose output
streamlit run main.py --logger.level=debug
```

### Import errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

### Database issues

```bash
# Delete and recreate
rm data/prompts.db

# Or in Python
from database import Database
db = Database()
```

## Performance Profiling

```python
import cProfile
import pstats

# Profile specific function
profiler = cProfile.Profile()
profiler.enable()

# Run code
result = expensive_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10
```

## Security Considerations for Developers

### Input Validation

```python
# Always validate user input
from pydantic import BaseModel, validator

class PromptInput(BaseModel):
    title: str
    
    @validator('title')
    def title_length(cls, v):
        if len(v) < 3:
            raise ValueError('Title too short')
        return v
```

### SQL Injection Prevention

```python
# ALWAYS use parameterized queries
cursor.execute(
    "SELECT * FROM prompts WHERE id = ?",
    (prompt_id,)  # Parameter, not string concatenation
)

# WRONG - Never do this
cursor.execute(f"SELECT * FROM prompts WHERE id = '{prompt_id}'")
```

### Error Handling

```python
# Always catch and handle errors gracefully
try:
    result = risky_operation()
except SpecificError as e:
    st.error(f"User-friendly message: {e}")
    logger.exception(e)
except Exception as e:
    st.error("Unexpected error occurred")
    logger.exception(e)
```

## Resources

### Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [Pydantic Docs](https://docs.pydantic.dev)
- [SQLite Docs](https://www.sqlite.org/docs.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Tools
- [Black - Code Formatter](https://black.readthedocs.io/)
- [flake8 - Style Guide Checker](https://flake8.pycqa.org/)
- [mypy - Type Checker](https://www.mypy-lang.org/)
- [pytest - Testing Framework](https://pytest.org/)

## Support for Developers

- Review ARCHITECTURE.md for system design
- Review DESIGN_SYSTEM.md for UI guidelines
- Check existing code for patterns and conventions
- Use type hints and docstrings consistently
- Test thoroughly before committing

---

Happy coding! 🚀
