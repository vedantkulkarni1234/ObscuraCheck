# Prompt Manager - A Beautiful Prompt Organization System

A production-grade Streamlit application for creating, organizing, and using reusable prompts with dynamic variables. Built for AI power users, developers, and content creators.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.32+-red)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### Core Functionality
- **Create Prompts**: Rich text editor with support for dynamic variables using `{{variable}}` syntax
- **Organize**: Categorize prompts and add tags for easy discovery
- **Search & Filter**: Full-text search across titles, content, and variables
- **Dynamic Variables**: Auto-detect or manually define text, textarea, select, and number inputs
- **Use Prompts**: Beautiful form to fill variables and generate final text
- **Favorites**: Star your most-used prompts for quick access
- **Statistics**: Track usage count and library metrics

### Data Management
- **Import/Export**: Full JSON import/export for backup and sharing
- **100% Offline**: No external API calls, works completely offline
- **SQLite Persistence**: Local database for fast, reliable storage
- **Parameterized Queries**: SQL injection protection throughout

### Design & UX
- **Dark/Light Themes**: Beautiful, accessible theming system
- **Responsive Layout**: Optimized for desktop screens (1200px+)
- **Smooth Animations**: Polish and micro-interactions throughout
- **Toast Notifications**: Immediate feedback for all actions
- **Clean Interface**: Generous whitespace, clear visual hierarchy

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository_url>
cd prompt-manager
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run main.py
```

5. **Open in browser**
The app will automatically open at `http://localhost:8501`

### First Run Experience

1. **Home Page**: See your empty library with quick stats
2. **Create First Prompt**: Click "➕ Create" button
3. **Fill Basic Info**: Add title, category, and content
4. **Add Variables**: Use `{{topic}}` syntax in your content
5. **Save**: Click "💾 Save Prompt"
6. **Use Your Prompt**: Go to home, select prompt, fill variables, copy!

## 📁 Project Structure

```
prompt-manager/
├── main.py                 # Entry point, app initialization
├── config.py              # Configuration, constants, theme colors
├── database.py            # SQLite models and CRUD operations
├── services.py            # Business logic (PromptService, etc.)
├── components.py          # Reusable UI components
├── styles.py              # CSS injection and theming
├── utils.py               # Helper utilities
├── pages/
│   ├── 1_🏠_Home.py       # Browse and search prompts
│   ├── 2_✏️_Create.py     # Create/edit prompts
│   ├── 3_▶️_Use.py        # Use prompts with variables
│   └── 4_⚙️_Settings.py   # Settings, import/export
├── data/                  # Data directory (created automatically)
│   ├── prompts.db        # SQLite database
│   └── settings.json     # User settings
├── requirements.txt       # Python dependencies
├── ARCHITECTURE.md       # System architecture document
├── DESIGN_SYSTEM.md      # Visual design system
├── SAMPLE_DATA.json      # Example prompts for import
└── README.md             # This file
```

## 💡 Usage Guide

### Creating Prompts

1. Navigate to "✏️ Create" page
2. Enter prompt details:
   - **Title**: Short, descriptive name (3-200 chars)
   - **Category**: Organize by type (Development, Writing, etc.)
   - **Content**: Your prompt text with `{{variable}}` placeholders
   - **Tags**: Add searchable tags
   - **Variables**: Define types, defaults, options

3. **Variable Syntax**:
```
Please review this {{language}} code for {{focus_area}}:

```{{code}}```

Provide suggestions for improvement.
```

### Variable Types

- **text**: Single-line input (default)
- **textarea**: Multi-line input for long content
- **select**: Dropdown with predefined options
- **number**: Numeric input

### Searching & Filtering

1. **Full-Text Search**: Search across titles, content, variables
2. **Category Filter**: Filter by category
3. **Tag Filter**: Filter by one or more tags
4. **Favorites**: Show only starred prompts
5. **Results Pagination**: Navigate through results

### Using Prompts

1. Find and select a prompt
2. Fill in the variable form
3. Review the final result
4. Copy to clipboard
5. Or edit/delete as needed

### Import/Export

**Export**:
1. Go to "⚙️ Settings" → "📤 Export"
2. Click "📥 Export as JSON"
3. Download the file

**Import**:
1. Go to "⚙️ Settings" → "📥 Import"
2. Upload a JSON file
3. Review and confirm
4. Prompts are added to your library

## 🎨 Theming

### Customize Colors

Edit `config.py` to modify theme colors:

```python
LIGHT_THEME: Dict[str, str] = {
    "primary": "#2563EB",  # Blue
    "accent": "#EC4899",   # Pink
    # ... more colors
}

DARK_THEME: Dict[str, str] = {
    "primary": "#60A5FA",  # Light blue
    "accent": "#F472B6",   # Light pink
    # ... more colors
}
```

### Apply Theme

1. Go to "⚙️ Settings" → "🎨 Preferences"
2. Select theme: "auto", "light", or "dark"
3. Changes apply immediately

## 🔐 Security & Privacy

- **No Cloud**: Everything stays on your machine
- **No Tracking**: No analytics or telemetry
- **SQL Injection Protection**: All queries parameterized
- **Input Validation**: Pydantic validation on all data
- **Open Source**: Audit the code yourself

## 📊 Data Model

### Prompt Schema

```json
{
  "id": "uuid",
  "title": "Code Review Request",
  "content": "Please review this {{language}} code...",
  "category": "Development",
  "tags": ["code-review", "programming"],
  "variables": [
    {
      "name": "language",
      "type": "select",
      "default_value": "Python",
      "options": ["Python", "JavaScript", "Go"]
    }
  ],
  "is_favorite": false,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "use_count": 47
}
```

## 🗄️ Database

### Tables

- **prompts**: Main prompt data
- **tags**: Tag definitions
- **prompt_tags**: Prompt-tag relationships
- **variables**: Variable definitions for prompts

### Indexes

- `prompts.category` - Fast category filtering
- `prompts.is_favorite` - Quick favorite lookups
- `prompt_tags.tag_id` - Efficient tag queries

## ⚙️ Configuration

Edit `config.py` to adjust:

- **THEMES**: Light/dark color schemes
- **TYPOGRAPHY**: Font sizes and weights
- **SPACING**: Margin and padding system
- **ANIMATIONS**: Transition durations
- **PAGINATION**: Items per page

## 🐛 Troubleshooting

### App won't start
```bash
# Clear Streamlit cache
streamlit cache clear

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database errors
```bash
# Database will auto-recreate on startup
# Delete data/prompts.db to reset
rm data/prompts.db
```

### Copy to clipboard not working
- Check if `pyperclip` is installed: `pip install pyperclip`
- Some browsers require clipboard permissions

## 📈 Performance

- **Search**: Indexed queries, <100ms typical
- **Pagination**: Load-on-demand, 20 items default
- **Export**: <1s for 1000 prompts
- **Database**: SQLite, ~10MB per 1000 prompts

## 🔧 Development

### Project Structure for Developers

```
UI Layer          → pages/1-4.py (Streamlit components)
Component Layer   → components.py (reusable UI pieces)
Service Layer     → services.py (business logic)
Data Layer        → database.py (SQLite CRUD)
Config/Utils      → config.py, styles.py, utils.py
```

### Adding Features

1. **New Page**: Create in `pages/` directory
2. **New Component**: Add to `components.py`
3. **New Service**: Add to `services.py`
4. **Database Changes**: Update `database.py` schema

### Code Style

- Type hints on all functions
- Docstrings on public functions
- Clean, Pythonic code
- No global mutable state

## 📦 Sample Data

### Import Sample Prompts

A `SAMPLE_DATA.json` file is provided with example prompts:

```bash
# Go to Settings → Import
# Upload SAMPLE_DATA.json
```

Contains examples for:
- Code review prompts
- Content writing templates
- Analysis frameworks
- General utilities

## 🤝 Contributing

Found a bug or have a feature request?

1. Check existing issues
2. Create detailed bug report
3. Include steps to reproduce
4. Suggest improvements with reasoning

## 📝 License

MIT License - Feel free to use and modify

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io) - Amazing data app framework
- [Pydantic](https://pydantic-settings.readthedocs.io) - Data validation
- [SQLite](https://www.sqlite.org) - Reliable local database

## 📞 Support

- **Documentation**: See `ARCHITECTURE.md` and `DESIGN_SYSTEM.md`
- **Issues**: GitHub issues section
- **Discussions**: GitHub discussions

## 🎯 Roadmap

Potential future features:
- [ ] Cloud sync (optional)
- [ ] Prompt templates/inheritance
- [ ] Advanced search with operators
- [ ] Batch operations
- [ ] Custom themes
- [ ] Keyboard shortcuts
- [ ] Dark mode improvements
- [ ] Mobile optimization

---

**Made with ❤️ for prompt enthusiasts**

Happy prompting! 🚀
