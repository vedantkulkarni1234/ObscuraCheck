"""
Prompt Manager - Main Application Entry Point
"""

import streamlit as st

from config import STREAMLIT_CONFIG, ThemeMode
from styles import inject_css
from utils import SettingsManager


def configure_page() -> None:
    """Configure Streamlit page settings"""
    st.set_page_config(**STREAMLIT_CONFIG)


def initialize_theme() -> None:
    """Initialize and apply theme"""
    settings = SettingsManager().load()
    theme_mode = settings.get("theme", "auto")

    # Determine actual theme
    if theme_mode == "auto":
        # Default to light, let system handle if available
        actual_theme = "light"
    else:
        actual_theme = theme_mode

    # Inject CSS
    st.markdown(
        inject_css(theme_mode=actual_theme),
        unsafe_allow_html=True,
    )

    # Store in session
    st.session_state.current_theme = actual_theme


def render_sidebar() -> None:
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown("## 💬 Prompt Manager")
        st.markdown("---")

        # Navigation
        st.markdown("### Navigation")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Home", use_container_width=True):
                st.switch_page("pages/1_🏠_Home.py")

        with col2:
            if st.button("➕ Create", use_container_width=True):
                st.session_state.edit_prompt_id = None
                st.switch_page("pages/2_✏️_Create.py")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌌 Galaxy", use_container_width=True):
                st.switch_page("pages/5_🌌_Prompt_Galaxy.py")

        with col2:
            if st.button("🎬 Studio", use_container_width=True):
                st.switch_page("pages/6_🎬_Studio.py")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❓ Help", use_container_width=True):
                render_help_modal()
        
        with col2:
            if st.button("⚙️ Settings", use_container_width=True):
                st.switch_page("pages/4_⚙️_Settings.py")

        st.markdown("---")

        # Quick stats
        from database import Database

        db = Database()
        stats = db.get_stats()

        st.markdown("### 📊 Quick Stats")
        st.metric("Prompts", stats["total_prompts"])
        st.metric("Favorites", stats["total_favorites"])
        st.metric("Tags", stats["total_tags"])

        st.markdown("---")

        # Footer
        st.caption("Made with ❤️ using Streamlit")
        st.caption("v1.0.0")


def render_help_modal() -> None:
    """Display help information"""
    with st.container(border=True):
        st.markdown("### ❓ How to Use")

        st.markdown(
            """
        **Prompt Manager** helps you organize and use prompts efficiently.

        **Quick Start:**
        1. Click "➕ Create" to add a new prompt
        2. Use `{{variable}}` syntax for dynamic content
        3. Browse and search on the home page
        4. Click "▶️ Use" to fill variables and copy

        **Features:**
        - 🔍 Full-text search
        - 🏷️ Tags and categories
        - ⭐ Favorites
        - 📥 Import/Export JSON
        - 🎨 Light/Dark theme
        - 🎬 **Live Studio** - Real-time split-screen editor with instant variable preview

        **🎬 Live Studio:**
        A dedicated editor with split-pane interface where you can:
        - Edit prompts with syntax highlighting (left pane)
        - See real-time preview with variables substituted (right pane)
        - Variables update instantly as you type
        - Copy previews or full output with one click

        **Need Help?**
        Check the settings page for more options and documentation.
        """
        )


def main() -> None:
    """Main application entry point"""
    # Configure page
    configure_page()

    # Initialize theme
    initialize_theme()

    # Render sidebar
    render_sidebar()

    # Home page content
    st.title("💬 Prompt Manager")
    st.markdown("Welcome! Select a page from the sidebar to get started.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Get Started", use_container_width=True):
            st.switch_page("pages/1_🏠_Home.py")

    with col2:
        if st.button("➕ Create Your First Prompt", use_container_width=True):
            st.session_state.edit_prompt_id = None
            st.switch_page("pages/2_✏️_Create.py")


if __name__ == "__main__":
    main()
