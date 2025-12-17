"""
Prompt Manager - Business Logic Services
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid

from database import Database, Prompt, Variable, VariableType
from config import EXPORT_FILENAME_FORMAT


# ============================================================================
# VARIABLE PARSER SERVICE
# ============================================================================

class VariableParser:
    """Parse and extract variables from prompt content"""

    @staticmethod
    def extract_variables(content: str) -> List[str]:
        """
        Extract all variable names from content ({{variable_name}} syntax)
        
        Args:
            content: Prompt content with variables
            
        Returns:
            List of unique variable names found
        """
        pattern = r"\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}"
        matches = re.findall(pattern, content)
        return list(dict.fromkeys(matches))  # Remove duplicates while preserving order

    @staticmethod
    def substitute_variables(content: str, values: Dict[str, str]) -> str:
        """
        Replace variables in content with provided values
        
        Args:
            content: Prompt content with variables
            values: Dictionary of variable_name -> value
            
        Returns:
            Content with variables substituted
        """
        result = content
        for var_name, var_value in values.items():
            pattern = r"\{\{" + re.escape(var_name) + r"\}\}"
            result = re.sub(pattern, str(var_value), result)
        return result

    @staticmethod
    def auto_detect_variables(
        content: str, existing_variables: Optional[List[Variable]] = None
    ) -> List[Variable]:
        """
        Auto-detect variables from content and merge with existing definitions
        
        Args:
            content: Prompt content
            existing_variables: Previously defined variables (optional)
            
        Returns:
            List of Variable objects with auto-detected ones added
        """
        extracted_names = VariableParser.extract_variables(content)
        existing_dict = {
            v.name: v for v in (existing_variables or [])
        }

        result = []
        for name in extracted_names:
            if name in existing_dict:
                result.append(existing_dict[name])
            else:
                result.append(
                    Variable(
                        name=name,
                        type=VariableType.TEXT,
                        default_value="",
                    )
                )

        return result


# ============================================================================
# PROMPT SERVICE
# ============================================================================

class PromptService:
    """High-level prompt operations"""

    def __init__(self, db: Database) -> None:
        """Initialize with database instance"""
        self.db = db

    def create_prompt(
        self,
        title: str,
        content: str,
        category: str,
        tags: Optional[List[str]] = None,
        variables: Optional[List[Variable]] = None,
    ) -> Prompt:
        """
        Create a new prompt
        
        Args:
            title: Prompt title
            content: Prompt content with {{variable}} placeholders
            category: Category name
            tags: Optional list of tags
            variables: Optional list of Variable definitions
            
        Returns:
            Created Prompt object
        """
        # Auto-detect variables if not provided
        if variables is None:
            variables = VariableParser.auto_detect_variables(content)

        prompt = Prompt(
            title=title,
            content=content,
            category=category,
            tags=tags or [],
            variables=variables,
        )

        prompt_id = self.db.create_prompt(prompt)
        return self.db.get_prompt(prompt_id)

    def update_prompt(self, prompt_id: str, **kwargs) -> Optional[Prompt]:
        """
        Update prompt fields
        
        Args:
            prompt_id: Prompt ID to update
            **kwargs: Fields to update (title, content, category, tags, variables, is_favorite)
            
        Returns:
            Updated Prompt or None if not found
        """
        prompt = self.db.get_prompt(prompt_id)
        if not prompt:
            return None

        for key, value in kwargs.items():
            if key == "variables" and value is not None:
                prompt.variables = value
            elif hasattr(prompt, key):
                setattr(prompt, key, value)

        self.db.update_prompt(prompt)
        return self.db.get_prompt(prompt_id)

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Get prompt by ID"""
        return self.db.get_prompt(prompt_id)

    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt"""
        return self.db.delete_prompt(prompt_id)

    def list_prompts(
        self,
        search_query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        favorites_only: bool = False,
    ) -> List[Prompt]:
        """
        List prompts with optional filtering
        
        Args:
            search_query: Text to search in title/content/variables
            category: Filter by category
            tags: Filter by any of these tags
            favorites_only: Only return favorites
            
        Returns:
            List of matching prompts
        """
        return self.db.search_prompts(
            query=search_query,
            category=category,
            tags=tags,
            favorites_only=favorites_only,
        )

    def toggle_favorite(self, prompt_id: str) -> bool:
        """Toggle favorite status"""
        return self.db.toggle_favorite(prompt_id)

    def use_prompt(self, prompt_id: str, substitutions: Dict[str, str]) -> Optional[str]:
        """
        Generate final prompt text by substituting variables
        
        Args:
            prompt_id: Prompt ID to use
            substitutions: Variable name -> value mapping
            
        Returns:
            Final prompt text or None if prompt not found
        """
        prompt = self.db.get_prompt(prompt_id)
        if not prompt:
            return None

        # Increment use count
        self.db.increment_use_count(prompt_id)

        # Substitute variables
        return VariableParser.substitute_variables(prompt.content, substitutions)


# ============================================================================
# FILTER SERVICE
# ============================================================================

class FilterService:
    """Filtering and faceting operations"""

    def __init__(self, db: Database) -> None:
        """Initialize with database instance"""
        self.db = db

    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return self.db.get_all_categories()

    def get_tags(self) -> List[str]:
        """Get all available tags"""
        return self.db.get_all_tags()

    def get_facet_counts(
        self, search_query: str = "", initial_tags: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, int]]:
        """
        Get facet counts for current search (categories and tags with counts)
        
        Args:
            search_query: Current search query
            initial_tags: Tags already applied
            
        Returns:
            {"categories": {name: count}, "tags": {name: count}}
        """
        # Get all matching prompts
        prompts = self.db.search_prompts(query=search_query, tags=initial_tags)

        categories = {}
        tags = {}

        for prompt in prompts:
            # Count categories
            categories[prompt.category] = categories.get(prompt.category, 0) + 1

            # Count tags
            for tag in prompt.tags:
                tags[tag] = tags.get(tag, 0) + 1

        return {
            "categories": categories,
            "tags": tags,
        }


# ============================================================================
# IMPORT/EXPORT SERVICE
# ============================================================================

class ImportExportService:
    """Handle import/export operations"""

    def __init__(self, db: Database) -> None:
        """Initialize with database instance"""
        self.db = db

    def export_prompts(self) -> Tuple[str, str]:
        """
        Export all prompts as JSON
        
        Returns:
            (json_content, suggested_filename)
        """
        json_content = self.db.export_to_json()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = EXPORT_FILENAME_FORMAT.format(timestamp=timestamp)
        return json_content, filename

    def import_prompts(self, json_content: str) -> Tuple[int, Optional[str]]:
        """
        Import prompts from JSON
        
        Args:
            json_content: JSON string with prompts
            
        Returns:
            (count_imported, error_message or None)
        """
        try:
            count = self.db.import_from_json(json_content)
            return count, None
        except json.JSONDecodeError as e:
            return 0, f"Invalid JSON: {str(e)}"
        except ValueError as e:
            return 0, str(e)
        except Exception as e:
            return 0, f"Import error: {str(e)}"

    def get_export_sample(self) -> str:
        """Get sample JSON for documentation"""
        sample_prompts = [
            {
                "id": str(uuid.uuid4()),
                "title": "Code Review Request",
                "content": "Please review this {{language}} code:\n\n```\n{{code}}\n```\n\nFocus on {{focus_area}}.",
                "category": "Development",
                "tags": ["code-review", "programming"],
                "variables": [
                    {
                        "name": "language",
                        "type": "select",
                        "default_value": "Python",
                        "options": ["Python", "JavaScript", "Go", "Rust"],
                    },
                    {
                        "name": "code",
                        "type": "textarea",
                        "default_value": "",
                    },
                    {
                        "name": "focus_area",
                        "type": "text",
                        "default_value": "performance",
                    },
                ],
                "is_favorite": False,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "use_count": 0,
            }
        ]
        return json.dumps(sample_prompts, indent=2, default=str)


# ============================================================================
# CLIPBOARD SERVICE
# ============================================================================

class ClipboardService:
    """Handle clipboard operations"""

    @staticmethod
    def format_for_clipboard(text: str) -> str:
        """
        Format text for clipboard copying
        
        Args:
            text: Text to format
            
        Returns:
            Formatted text (may normalize line endings, trim, etc.)
        """
        return text.strip()

    @staticmethod
    def get_copy_command(text: str) -> str:
        """
        Generate platform-specific copy command
        
        Args:
            text: Text to copy
            
        Returns:
            Command that would copy to clipboard
        """
        # Note: Actual clipboard operations handled by streamlit-copy-to-clipboard
        # This is just helper for formatting/info
        return f"Copy {len(text)} characters to clipboard"
