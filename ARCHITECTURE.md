# Prompt Manager - Architecture Document

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PROMPT MANAGER APP                              │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  UI LAYER (Streamlit Components)                                │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │  │
│  │  │   Home      │  │   Editor    │  │   Viewer    │  Settings   │  │
│  │  │  (Browse)   │  │  (Create)   │  │   (Use)     │             │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘              │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                              ▲                                          │
│                              │                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  COMPONENT LAYER (Reusable UI Components)                        │  │
│  │  • SearchBar       • PromptCard    • VariableForm               │  │
│  │  • FilterPanel     • TagInput      • ConfirmDialog              │  │
│  │  • CategorySelect  • Toast         • ThemeToggle                │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                              ▲                                          │
│                              │                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  SERVICE LAYER (Business Logic)                                  │  │
│  │  • PromptService      • VariableParser                           │  │
│  │  • FilterService      • ImportExportService                      │  │
│  │  • SearchService      • ClipboardService                         │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                              ▲                                          │
│                              │                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  DATA LAYER (SQLite Database)                                    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │  │
│  │  │   prompts    │  │   tags       │  │ prompt_tags  │            │  │
│  │  │   (main)     │  │  (lookup)    │  │  (junction)  │            │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘            │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  CONFIG & UTILITIES                                               │  │
│  │  • Theme Config (dark/light CSS)   • Utils (clipboard, etc)      │  │
│  │  • Constants & Settings             • Error Handlers             │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### UI Pages (pages/)
- **home.py**: Dashboard showing all prompts, search, filter, favorite management
- **editor.py**: Create/edit prompts with rich text, variable definition
- **viewer.py**: Dynamic form to fill variables, copy to clipboard
- **settings.py**: Preferences, import/export, data management

### Service Layer (services.py)
- `PromptService`: CRUD operations on prompts
- `VariableParser`: Extract/parse {{variable}} syntax
- `FilterService`: Search and filter logic
- `ImportExportService`: JSON serialization

### Component Layer (components.py)
- Reusable UI elements (cards, forms, dialogs)
- Encapsulates styling and Streamlit patterns

### Data Layer (database.py)
- `Database`: SQLite connection management
- `Prompt` model: Pydantic schema
- CRUD operations with parameterized queries

## Data Flow Diagram

```
USER ACTION
    │
    ▼
┌─────────────────────────────────────────┐
│  STREAMLIT PAGE (UI)                    │
│  • Renders components                   │
│  • Handles session_state                │
│  • Captures user input                  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  SERVICE LAYER                          │
│  • Validates data                       │
│  • Parses variables                     │
│  • Filters/searches                     │
│  • Handles business logic               │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  DATABASE LAYER                         │
│  • Execute SQL queries                  │
│  • Manage transactions                  │
│  • Return typed results                 │
└─────────────────────────────────────────┘
    │
    ▼
SQLite DB File (prompts.db)
```

## State Management Strategy

### Session State Keys
- `theme`: "light" or "dark" (persisted in settings)
- `search_query`: Current search text
- `active_filter`: Selected filter (category/tag)
- `selected_prompt_id`: Currently viewing/editing prompt
- `edit_mode`: Boolean for editor state
- `form_variables`: Dict of user-filled variables
- `toast_message`: Temporary notification
- `show_import_modal`: Boolean for import dialog

### Persistence Strategy
1. **In-Memory**: Session state for UI interactions (search, filters, current view)
2. **SQLite**: Persistent prompt data (all prompts, tags, favorites)
3. **JSON**: Settings file for user preferences (theme, layout)
4. **Clipboard**: Temporary (during session only)

## Error Handling Strategy

All operations wrapped with try-except returning user-friendly messages:
```python
try:
    result = service.operation()
    st.success("Operation completed")
except ValueError as e:
    st.error(f"Invalid input: {e}")
except Exception as e:
    st.error("Unexpected error. Please try again.")
    logger.exception(e)
```

## Performance Considerations

1. **Database Indexing**: Indexes on category, tags, is_favorite
2. **Query Optimization**: Lazy loading, pagination
3. **Caching**: `@st.cache_data` for static resources
4. **Session Caching**: Reuse query results within render cycle

## Security Considerations

1. **SQL Injection Prevention**: All queries parameterized
2. **Input Validation**: Pydantic schemas validate all data
3. **File Handling**: Safe JSON parsing with error handling
4. **No Remote Calls**: 100% offline, no API vulnerabilities
