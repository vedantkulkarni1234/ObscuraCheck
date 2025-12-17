"""
Prompt Manager - Home Page (Browse & Search)
"""

import streamlit as st

from database import Database
from services import PromptService, FilterService
from components import (
    search_bar,
    category_filter,
    tag_filter,
    favorites_toggle,
    prompt_card,
    stats_display,
    empty_state,
)
from config import PAGINATE_BY


def initialize_session_state() -> None:
    """Initialize session state variables"""
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "selected_tags" not in st.session_state:
        st.session_state.selected_tags = []
    if "favorites_only" not in st.session_state:
        st.session_state.favorites_only = False
    if "current_page" not in st.session_state:
        st.session_state.current_page = 0


def render_home() -> None:
    """Render home page"""
    st.title("💬 Prompt Manager")
    st.markdown("Browse, search, and organize your prompt library")

    # Initialize services
    db = Database()
    prompt_service = PromptService(db)
    filter_service = FilterService(db)

    # Get all categories and tags
    all_categories = filter_service.get_categories()
    all_tags = filter_service.get_tags()

    # Display statistics
    stats = db.get_stats()
    stats_display(stats)

    st.divider()

    # Search and filters
    st.subheader("Search & Filter")

    col1, col2 = st.columns([2, 1])
    with col1:
        query = search_bar("Search by title, content, or variables...")
        st.session_state.search_query = query

    with col2:
        st.session_state.favorites_only = favorites_toggle()

    col1, col2, col3 = st.columns(3)
    with col1:
        category = category_filter(all_categories)
        st.session_state.selected_category = category

    with col2:
        tags = tag_filter(all_tags)
        st.session_state.selected_tags = tags

    with col3:
        st.markdown("")  # Spacer

    st.divider()

    # Get filtered prompts
    prompts = prompt_service.list_prompts(
        search_query=st.session_state.search_query,
        category=st.session_state.selected_category,
        tags=st.session_state.selected_tags if st.session_state.selected_tags else None,
        favorites_only=st.session_state.favorites_only,
    )

    # Display results
    st.subheader(f"Results ({len(prompts)} prompts)")

    if not prompts:
        empty_state(
            icon="🔍",
            title="No prompts found",
            message="Try adjusting your search or filters",
        )
    else:
        # Pagination
        total_pages = (len(prompts) + PAGINATE_BY - 1) // PAGINATE_BY

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Previous", disabled=st.session_state.current_page == 0):
                st.session_state.current_page -= 1
                st.rerun()

        with col2:
            st.write(
                f"Page {st.session_state.current_page + 1} of {total_pages}",
                unsafe_allow_html=False,
            )

        with col3:
            if st.button("Next →", disabled=st.session_state.current_page >= total_pages - 1):
                st.session_state.current_page += 1
                st.rerun()

        # Display prompts for current page
        start_idx = st.session_state.current_page * PAGINATE_BY
        end_idx = start_idx + PAGINATE_BY
        page_prompts = prompts[start_idx:end_idx]

        for prompt in page_prompts:

            def on_select(prompt_id: str) -> None:
                st.session_state.selected_prompt_id = prompt_id
                st.session_state.current_page_name = "viewer"
                st.switch_page("pages/3_▶️_Use.py")

            def on_favorite(prompt_id: str) -> None:
                prompt_service.toggle_favorite(prompt_id)
                st.rerun()

            prompt_card(
                prompt,
                on_select=on_select,
                on_favorite=on_favorite,
            )

    # Create new button (sticky at bottom)
    st.divider()
    if st.button("➕ Create New Prompt", use_container_width=True):
        st.switch_page("pages/2_✏️_Create.py")


if __name__ == "__main__":
    initialize_session_state()
    render_home()
