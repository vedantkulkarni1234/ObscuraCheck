"""
Prompt Manager - Utility Functions
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from config import SETTINGS_PATH, DATA_DIR


# ============================================================================
# SETTINGS MANAGEMENT
# ============================================================================

class SettingsManager:
    """Manage user preferences"""

    def __init__(self, settings_path: Path = SETTINGS_PATH) -> None:
        """Initialize settings manager"""
        self.settings_path = settings_path
        self.defaults: Dict[str, Any] = {
            "theme": "auto",
            "show_stats": True,
            "items_per_page": 20,
            "last_export": None,
            "sort_by": "created_at",
            "sort_order": "desc",
        }

    def load(self) -> Dict[str, Any]:
        """Load settings from file"""
        if not self.settings_path.exists():
            return self.defaults.copy()

        try:
            with open(self.settings_path) as f:
                settings = json.load(f)
                # Merge with defaults for any missing keys
                return {**self.defaults, **settings}
        except (json.JSONDecodeError, IOError):
            return self.defaults.copy()

    def save(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file"""
        try:
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_path, "w") as f:
                json.dump(settings, f, indent=2)
            return True
        except IOError:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        settings = self.load()
        return settings.get(key, default)

    def set(self, key: str, value: Any) -> bool:
        """Set a setting value"""
        settings = self.load()
        settings[key] = value
        return self.save(settings)


# ============================================================================
# CLIPBOARD UTILITIES
# ============================================================================

class ClipboardUtil:
    """Clipboard operations"""

    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """
        Copy text to clipboard (works with streamlit-copy-to-clipboard)
        
        Args:
            text: Text to copy
            
        Returns:
            True if successful
        """
        try:
            import pyperclip

            pyperclip.copy(text)
            return True
        except ImportError:
            # Fallback: copy_to_clipboard is handled by Streamlit component
            return True
        except Exception:
            return False

    @staticmethod
    def format_for_copying(text: str) -> str:
        """Format text for optimal copying"""
        return text.strip()


# ============================================================================
# DATE/TIME UTILITIES
# ============================================================================

class DateTimeUtil:
    """Date and time utilities"""

    @staticmethod
    def format_relative(iso_datetime: str) -> str:
        """
        Format ISO datetime as relative time
        
        Args:
            iso_datetime: ISO format datetime string
            
        Returns:
            Relative time string (e.g., "2 hours ago")
        """
        try:
            dt = datetime.fromisoformat(iso_datetime)
            now = datetime.utcnow()
            diff = now - dt

            if diff.days > 365:
                years = diff.days // 365
                return f"{years}y ago"
            elif diff.days > 30:
                months = diff.days // 30
                return f"{months}mo ago"
            elif diff.days > 0:
                return f"{diff.days}d ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours}h ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes}m ago"
            else:
                return "just now"
        except (ValueError, TypeError):
            return "unknown"

    @staticmethod
    def format_date(iso_datetime: str, format_str: str = "%Y-%m-%d") -> str:
        """
        Format ISO datetime
        
        Args:
            iso_datetime: ISO format datetime string
            format_str: Python datetime format string
            
        Returns:
            Formatted date string
        """
        try:
            dt = datetime.fromisoformat(iso_datetime)
            return dt.strftime(format_str)
        except (ValueError, TypeError):
            return "unknown"


# ============================================================================
# STRING UTILITIES
# ============================================================================

class StringUtil:
    """String manipulation utilities"""

    @staticmethod
    def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
        """Truncate string with suffix"""
        if len(text) <= length:
            return text
        return text[: length - len(suffix)] + suffix

    @staticmethod
    def excerpt(text: str, length: int = 200) -> str:
        """Get excerpt from text (first N chars)"""
        return StringUtil.truncate(text, length, "...")

    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to slug format"""
        import re

        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_]+", "-", text)
        return text

    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        return len(text.split())

    @staticmethod
    def count_characters(text: str) -> int:
        """Count characters in text"""
        return len(text)


# ============================================================================
# VALIDATION UTILITIES
# ============================================================================

class ValidationUtil:
    """Input validation utilities"""

    @staticmethod
    def is_valid_title(title: str) -> bool:
        """Validate prompt title"""
        return bool(title and len(title.strip()) >= 3 and len(title) <= 200)

    @staticmethod
    def is_valid_content(content: str) -> bool:
        """Validate prompt content"""
        return bool(content and len(content.strip()) >= 10 and len(content) <= 10000)

    @staticmethod
    def is_valid_category(category: str) -> bool:
        """Validate category name"""
        return bool(category and len(category.strip()) >= 1 and len(category) <= 50)

    @staticmethod
    def is_valid_tag(tag: str) -> bool:
        """Validate tag name"""
        return bool(tag and len(tag.strip()) >= 1 and len(tag) <= 30)

    @staticmethod
    def validate_prompt_data(
        title: str, content: str, category: str
    ) -> tuple[bool, str]:
        """
        Validate prompt data
        
        Returns:
            (is_valid, error_message)
        """
        if not ValidationUtil.is_valid_title(title):
            return False, "Title must be 3-200 characters"

        if not ValidationUtil.is_valid_content(content):
            return False, "Content must be 10-10000 characters"

        if not ValidationUtil.is_valid_category(category):
            return False, "Category must be 1-50 characters"

        return True, ""


# ============================================================================
# FILE UTILITIES
# ============================================================================

class FileUtil:
    """File handling utilities"""

    @staticmethod
    def safe_read_file(file_path: Path) -> Optional[str]:
        """Safely read file content"""
        try:
            if file_path.exists() and file_path.is_file():
                with open(file_path, encoding="utf-8") as f:
                    return f.read()
            return None
        except (IOError, UnicodeDecodeError):
            return None

    @staticmethod
    def safe_write_file(file_path: Path, content: str) -> bool:
        """Safely write file content"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except IOError:
            return False

    @staticmethod
    def ensure_data_dir() -> Path:
        """Ensure data directory exists"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return DATA_DIR


# ============================================================================
# JSON UTILITIES
# ============================================================================

class JsonUtil:
    """JSON utilities"""

    @staticmethod
    def safe_loads(json_str: str) -> Optional[Any]:
        """Safely parse JSON"""
        try:
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            return None

    @staticmethod
    def safe_dumps(obj: Any, indent: int = 2) -> str:
        """Safely serialize to JSON"""
        try:
            return json.dumps(obj, indent=indent, default=str)
        except (TypeError, ValueError):
            return "{}"
