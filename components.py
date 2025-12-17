"""
Prompt Manager - Reusable UI Components
"""

from typing import Callable, Dict, List, Optional
import streamlit as st

from database import Prompt, Variable, VariableType


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_color_for_tag(tag_name: str) -> str:
    """Generate a consistent color for a tag"""
    colors = [
        "#DBEAFE",  # Light blue
        "#DBEAFE",  # Light purple
        "#FCE7F3",  # Light pink
        "#DCFCE7",  # Light green
        "#FEF3C7",  # Light yellow
        "#F3E8FF",  # Light purple
    ]
    # Use hash to ensure same tag always gets same color
    hash_val = hash(tag_name) % len(colors)
    return colors[hash_val]


# ============================================================================
# SEARCH & FILTER COMPONENTS
# ============================================================================

def search_bar(
    placeholder: str = "Search prompts...",
    key: Optional[str] = None,
) -> str:
    """
    Search input component
    
    Args:
        placeholder: Placeholder text
        key: Streamlit key
        
    Returns:
        Search query text
    """
    query = st.text_input(
        "🔍 Search",
        placeholder=placeholder,
        key=key,
        label_visibility="collapsed",
    )
    return query.strip()


def category_filter(
    categories: List[str],
    key: Optional[str] = None,
) -> Optional[str]:
    """
    Category filter select component
    
    Args:
        categories: List of available categories
        key: Streamlit key
        
    Returns:
        Selected category or None for all
    """
    options = ["All Categories"] + sorted(categories)
    selected = st.selectbox(
        "Category",
        options=options,
        key=key,
        label_visibility="collapsed",
    )
    return None if selected == "All Categories" else selected


def tag_filter(
    all_tags: List[str],
    key: Optional[str] = None,
) -> List[str]:
    """
    Tag filter multiselect component
    
    Args:
        all_tags: List of available tags
        key: Streamlit key
        
    Returns:
        List of selected tags
    """
    selected = st.multiselect(
        "Filter by tags",
        options=sorted(all_tags),
        key=key,
    )
    return selected


def favorites_toggle(
    key: Optional[str] = None,
) -> bool:
    """
    Favorites only toggle
    
    Args:
        key: Streamlit key
        
    Returns:
        Whether favorites only is enabled
    """
    return st.checkbox(
        "⭐ Favorites only",
        key=key,
    )


# ============================================================================
# PROMPT CARD COMPONENT
# ============================================================================

def prompt_card(
    prompt: Prompt,
    on_select: Callable[[str], None],
    on_favorite: Callable[[str], None],
    show_full_content: bool = False,
) -> None:
    """
    Display a single prompt as a card
    
    Args:
        prompt: Prompt object to display
        on_select: Callback when card is clicked
        on_favorite: Callback when favorite button is clicked
        show_full_content: Whether to show full content or truncated
    """
    with st.container(border=True):
        col1, col2 = st.columns([1, 0.08])
        
        with col1:
            # Title and header
            st.subheader(prompt.title, anchor=False)
            
            # Category and stats
            col_cat, col_use, col_time = st.columns([1, 1, 1])
            with col_cat:
                st.caption(f"📁 {prompt.category}")
            with col_use:
                st.caption(f"✓ Used {prompt.use_count}x")
            with col_time:
                created_date = prompt.created_at.split("T")[0]
                st.caption(f"📅 {created_date}")
            
            # Tags
            if prompt.tags:
                tag_cols = st.columns(len(prompt.tags))
                for i, tag in enumerate(prompt.tags):
                    with tag_cols[i]:
                        st.markdown(
                            f"""<span class="badge">{tag}</span>""",
                            unsafe_allow_html=True,
                        )
            
            # Content preview
            content_display = prompt.content
            if not show_full_content and len(prompt.content) > 200:
                content_display = prompt.content[:200] + "..."
            
            st.markdown(content_display)
            
            # Variables info
            if prompt.variables:
                var_names = ", ".join([f"{{{{" + v.name + "}}}}" for v in prompt.variables])
                st.caption(f"Variables: {var_names}")
            
            # Action buttons
            col_use_btn, col_edit_btn, col_delete_btn = st.columns(3)
            with col_use_btn:
                if st.button("▶️ Use", key=f"use_{prompt.id}", use_container_width=True):
                    on_select(prompt.id)
            with col_edit_btn:
                if st.button("✏️ Edit", key=f"edit_{prompt.id}", use_container_width=True):
                    st.session_state.edit_prompt_id = prompt.id
                    st.rerun()
        
        # Favorite button
        with col2:
            fav_icon = "★" if prompt.is_favorite else "☆"
            if st.button(fav_icon, key=f"fav_{prompt.id}", help="Toggle favorite"):
                on_favorite(prompt.id)


# ============================================================================
# VARIABLE FORM COMPONENT
# ============================================================================

def variable_form(
    prompt: Prompt,
) -> Dict[str, str]:
    """
    Create a form for filling in prompt variables
    
    Args:
        prompt: Prompt with variables
        
    Returns:
        Dictionary of variable_name -> value
    """
    values = {}
    
    if not prompt.variables:
        st.info("This prompt has no variables.")
        return values
    
    for variable in prompt.variables:
        if variable.type == VariableType.TEXT:
            values[variable.name] = st.text_input(
                label=variable.name,
                value=variable.default_value or "",
                key=f"var_{prompt.id}_{variable.name}",
            )
        
        elif variable.type == VariableType.TEXTAREA:
            values[variable.name] = st.text_area(
                label=variable.name,
                value=variable.default_value or "",
                key=f"var_{prompt.id}_{variable.name}",
                height=120,
            )
        
        elif variable.type == VariableType.SELECT:
            if variable.options:
                values[variable.name] = st.selectbox(
                    label=variable.name,
                    options=variable.options,
                    index=0 if not variable.default_value else variable.options.index(
                        variable.default_value
                    ),
                    key=f"var_{prompt.id}_{variable.name}",
                )
            else:
                st.error(f"Select variable '{variable.name}' has no options")
        
        elif variable.type == VariableType.NUMBER:
            values[variable.name] = str(
                st.number_input(
                    label=variable.name,
                    value=float(variable.default_value or 0),
                    key=f"var_{prompt.id}_{variable.name}",
                )
            )
    
    return values


# ============================================================================
# TEXT EDITOR COMPONENTS
# ============================================================================

def title_input(
    value: str = "",
    key: Optional[str] = None,
) -> str:
    """Prompt title input"""
    return st.text_input(
        label="Title",
        value=value,
        key=key,
        placeholder="Enter prompt title",
    )


def content_editor(
    value: str = "",
    key: Optional[str] = None,
) -> str:
    """Prompt content text area with variable hint"""
    st.caption("💡 Use {{variable_name}} for dynamic content")
    return st.text_area(
        label="Content",
        value=value,
        key=key,
        placeholder="Enter prompt content. Use {{variable_name}} for placeholders.",
        height=300,
    )


def category_input(
    categories: List[str],
    value: Optional[str] = None,
    key: Optional[str] = None,
) -> str:
    """Category select or create new"""
    options = sorted(categories) + ["➕ Create new category"]
    selected = st.selectbox(
        label="Category",
        options=options,
        index=sorted(categories).index(value) if value in sorted(categories) else 0,
        key=key,
    )
    
    if selected == "➕ Create new category":
        return st.text_input("New category name", placeholder="e.g., 'Marketing'")
    
    return selected


def tags_input(
    existing_tags: List[str],
    selected_tags: Optional[List[str]] = None,
    key: Optional[str] = None,
) -> List[str]:
    """Tag input/selection"""
    return st.multiselect(
        label="Tags",
        options=sorted(existing_tags),
        default=selected_tags or [],
        key=key,
        help="Select existing tags or type to create new ones",
    )


# ============================================================================
# VARIABLE DEFINITION COMPONENT
# ============================================================================

def variable_editor(
    variables: List[Variable],
    prompt_content: str,
    key_prefix: str = "var_editor",
) -> List[Variable]:
    """
    Editor for creating/editing variable definitions
    
    Args:
        variables: Existing variables
        prompt_content: Prompt content (for auto-detection)
        key_prefix: Prefix for Streamlit keys
        
    Returns:
        Updated list of variables
    """
    st.subheader("Variables")
    
    # Display detected variables from content
    st.caption("Detected variables from content:")
    cols = st.columns(len(variables) if variables else 1)
    for i, var in enumerate(variables):
        with cols[i] if len(variables) <= 5 else st.container():
            st.write(f"• {{{{" + var.name + "}}}}")
    
    updated_variables = []
    
    for i, variable in enumerate(variables):
        with st.expander(f"✏️ {variable.name}", expanded=False):
            var_type = st.selectbox(
                label="Type",
                options=[t.value for t in VariableType],
                index=list(VariableType).index(VariableType(variable.type)),
                key=f"{key_prefix}_type_{i}",
            )
            
            default_value = st.text_input(
                label="Default value",
                value=variable.default_value or "",
                key=f"{key_prefix}_default_{i}",
            )
            
            options = None
            if var_type == VariableType.SELECT.value:
                options_text = st.text_area(
                    label="Options (one per line)",
                    value="\n".join(variable.options or []),
                    key=f"{key_prefix}_options_{i}",
                    height=100,
                )
                options = [o.strip() for o in options_text.split("\n") if o.strip()]
            
            updated_variables.append(
                Variable(
                    name=variable.name,
                    type=var_type,
                    default_value=default_value or None,
                    options=options,
                )
            )
    
    return updated_variables


# ============================================================================
# TOAST/NOTIFICATION COMPONENTS
# ============================================================================

def toast_success(message: str) -> None:
    """Show success notification"""
    st.success(message)


def toast_error(message: str) -> None:
    """Show error notification"""
    st.error(message)


def toast_info(message: str) -> None:
    """Show info notification"""
    st.info(message)


def toast_warning(message: str) -> None:
    """Show warning notification"""
    st.warning(message)


# ============================================================================
# DIALOG/MODAL COMPONENTS
# ============================================================================

def confirm_dialog(
    title: str,
    message: str,
) -> bool:
    """
    Show confirmation dialog
    
    Args:
        title: Dialog title
        message: Dialog message
        
    Returns:
        True if confirmed, False otherwise
    """
    with st.container(border=True):
        st.warning(f"⚠️ {title}")
        st.write(message)
        
        col1, col2 = st.columns(2)
        with col1:
            confirm = st.button("Confirm", use_container_width=True)
        with col2:
            cancel = st.button("Cancel", use_container_width=True)
        
        if confirm:
            return True
        if cancel:
            return False
    
    return False


# ============================================================================
# STATISTICS DISPLAY
# ============================================================================

def stats_display(stats: Dict[str, int]) -> None:
    """Display database statistics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Prompts", stats.get("total_prompts", 0))
    
    with col2:
        st.metric("Favorites", stats.get("total_favorites", 0))
    
    with col3:
        st.metric("Tags", stats.get("total_tags", 0))
    
    with col4:
        st.metric("Total Uses", stats.get("total_uses", 0))


# ============================================================================
# EMPTY STATE
# ============================================================================

def empty_state(
    icon: str = "📭",
    title: str = "No prompts found",
    message: str = "Create your first prompt to get started.",
) -> None:
    """Display empty state message"""
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"<h2 style='text-align: center'>{icon}</h2>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center'>{title}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center'>{message}</p>", unsafe_allow_html=True)
