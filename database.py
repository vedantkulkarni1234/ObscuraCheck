"""
Prompt Manager - Database Layer
Handles all SQLite operations with parameterized queries
"""

import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from config import DB_PATH, CREATE_TABLES_SQL, VariableType


# ============================================================================
# DATA MODELS (Pydantic)
# ============================================================================

class Variable(BaseModel):
    """Variable definition in a prompt"""
    name: str
    type: VariableType = VariableType.TEXT
    default_value: Optional[str] = None
    options: Optional[List[str]] = None

    class Config:
        use_enum_values = True


class Prompt(BaseModel):
    """Prompt data model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    category: str
    tags: List[str] = Field(default_factory=list)
    variables: List[Variable] = Field(default_factory=list)
    is_favorite: bool = False
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    use_count: int = 0

    class Config:
        use_enum_values = True


# ============================================================================
# DATABASE CLASS
# ============================================================================

class Database:
    """SQLite database manager with type safety"""

    def __init__(self, db_path: Path = DB_PATH) -> None:
        """Initialize database connection"""
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self) -> None:
        """Create database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executescript(CREATE_TABLES_SQL)
        conn.commit()
        conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ========================================================================
    # PROMPT OPERATIONS
    # ========================================================================

    def create_prompt(self, prompt: Prompt) -> str:
        """Create a new prompt"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Insert prompt
            cursor.execute(
                """
                INSERT INTO prompts
                (id, title, content, category, is_favorite, created_at, updated_at, use_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    prompt.id,
                    prompt.title,
                    prompt.content,
                    prompt.category,
                    int(prompt.is_favorite),
                    prompt.created_at,
                    prompt.updated_at,
                    prompt.use_count,
                ),
            )

            # Insert tags
            for tag_name in prompt.tags:
                self._ensure_tag_exists(cursor, tag_name)
                tag_id = cursor.execute(
                    "SELECT id FROM tags WHERE name = ?", (tag_name,)
                ).fetchone()[0]
                cursor.execute(
                    "INSERT OR IGNORE INTO prompt_tags (prompt_id, tag_id) VALUES (?, ?)",
                    (prompt.id, tag_id),
                )

            # Insert variables
            for variable in prompt.variables:
                var_id = str(uuid.uuid4())
                cursor.execute(
                    """
                    INSERT INTO variables
                    (id, prompt_id, name, type, default_value, options)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        var_id,
                        prompt.id,
                        variable.name,
                        variable.type,
                        variable.default_value,
                        json.dumps(variable.options) if variable.options else None,
                    ),
                )

            conn.commit()
            return prompt.id

        finally:
            conn.close()

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Get prompt
            row = cursor.execute(
                "SELECT * FROM prompts WHERE id = ?", (prompt_id,)
            ).fetchone()
            if not row:
                return None

            # Get tags
            tag_rows = cursor.execute(
                """
                SELECT t.name FROM tags t
                JOIN prompt_tags pt ON t.id = pt.tag_id
                WHERE pt.prompt_id = ?
                """,
                (prompt_id,),
            ).fetchall()
            tags = [tag_row["name"] for tag_row in tag_rows]

            # Get variables
            var_rows = cursor.execute(
                "SELECT * FROM variables WHERE prompt_id = ?", (prompt_id,)
            ).fetchall()
            variables = [
                Variable(
                    name=var_row["name"],
                    type=var_row["type"],
                    default_value=var_row["default_value"],
                    options=json.loads(var_row["options"])
                    if var_row["options"]
                    else None,
                )
                for var_row in var_rows
            ]

            return Prompt(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                category=row["category"],
                tags=tags,
                variables=variables,
                is_favorite=bool(row["is_favorite"]),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                use_count=row["use_count"],
            )

        finally:
            conn.close()

    def update_prompt(self, prompt: Prompt) -> bool:
        """Update an existing prompt"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Update prompt
            prompt.updated_at = datetime.utcnow().isoformat()
            cursor.execute(
                """
                UPDATE prompts
                SET title = ?, content = ?, category = ?, is_favorite = ?, updated_at = ?, use_count = ?
                WHERE id = ?
                """,
                (
                    prompt.title,
                    prompt.content,
                    prompt.category,
                    int(prompt.is_favorite),
                    prompt.updated_at,
                    prompt.use_count,
                    prompt.id,
                ),
            )

            # Delete existing tags and re-insert
            cursor.execute("DELETE FROM prompt_tags WHERE prompt_id = ?", (prompt.id,))
            for tag_name in prompt.tags:
                self._ensure_tag_exists(cursor, tag_name)
                tag_id = cursor.execute(
                    "SELECT id FROM tags WHERE name = ?", (tag_name,)
                ).fetchone()[0]
                cursor.execute(
                    "INSERT OR IGNORE INTO prompt_tags (prompt_id, tag_id) VALUES (?, ?)",
                    (prompt.id, tag_id),
                )

            # Delete existing variables and re-insert
            cursor.execute("DELETE FROM variables WHERE prompt_id = ?", (prompt.id,))
            for variable in prompt.variables:
                var_id = str(uuid.uuid4())
                cursor.execute(
                    """
                    INSERT INTO variables
                    (id, prompt_id, name, type, default_value, options)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        var_id,
                        prompt.id,
                        variable.name,
                        variable.type,
                        variable.default_value,
                        json.dumps(variable.options) if variable.options else None,
                    ),
                )

            conn.commit()
            return True

        finally:
            conn.close()

    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
            # Cascade delete of tags, variables handled by foreign keys
            conn.commit()
            return cursor.rowcount > 0

        finally:
            conn.close()

    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all prompts"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            rows = cursor.execute("SELECT id FROM prompts ORDER BY created_at DESC").fetchall()
            prompts = []
            for row in rows:
                prompt = self.get_prompt(row["id"])
                if prompt:
                    prompts.append(prompt)
            return prompts

        finally:
            conn.close()

    def search_prompts(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        favorites_only: bool = False,
    ) -> List[Prompt]:
        """Search and filter prompts"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            sql = "SELECT DISTINCT p.id FROM prompts p"
            params: List[Any] = []

            # Build WHERE clause
            conditions = []

            if query:
                sql += " LEFT JOIN variables v ON p.id = v.prompt_id"
                conditions.append(
                    "(p.title LIKE ? OR p.content LIKE ? OR v.name LIKE ?)"
                )
                search_term = f"%{query}%"
                params.extend([search_term, search_term, search_term])

            if tags:
                sql += " JOIN prompt_tags pt ON p.id = pt.prompt_id JOIN tags t ON pt.tag_id = t.id"
                placeholders = ",".join("?" * len(tags))
                conditions.append(f"t.name IN ({placeholders})")
                params.extend(tags)

            if category:
                conditions.append("p.category = ?")
                params.append(category)

            if favorites_only:
                conditions.append("p.is_favorite = 1")

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += " ORDER BY p.created_at DESC"

            rows = cursor.execute(sql, params).fetchall()
            prompts = []
            for row in rows:
                prompt = self.get_prompt(row["id"])
                if prompt:
                    prompts.append(prompt)
            return prompts

        finally:
            conn.close()

    # ========================================================================
    # TAG OPERATIONS
    # ========================================================================

    def _ensure_tag_exists(self, cursor: sqlite3.Cursor, tag_name: str) -> str:
        """Ensure a tag exists, create if not"""
        tag_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT OR IGNORE INTO tags (id, name) VALUES (?, ?)",
            (tag_id, tag_name),
        )
        row = cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,)).fetchone()
        return row[0]

    def get_all_tags(self) -> List[str]:
        """Get all unique tags"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            rows = cursor.execute(
                "SELECT DISTINCT name FROM tags ORDER BY name"
            ).fetchall()
            return [row["name"] for row in rows]

        finally:
            conn.close()

    def get_tags_for_prompt(self, prompt_id: str) -> List[str]:
        """Get tags for a specific prompt"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            rows = cursor.execute(
                """
                SELECT t.name FROM tags t
                JOIN prompt_tags pt ON t.id = pt.tag_id
                WHERE pt.prompt_id = ?
                ORDER BY t.name
                """,
                (prompt_id,),
            ).fetchall()
            return [row["name"] for row in rows]

        finally:
            conn.close()

    # ========================================================================
    # CATEGORY OPERATIONS
    # ========================================================================

    def get_all_categories(self) -> List[str]:
        """Get all unique categories"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            rows = cursor.execute(
                "SELECT DISTINCT category FROM prompts ORDER BY category"
            ).fetchall()
            return [row["category"] for row in rows]

        finally:
            conn.close()

    # ========================================================================
    # STATISTICS
    # ========================================================================

    def increment_use_count(self, prompt_id: str) -> bool:
        """Increment use count for a prompt"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE prompts SET use_count = use_count + 1 WHERE id = ?",
                (prompt_id,),
            )
            conn.commit()
            return cursor.rowcount > 0

        finally:
            conn.close()

    def toggle_favorite(self, prompt_id: str) -> bool:
        """Toggle favorite status"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE prompts SET is_favorite = 1 - is_favorite WHERE id = ?",
                (prompt_id,),
            )
            conn.commit()
            return cursor.rowcount > 0

        finally:
            conn.close()

    def get_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            total_prompts = cursor.execute("SELECT COUNT(*) as count FROM prompts").fetchone()[
                0
            ]
            total_favorites = cursor.execute(
                "SELECT COUNT(*) as count FROM prompts WHERE is_favorite = 1"
            ).fetchone()[0]
            total_tags = cursor.execute("SELECT COUNT(*) as count FROM tags").fetchone()[0]
            total_uses = cursor.execute(
                "SELECT SUM(use_count) as total FROM prompts"
            ).fetchone()[0]

            return {
                "total_prompts": total_prompts,
                "total_favorites": total_favorites,
                "total_tags": total_tags,
                "total_uses": total_uses or 0,
            }

        finally:
            conn.close()

    # ========================================================================
    # IMPORT/EXPORT
    # ========================================================================

    def export_to_json(self) -> str:
        """Export all prompts to JSON string"""
        prompts = self.get_all_prompts()
        return json.dumps(
            [prompt.dict() for prompt in prompts],
            indent=2,
            default=str,
        )

    def import_from_json(self, json_str: str) -> int:
        """Import prompts from JSON string"""
        data = json.loads(json_str)
        if not isinstance(data, list):
            raise ValueError("Invalid JSON format: expected array of prompts")

        count = 0
        for item in data:
            try:
                prompt = Prompt(**item)
                # Regenerate ID to avoid conflicts
                prompt.id = str(uuid.uuid4())
                self.create_prompt(prompt)
                count += 1
            except Exception as e:
                # Log error but continue with other prompts
                print(f"Error importing prompt: {e}")
                continue

        return count
