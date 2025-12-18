"""
Prompt Manager - Configuration and Constants
"""

import os
from enum import Enum
from pathlib import Path
from typing import Dict, Tuple

# ============================================================================
# PATHS & FILES
# ============================================================================

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "prompts.db"
SETTINGS_PATH = DATA_DIR / "settings.json"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# ============================================================================
# STREAMLIT CONFIG
# ============================================================================

STREAMLIT_CONFIG = {
    "page_title": "Prompt Manager",
    "page_icon": "💬",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ============================================================================
# THEME CONFIGURATION
# ============================================================================

class ThemeMode(str, Enum):
    """Theme enumeration"""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"
    GLASSMORPHISM = "glassmorphism"
    NEON = "neon"


# Light Theme Colors
LIGHT_THEME: Dict[str, str] = {
    # Primary
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "primary_light": "#DBEAFE",
    # Secondary
    "secondary": "#8B5CF6",
    "secondary_hover": "#7C3AED",
    "secondary_light": "#EDE9FE",
    # Accent
    "accent": "#EC4899",
    "accent_light": "#FCE7F3",
    # Background
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F9FAFB",
    "bg_tertiary": "#F3F4F6",
    # Text
    "text_primary": "#1F2937",
    "text_secondary": "#6B7280",
    "text_tertiary": "#9CA3AF",
    # Status
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    # Neutral
    "border": "#E5E7EB",
    "divider": "#D1D5DB",
}

# Dark Theme Colors
DARK_THEME: Dict[str, str] = {
    # Primary
    "primary": "#60A5FA",
    "primary_hover": "#93C5FD",
    "primary_light": "#1E3A8A",
    # Secondary
    "secondary": "#A78BFA",
    "secondary_hover": "#C4B5FD",
    "secondary_light": "#4C1D95",
    # Accent
    "accent": "#F472B6",
    "accent_light": "#831843",
    # Background
    "bg_primary": "#111827",
    "bg_secondary": "#1F2937",
    "bg_tertiary": "#374151",
    # Text
    "text_primary": "#F9FAFB",
    "text_secondary": "#D1D5DB",
    "text_tertiary": "#9CA3AF",
    # Status
    "success": "#34D399",
    "warning": "#FBBF24",
    "danger": "#F87171",
    "info": "#60A5FA",
    # Neutral
    "border": "#374151",
    "divider": "#4B5563",
}

# Glassmorphism Theme Colors (Modern frosted glass aesthetic)
GLASSMORPHISM_THEME: Dict[str, str] = {
    # Primary
    "primary": "#06B6D4",
    "primary_hover": "#0891B2",
    "primary_light": "#06B6D4",
    # Secondary
    "secondary": "#8B5CF6",
    "secondary_hover": "#7C3AED",
    "secondary_light": "#8B5CF6",
    # Accent
    "accent": "#EC4899",
    "accent_light": "#EC4899",
    # Background (Deep dark for contrast with glass)
    "bg_primary": "#0F172A",
    "bg_secondary": "rgba(15, 23, 42, 0.7)",
    "bg_tertiary": "rgba(30, 41, 59, 0.5)",
    # Text
    "text_primary": "#F1F5F9",
    "text_secondary": "#CBD5E1",
    "text_tertiary": "#94A3B8",
    # Status
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#06B6D4",
    # Neutral
    "border": "rgba(148, 163, 184, 0.3)",
    "divider": "rgba(148, 163, 184, 0.2)",
}

# Neon Theme Colors (High contrast with glowing accents)
NEON_THEME: Dict[str, str] = {
    # Primary (Neon cyan)
    "primary": "#00FFFF",
    "primary_hover": "#00E5E5",
    "primary_light": "#00FFFF",
    # Secondary (Neon purple)
    "secondary": "#FF00FF",
    "secondary_hover": "#E500E5",
    "secondary_light": "#FF00FF",
    # Accent (Neon pink)
    "accent": "#FF0080",
    "accent_light": "#FF0080",
    # Background (Dark for neon contrast)
    "bg_primary": "#0A0E27",
    "bg_secondary": "#1A1F3A",
    "bg_tertiary": "#2A2F4A",
    # Text
    "text_primary": "#FFFFFF",
    "text_secondary": "#E0E0FF",
    "text_tertiary": "#A0A0FF",
    # Status
    "success": "#00FF41",
    "warning": "#FFFF00",
    "danger": "#FF0041",
    "info": "#00FFFF",
    # Neutral
    "border": "#FF00FF",
    "divider": "#00FFFF",
}

# ============================================================================
# TYPOGRAPHY
# ============================================================================

TYPOGRAPHY = {
    "h1": {"size": "32px", "weight": 700, "line_height": 1.2},
    "h2": {"size": "24px", "weight": 600, "line_height": 1.3},
    "h3": {"size": "18px", "weight": 600, "line_height": 1.4},
    "body_lg": {"size": "16px", "weight": 400, "line_height": 1.5},
    "body": {"size": "14px", "weight": 400, "line_height": 1.5},
    "body_sm": {"size": "12px", "weight": 400, "line_height": 1.4},
    "label": {"size": "12px", "weight": 500, "line_height": 1.4},
    "code": {"size": "13px", "weight": 400, "line_height": 1.6},
}

FONT_FAMILY = "'Inter', 'Segoe UI', system-ui, sans-serif"

# ============================================================================
# SPACING SYSTEM
# ============================================================================

SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px",
    "2xl": "32px",
    "3xl": "48px",
}

# ============================================================================
# BORDER RADIUS
# ============================================================================

BORDER_RADIUS = {
    "sm": "4px",
    "md": "6px",
    "lg": "8px",
    "xl": "10px",
    "2xl": "12px",
}

# ============================================================================
# SHADOWS
# ============================================================================

SHADOWS = {
    "xs": "0 1px 2px rgba(0,0,0,0.05)",
    "sm": "0 1px 3px rgba(0,0,0,0.1)",
    "md": "0 4px 6px rgba(0,0,0,0.1)",
    "lg": "0 10px 15px rgba(0,0,0,0.1)",
    "xl": "0 20px 25px rgba(0,0,0,0.1)",
    "2xl": "0 25px 50px rgba(0,0,0,0.15)",
}

# ============================================================================
# VARIABLE TYPES
# ============================================================================

class VariableType(str, Enum):
    """Variable input types"""
    TEXT = "text"
    TEXTAREA = "textarea"
    SELECT = "select"
    NUMBER = "number"


# ============================================================================
# CATEGORIES
# ============================================================================

DEFAULT_CATEGORIES = [
    "Development",
    "Writing",
    "Marketing",
    "Analysis",
    "General",
]

# ============================================================================
# DATABASE SCHEMA
# ============================================================================

# Schema version for migrations
SCHEMA_VERSION = 1

# SQL for creating tables
CREATE_TABLES_SQL = """
-- Prompts table
CREATE TABLE IF NOT EXISTS prompts (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    is_favorite INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    use_count INTEGER DEFAULT 0
);

-- Create index on category for faster queries
CREATE INDEX IF NOT EXISTS idx_prompts_category ON prompts(category);
CREATE INDEX IF NOT EXISTS idx_prompts_is_favorite ON prompts(is_favorite);

-- Tags table
CREATE TABLE IF NOT EXISTS tags (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    color TEXT
);

-- Junction table for prompt-tag relationship
CREATE TABLE IF NOT EXISTS prompt_tags (
    prompt_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (prompt_id, tag_id),
    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Create index on tags
CREATE INDEX IF NOT EXISTS idx_prompt_tags_tag_id ON prompt_tags(tag_id);

-- Variables table
CREATE TABLE IF NOT EXISTS variables (
    id TEXT PRIMARY KEY,
    prompt_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    default_value TEXT,
    options TEXT,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE
);

-- Create index on variables
CREATE INDEX IF NOT EXISTS idx_variables_prompt_id ON variables(prompt_id);
"""

# ============================================================================
# UI SETTINGS
# ============================================================================

DEFAULT_SEARCH_DEBOUNCE_MS = 300
TOAST_DURATION_SUCCESS_MS = 3000
TOAST_DURATION_ERROR_MS = 5000
ITEMS_PER_PAGE = 20

# ============================================================================
# ANIMATION & TRANSITIONS
# ============================================================================

ANIMATION_QUICK_MS = 150
ANIMATION_STANDARD_MS = 300
ANIMATION_SMOOTH_MS = 500

# ============================================================================
# IMPORT/EXPORT
# ============================================================================

EXPORT_FILENAME_FORMAT = "prompts_export_{timestamp}.json"
MAX_IMPORT_SIZE_MB = 50

# ============================================================================
# PAGINATION
# ============================================================================

PAGINATE_BY = 20
