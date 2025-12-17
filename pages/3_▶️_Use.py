"""
Prompt Manager - Use Prompt Page (Fill Variables & Copy)
"""

import streamlit as st

from database import Database
from services import PromptService, VariableParser
from components import (
    variable_form,
    toast_success,
    toast_error,
    toast_info,
)
from utils import DateTimeUtil


def initialize_session_state() -> None:
    """Initialize session state variables"""
    if "selected_prompt_id" not in st.session_state:
        st.session_state.selected_prompt_id = None
    if "filled_variables" not in st.session_state:
        st.session_state.filled_variables = {}


def render_viewer() -> None:
    """Render use prompt page"""
    if not st.session_state.selected_prompt_id:
        st.info("Select a prompt from the home page to use it.")
        if st.button("← Go Back to Home"):
            st.switch_page("pages/1_🏠_Home.py")
        return

    db = Database()
    prompt_service = PromptService(db)

    prompt = prompt_service.get_prompt(st.session_state.selected_prompt_id)
    if not prompt:
        st.error("Prompt not found")
        if st.button("← Go Back"):
            st.session_state.selected_prompt_id = None
            st.switch_page("pages/1_🏠_Home.py")
        return

    # Page header
    st.title(f"▶️ Use: {prompt.title}")

    # Prompt details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📁 Category: {prompt.category}")
    with col2:
        created_date = DateTimeUtil.format_date(prompt.created_at)
        st.caption(f"📅 Created: {created_date}")
    with col3:
        st.caption(f"✓ Used {prompt.use_count}x")

    # Tags
    if prompt.tags:
        tag_str = ", ".join(prompt.tags)
        st.caption(f"🏷️ Tags: {tag_str}")

    st.divider()

    # Original prompt content
    with st.expander("📄 Original Prompt"):
        st.markdown(prompt.content)

    st.divider()

    # Variable form
    if prompt.variables:
        st.subheader("📝 Fill in Variables")

        filled_vars = variable_form(prompt)
        st.session_state.filled_variables = filled_vars

        st.divider()

        # Generate result
        st.subheader("🎯 Final Prompt")

        try:
            result = VariableParser.substitute_variables(
                prompt.content, filled_vars
            )

            # Display result
            st.markdown(result)

            # Copy to clipboard button
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    try:
                        import pyperclip

                        pyperclip.copy(result)
                        toast_success("Copied to clipboard!")
                    except Exception as e:
                        st.warning(
                            f"Could not copy to clipboard: {e}\n\nPlease copy manually from the text above."
                        )

            with col2:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state.filled_variables = {}
                    st.rerun()

        except Exception as e:
            toast_error(f"Error generating prompt: {str(e)}")

    else:
        st.info("This prompt has no variables.")
        st.markdown(prompt.content)

        if st.button("📋 Copy to Clipboard", use_container_width=True):
            try:
                import pyperclip

                pyperclip.copy(prompt.content)
                toast_success("Copied to clipboard!")
            except Exception as e:
                st.warning(
                    f"Could not copy to clipboard: {e}\n\nPlease copy manually from the text above."
                )

    st.divider()

    # Action buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✏️ Edit", use_container_width=True):
            st.session_state.edit_prompt_id = st.session_state.selected_prompt_id
            st.switch_page("pages/2_✏️_Create.py")

    with col2:
        if st.button("🗑️ Delete", use_container_width=True):
            try:
                prompt_service.delete_prompt(st.session_state.selected_prompt_id)
                toast_success("Prompt deleted!")
                st.session_state.selected_prompt_id = None
                import time

                time.sleep(1)
                st.switch_page("pages/1_🏠_Home.py")
            except Exception as e:
                toast_error(f"Error deleting prompt: {str(e)}")

    with col3:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.selected_prompt_id = None
            st.switch_page("pages/1_🏠_Home.py")


if __name__ == "__main__":
    initialize_session_state()
    render_viewer()
