"""
Prompt Manager - Settings Page (Import/Export, Preferences)
"""

import json
import streamlit as st

from database import Database
from services import ImportExportService
from utils import SettingsManager
from components import toast_success, toast_error, toast_info


def initialize_session_state() -> None:
    """Initialize session state variables"""
    pass


def render_settings() -> None:
    """Render settings page"""
    st.title("⚙️ Settings")

    db = Database()
    import_export_service = ImportExportService(db)
    settings_manager = SettingsManager()

    # Tabs for different settings
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Data", "🎨 Preferences", "📥 Import", "📤 Export"]
    )

    # ========================================================================
    # TAB 1: DATA MANAGEMENT
    # ========================================================================

    with tab1:
        st.subheader("📊 Database Information")

        stats = db.get_stats()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Prompts", stats["total_prompts"])
            st.metric("Total Favorites", stats["total_favorites"])
        with col2:
            st.metric("Total Tags", stats["total_tags"])
            st.metric("Total Uses", stats["total_uses"])

        st.divider()

        st.subheader("🧹 Maintenance")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Refresh Database", use_container_width=True):
                # Force recompute stats
                st.rerun()

        with col2:
            if st.button("⚠️ Clear All Data", use_container_width=True):
                if st.confirm("Are you sure? This cannot be undone."):
                    try:
                        # Delete all prompts
                        all_prompts = db.get_all_prompts()
                        for prompt in all_prompts:
                            db.delete_prompt(prompt.id)
                        toast_success("All data cleared!")
                        st.rerun()
                    except Exception as e:
                        toast_error(f"Error clearing data: {str(e)}")

    # ========================================================================
    # TAB 2: PREFERENCES
    # ========================================================================

    with tab2:
        st.subheader("🎨 Theme")

        settings = settings_manager.load()
        current_theme = settings.get("theme", "auto")

        theme_options = ["auto", "light", "dark", "glassmorphism", "neon"]
        theme = st.selectbox(
            "Theme Mode",
            options=theme_options,
            index=theme_options.index(current_theme) if current_theme in theme_options else 0,
        )

        if theme != current_theme:
            settings_manager.set("theme", theme)
            toast_success(f"Theme changed to {theme}")
            import time

            time.sleep(0.5)
            st.rerun()

        st.markdown("---")

        st.subheader("✨ Theme Descriptions")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **🌀 Auto** - System theme
            
            **☀️ Light** - Clean bright interface
            
            **🌙 Dark** - Easy on the eyes
            """)

        with col2:
            st.markdown("""
            **💎 Glassmorphism** - Frosted glass aesthetic with animated gradients and cyan glow effects
            
            **⚡ Neon** - High-contrast cyberpunk style with neon glows and vibrant accents
            """)

        st.divider()

        st.subheader("📋 Display Preferences")

        show_stats = st.checkbox(
            "Show statistics on home page",
            value=settings.get("show_stats", True),
        )
        if show_stats != settings.get("show_stats", True):
            settings_manager.set("show_stats", show_stats)

        items_per_page = st.slider(
            "Items per page",
            min_value=5,
            max_value=50,
            value=settings.get("items_per_page", 20),
            step=5,
        )
        if items_per_page != settings.get("items_per_page", 20):
            settings_manager.set("items_per_page", items_per_page)
            toast_info("Display preference updated")

        sort_by = st.selectbox(
            "Sort by",
            options=["created_at", "title", "use_count"],
            index=["created_at", "title", "use_count"].index(
                settings.get("sort_by", "created_at")
            ),
        )
        if sort_by != settings.get("sort_by", "created_at"):
            settings_manager.set("sort_by", sort_by)

    # ========================================================================
    # TAB 3: IMPORT
    # ========================================================================

    with tab3:
        st.subheader("📥 Import Prompts")
        st.info("Upload a JSON file exported from Prompt Manager to import prompts.")

        uploaded_file = st.file_uploader(
            "Choose JSON file",
            type=["json"],
            label_visibility="collapsed",
        )

        if uploaded_file:
            try:
                content = uploaded_file.read().decode("utf-8")
                preview_data = json.loads(content)

                st.write(f"**File contains {len(preview_data)} prompt(s)**")

                if st.button("✅ Import Prompts", use_container_width=True):
                    count, error = import_export_service.import_prompts(content)
                    if error:
                        toast_error(f"Import error: {error}")
                    else:
                        toast_success(f"Successfully imported {count} prompt(s)!")
                        import time

                        time.sleep(1)
                        st.rerun()

            except json.JSONDecodeError:
                st.error("Invalid JSON file")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

        st.divider()

        st.subheader("📋 Sample JSON Format")
        with st.expander("View sample format"):
            sample = import_export_service.get_export_sample()
            st.code(sample, language="json")

    # ========================================================================
    # TAB 4: EXPORT
    # ========================================================================

    with tab4:
        st.subheader("📤 Export Prompts")
        st.info("Download all your prompts as a JSON file for backup or sharing.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📥 Export as JSON", use_container_width=True):
                try:
                    json_content, filename = import_export_service.export_prompts()

                    st.download_button(
                        label="Download JSON",
                        data=json_content,
                        file_name=filename,
                        mime="application/json",
                        use_container_width=True,
                    )

                    settings_manager.set("last_export", filename)
                    toast_success(f"Ready to download: {filename}")

                except Exception as e:
                    toast_error(f"Error exporting: {str(e)}")

        with col2:
            st.markdown("")  # Spacer

        st.divider()

        st.subheader("📊 Export Statistics")

        all_prompts = db.get_all_prompts()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Prompts to export", len(all_prompts))

        with col2:
            total_size = sum(len(p.content) for p in all_prompts)
            size_kb = total_size / 1024
            st.metric("Estimated size", f"{size_kb:.1f} KB")

        with col3:
            total_vars = sum(len(p.variables) for p in all_prompts)
            st.metric("Total variables", total_vars)


if __name__ == "__main__":
    initialize_session_state()
    render_settings()
