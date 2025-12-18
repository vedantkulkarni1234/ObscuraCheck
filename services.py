"""
Prompt Manager - Business Logic Services
"""

import json
import re
import math
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid

import networkx as nx
import numpy as np

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

    @staticmethod
    def get_missing_variables(content: str, values: Dict[str, str]) -> List[str]:
        """
        Get list of variables that have empty/missing values
        
        Args:
            content: Prompt content with variables
            values: Dictionary of variable_name -> value
            
        Returns:
            List of variable names with missing/empty values
        """
        extracted_vars = VariableParser.extract_variables(content)
        missing = []
        for var_name in extracted_vars:
            if not values.get(var_name, "").strip():
                missing.append(var_name)
        return missing

    @staticmethod
    def generate_live_preview(
        content: str, values: Dict[str, str], show_missing: bool = True
    ) -> Tuple[str, List[str]]:
        """
        Generate live preview with variable substitution
        
        Args:
            content: Prompt content with variables
            values: Dictionary of variable_name -> value
            show_missing: Whether to highlight missing variables
            
        Returns:
            (preview_text, list_of_missing_variables)
        """
        missing = VariableParser.get_missing_variables(content, values)
        preview = VariableParser.substitute_variables(content, values)
        return preview, missing


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
# GALAXY SERVICE (3D KNOWLEDGE GRAPH)
# ============================================================================

class GalaxyService:
    """
    3D Knowledge Graph visualization service
    Creates an interactive galaxy of prompts with clustering based on similarity
    """

    def __init__(self, db: Database) -> None:
        """Initialize with database instance"""
        self.db = db

    def calculate_similarity_score(self, prompt1: Prompt, prompt2: Prompt) -> float:
        """
        Calculate similarity between two prompts based on tags and categories
        
        Args:
            prompt1: First prompt
            prompt2: Second prompt
            
        Returns:
            Similarity score between 0 and 1
        """
        score = 0.0

        # Category similarity (high weight)
        if prompt1.category and prompt2.category:
            if prompt1.category == prompt2.category:
                score += 0.4

        # Tags similarity (medium weight)
        if prompt1.tags and prompt2.tags:
            common_tags = set(prompt1.tags) & set(prompt2.tags)
            total_tags = set(prompt1.tags) | set(prompt2.tags)
            if total_tags:
                score += 0.5 * (len(common_tags) / len(total_tags))

        # Title similarity (low weight)
        if prompt1.title and prompt2.title:
            # Simple word overlap similarity
            words1 = set(prompt1.title.lower().split())
            words2 = set(prompt2.title.lower().split())
            if words1 and words2:
                common_words = words1 & words2
                total_words = words1 | words2
                score += 0.1 * (len(common_words) / len(total_words))

        return min(score, 1.0)

    def create_galaxy_data(self) -> Dict:
        """
        Create 3D positioning data for all prompts in the galaxy
        
        Returns:
            Dictionary with node positions, edges, and metadata
        """
        prompts = self.db.get_all_prompts()
        
        if not prompts:
            return {
                "nodes": [],
                "edges": [],
                "categories": {},
                "stats": {"total_prompts": 0}
            }

        # Create similarity graph
        G = nx.Graph()
        
        # Add nodes
        for i, prompt in enumerate(prompts):
            G.add_node(i, prompt=prompt)

        # Add edges based on similarity
        similarity_threshold = 0.1  # Minimum similarity to connect
        for i in range(len(prompts)):
            for j in range(i + 1, len(prompts)):
                similarity = self.calculate_similarity_score(prompts[i], prompts[j])
                if similarity >= similarity_threshold:
                    G.add_edge(i, j, weight=similarity)

        # Calculate 3D positions using force-directed layout
        if len(G.nodes()) > 0:
            # Use spring layout with 3D extension
            pos_2d = nx.spring_layout(G, k=3, iterations=50, seed=42)
            
            # Convert to 3D and add depth variations
            positions = {}
            for node, (x, y) in pos_2d.items():
                # Add depth based on category and usage patterns
                prompt = prompts[node]
                
                # Calculate depth based on usage and favorites
                base_depth = 0
                if prompt.is_favorite:
                    base_depth += 2
                if prompt.use_count > 0:
                    base_depth += min(prompt.use_count / 10, 3)
                
                # Add some randomness for visual appeal
                z = base_depth + random.uniform(-1, 1)
                
                # Scale and center positions
                positions[node] = (x * 10, y * 10, z * 5)

            # If no edges (isolated nodes), create circular layout
            if not G.edges():
                for i in range(len(prompts)):
                    angle = 2 * math.pi * i / len(prompts)
                    radius = max(5, len(prompts) * 0.5)
                    x = radius * math.cos(angle)
                    y = radius * math.sin(angle)
                    z = random.uniform(-2, 2)
                    positions[i] = (x, y, z)
        else:
            positions = {}

        # Prepare node data for visualization
        nodes = []
        categories = set()
        for i, prompt in enumerate(prompts):
            categories.add(prompt.category)
            pos = positions.get(i, (0, 0, 0))
            
            # Node size based on usage and favorites
            base_size = 8
            if prompt.is_favorite:
                base_size += 4
            if prompt.use_count > 0:
                base_size += min(prompt.use_count / 2, 8)

            nodes.append({
                "id": str(prompt.id),
                "label": prompt.title,
                "category": prompt.category,
                "tags": prompt.tags,
                "is_favorite": prompt.is_favorite,
                "use_count": prompt.use_count,
                "x": pos[0],
                "y": pos[1],
                "z": pos[2],
                "size": base_size,
                "color": self._get_node_color(prompt.category, prompt.is_favorite)
            })

        # Prepare edge data for visualization
        edges = []
        for edge in G.edges(data=True):
            node1, node2, data = edge
            pos1 = positions.get(node1, (0, 0, 0))
            pos2 = positions.get(node2, (0, 0, 0))
            
            edges.append({
                "from": node1,
                "to": node2,
                "weight": data.get("weight", 0.1),
                "x1": pos1[0],
                "y1": pos1[1],
                "z1": pos1[2],
                "x2": pos2[0],
                "y2": pos2[1],
                "z2": pos2[2]
            })

        return {
            "nodes": nodes,
            "edges": edges,
            "categories": sorted(list(categories)),
            "stats": {
                "total_prompts": len(prompts),
                "total_edges": len(edges),
                "connected_components": nx.number_connected_components(G)
            }
        }

    def _get_node_color(self, category: str, is_favorite: bool) -> str:
        """
        Get color for a node based on category and favorite status
        
        Args:
            category: Prompt category
            is_favorite: Whether it's a favorite
            
        Returns:
            Color string (hex or named)
        """
        # Color palette for different categories
        color_map = {
            "Development": "#3498db",
            "Marketing": "#e74c3c", 
            "Research": "#f39c12",
            "Writing": "#9b59b6",
            "Analysis": "#1abc9c",
            "Planning": "#f1c40f",
            "Communication": "#2ecc71",
            "Documentation": "#95a5a6",
            "Testing": "#e67e22",
            "Design": "#ff69b4",
        }
        
        base_color = color_map.get(category, "#34495e")
        
        # Enhance color for favorites
        if is_favorite:
            # Make it brighter/gold
            return "#ffd700"
        
        return base_color

    def get_galaxy_statistics(self) -> Dict:
        """
        Get statistics about the current galaxy state
        
        Returns:
            Dictionary with galaxy statistics
        """
        data = self.create_galaxy_data()
        
        prompts = self.db.get_all_prompts()
        total_prompts = len(prompts)
        
        if total_prompts == 0:
            return {
                "total_prompts": 0,
                "avg_similarity": 0,
                "most_connected_category": "None",
                "cluster_count": 0
            }

        # Calculate average similarity
        total_similarity = 0
        similarity_count = 0
        
        for node in data["nodes"]:
            connected_edges = [edge for edge in data["edges"] 
                             if edge["from"] == node["id"] or edge["to"] == node["id"]]
            
            for edge in connected_edges:
                total_similarity += edge["weight"]
                similarity_count += 1

        avg_similarity = total_similarity / similarity_count if similarity_count > 0 else 0

        # Find most connected category
        category_connections = {}
        for node in data["nodes"]:
            category = node["category"]
            connected_edges = [edge for edge in data["edges"] 
                             if edge["from"] == node["id"] or edge["to"] == node["id"]]
            
            if category not in category_connections:
                category_connections[category] = 0
            category_connections[category] += len(connected_edges)

        most_connected_category = max(category_connections, key=category_connections.get) if category_connections else "None"

        return {
            "total_prompts": total_prompts,
            "avg_similarity": round(avg_similarity, 3),
            "most_connected_category": most_connected_category,
            "cluster_count": data["stats"]["connected_components"],
            "total_connections": data["stats"]["total_edges"]
        }


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
