"""
Prompt Manager - Create/Edit Prompt Page
"""

import streamlit as st

from database import Database, Variable
from services import PromptService, VariableParser
from components import (
    title_input,
    content_editor,
    category_input,
    tags_input,
    variable_editor,
    toast_success,
    toast_error,
)
from utils import ValidationUtil
from config import DEFAULT_CATEGORIES


def initialize_session_state() -> None:
    """Initialize session state variables"""
    if "edit_prompt_id" not in st.session_state:
        st.session_state.edit_prompt_id = None
    if "form_title" not in st.session_state:
        st.session_state.form_title = ""
    if "form_content" not in st.session_state:
        st.session_state.form_content = ""
    if "form_category" not in st.session_state:
        st.session_state.form_category = DEFAULT_CATEGORIES[0]
    if "form_tags" not in st.session_state:
        st.session_state.form_tags = []
    if "form_variables" not in st.session_state:
        st.session_state.form_variables = []


def render_editor() -> None:
    """Render create/edit page"""
    db = Database()
    prompt_service = PromptService(db)

    # Determine if editing or creating
    is_editing = st.session_state.edit_prompt_id is not None

    if is_editing:
        st.title("✏️ Edit Prompt")
        prompt = db.get_prompt(st.session_state.edit_prompt_id)
        if not prompt:
            st.error("Prompt not found")
            return

        # Load prompt data into form
        st.session_state.form_title = prompt.title
        st.session_state.form_content = prompt.content
        st.session_state.form_category = prompt.category
        st.session_state.form_tags = prompt.tags
        st.session_state.form_variables = prompt.variables
    else:
        st.title("➕ Create New Prompt")

    # Get categories and tags
    existing_categories = db.get_all_categories()
    all_categories = sorted(set(DEFAULT_CATEGORIES + existing_categories))
    existing_tags = db.get_all_tags()

    # Form columns
    col1, col2 = st.columns([2, 1])

    with col1:
        # Title input
        title = title_input(
            value=st.session_state.form_title,
            key="title_input",
        )
        st.session_state.form_title = title

    with col2:
        # Category input
        category = category_input(
            categories=all_categories,
            value=st.session_state.form_category,
            key="category_input",
        )
        st.session_state.form_category = category

    # Content editor
    content = content_editor(
        value=st.session_state.form_content,
        key="content_input",
    )
    st.session_state.form_content = content

    # Tags input
    tags = tags_input(
        existing_tags=existing_tags,
        selected_tags=st.session_state.form_tags,
        key="tags_input",
    )
    st.session_state.form_tags = tags

    st.divider()

    # Auto-detect variables
    detected_vars = VariableParser.auto_detect_variables(content)

    # Variable editor
    if detected_vars:
        edited_vars = variable_editor(
            variables=detected_vars,
            prompt_content=content,
            key_prefix="var_editor",
        )
        st.session_state.form_variables = edited_vars
    else:
        st.info("ℹ️ No variables detected. Use {{variable_name}} in your content.")

    st.divider()

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("💾 Save Prompt", use_container_width=True):
            # Validate
            is_valid, error_msg = ValidationUtil.validate_prompt_data(
                title=st.session_state.form_title,
                content=st.session_state.form_content,
                category=st.session_state.form_category,
            )

            if not is_valid:
                toast_error(error_msg)
            else:
                try:
                    if is_editing:
                        # Update existing prompt
                        prompt_service.update_prompt(
                            st.session_state.edit_prompt_id,
                            title=st.session_state.form_title,
                            content=st.session_state.form_content,
                            category=st.session_state.form_category,
                            tags=st.session_state.form_tags,
                            variables=st.session_state.form_variables,
                        )
                        toast_success("Prompt updated successfully!")
                    else:
                        # Create new prompt
                        prompt_service.create_prompt(
                            title=st.session_state.form_title,
                            content=st.session_state.form_content,
                            category=st.session_state.form_category,
                            tags=st.session_state.form_tags,
                            variables=st.session_state.form_variables,
                        )
                        toast_success("Prompt created successfully!")

                    # Reset form and redirect
                    st.session_state.form_title = ""
                    st.session_state.form_content = ""
                    st.session_state.form_category = DEFAULT_CATEGORIES[0]
                    st.session_state.form_tags = []
                    st.session_state.form_variables = []
                    st.session_state.edit_prompt_id = None

                    import time

                    time.sleep(1)
                    st.switch_page("pages/1_🏠_Home.py")

                except Exception as e:
                    toast_error(f"Error saving prompt: {str(e)}")

    with col2:
        if st.button("🔄 Reset Form", use_container_width=True):
            st.session_state.form_title = ""
            st.session_state.form_content = ""
            st.session_state.form_category = DEFAULT_CATEGORIES[0]
            st.session_state.form_tags = []
            st.session_state.form_variables = []
            st.rerun()

    with col3:
        if st.button("🏠 Back", use_container_width=True):
            st.session_state.edit_prompt_id = None
            st.switch_page("pages/1_🏠_Home.py")


if __name__ == "__main__":
    initialize_session_state()
    render_editor()
