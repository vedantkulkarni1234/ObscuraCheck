"""
Prompt Manager - Live Split-Screen Studio Page
A dedicated "Studio" page with unified split-pane interface for real-time variable preview.
"""

import streamlit as st
from streamlit_ace import st_ace

from database import Database, Variable, VariableType
from services import PromptService, VariableParser
from components import toast_success, toast_error
from utils import ValidationUtil
from config import DEFAULT_CATEGORIES


def initialize_studio_session_state() -> None:
    """Initialize studio session state variables"""
    if "studio_prompt_id" not in st.session_state:
        st.session_state.studio_prompt_id = None
    if "studio_content" not in st.session_state:
        st.session_state.studio_content = ""
    if "studio_title" not in st.session_state:
        st.session_state.studio_title = ""
    if "studio_category" not in st.session_state:
        st.session_state.studio_category = DEFAULT_CATEGORIES[0]
    if "studio_tags" not in st.session_state:
        st.session_state.studio_tags = []
    if "studio_variables" not in st.session_state:
        st.session_state.studio_variables = []
    if "studio_variable_values" not in st.session_state:
        st.session_state.studio_variable_values = {}


def render_studio() -> None:
    """Render the live studio editor with split-pane interface"""
    st.set_page_config(layout="wide")
    st.title("🎬 Live Studio")
    st.markdown("✨ Real-time prompt editor with instant variable preview - Edit on the left, see results on the right!")
    
    db = Database()
    prompt_service = PromptService(db)
    
    # Sidebar: Prompt selector and quick actions
    with st.sidebar:
        st.markdown("### 📚 Prompt Library")
        
        # Prompt selector
        all_prompts = db.get_all_prompts()
        if all_prompts:
            prompt_options = {p.title: p.id for p in all_prompts}
            selected_title = st.selectbox(
                "Select a prompt to edit:",
                options=["Create New"] + list(prompt_options.keys()),
                key="studio_prompt_selector"
            )
            
            if selected_title != "Create New":
                prompt_id = prompt_options[selected_title]
                if st.session_state.studio_prompt_id != prompt_id:
                    # Load prompt data
                    prompt = db.get_prompt(prompt_id)
                    if prompt:
                        st.session_state.studio_prompt_id = prompt_id
                        st.session_state.studio_title = prompt.title
                        st.session_state.studio_content = prompt.content
                        st.session_state.studio_category = prompt.category
                        st.session_state.studio_tags = prompt.tags
                        st.session_state.studio_variables = prompt.variables
                        st.session_state.studio_variable_values = {
                            v.name: v.default_value or "" for v in prompt.variables
                        }
            else:
                st.session_state.studio_prompt_id = None
                st.session_state.studio_title = ""
                st.session_state.studio_content = ""
                st.session_state.studio_category = DEFAULT_CATEGORIES[0]
                st.session_state.studio_tags = []
                st.session_state.studio_variables = []
                st.session_state.studio_variable_values = {}
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", use_container_width=True):
                handle_save(prompt_service, db)
        
        with col2:
            if st.button("🏠 Home", use_container_width=True):
                st.switch_page("pages/1_🏠_Home.py")
        
        if st.session_state.studio_prompt_id:
            if st.button("🗑️ Delete", use_container_width=True):
                if prompt_service.delete_prompt(st.session_state.studio_prompt_id):
                    toast_success("Prompt deleted!")
                    st.session_state.studio_prompt_id = None
                    st.session_state.studio_content = ""
                    st.session_state.studio_title = ""
                    st.session_state.studio_variable_values = {}
                    st.rerun()
    
    # Main content area with split panes
    col_left, col_right = st.columns([1, 1])
    
    # LEFT PANE: Editor
    with col_left:
        st.markdown("### ✏️ Editor")
        
        # Title input
        title = st.text_input(
            label="Title",
            value=st.session_state.studio_title,
            key="studio_title_input",
            placeholder="Enter prompt title"
        )
        st.session_state.studio_title = title
        
        # Category input
        existing_categories = db.get_all_categories()
        all_categories = sorted(set(DEFAULT_CATEGORIES + existing_categories))
        category = st.selectbox(
            label="Category",
            options=all_categories,
            index=all_categories.index(st.session_state.studio_category) if st.session_state.studio_category in all_categories else 0,
            key="studio_category_input"
        )
        st.session_state.studio_category = category
        
        # Tags input
        existing_tags = db.get_all_tags()
        tags = st.multiselect(
            label="Tags",
            options=sorted(existing_tags),
            default=st.session_state.studio_tags,
            key="studio_tags_input"
        )
        st.session_state.studio_tags = tags
        
        st.markdown("---")
        
        # Ace Editor for code/content editing with syntax highlighting
        st.markdown("💡 **Use {{variable_name}} for dynamic content**")
        
        content = st_ace(
            value=st.session_state.studio_content,
            language="markdown",
            theme="monokai",
            height=400,
            key="studio_ace_editor",
            extensions=["language_tools"],
        )
        
        if content is not None:
            st.session_state.studio_content = content
    
    # RIGHT PANE: Real-time Preview
    with col_right:
        st.markdown("### 👁️ Live Preview")
        
        # Auto-detect variables on every change
        if st.session_state.studio_content:
            detected_vars = VariableParser.extract_variables(st.session_state.studio_content)
            
            # Update session state with new detected variables
            existing_var_dict = {v.name: v for v in st.session_state.studio_variables}
            new_variables = []
            
            for var_name in detected_vars:
                if var_name in existing_var_dict:
                    new_variables.append(existing_var_dict[var_name])
                else:
                    new_variables.append(
                        Variable(
                            name=var_name,
                            type=VariableType.TEXT,
                            default_value="",
                        )
                    )
            
            st.session_state.studio_variables = new_variables
            
            # Variable inputs for live preview
            if detected_vars:
                st.markdown("**📝 Fill in variables to preview:**")
                
                for variable in st.session_state.studio_variables:
                    if variable.type == VariableType.TEXT:
                        value = st.text_input(
                            label=f"{{{{ {variable.name} }}}}",
                            value=st.session_state.studio_variable_values.get(variable.name, variable.default_value or ""),
                            key=f"studio_var_{variable.name}",
                            placeholder="Enter value"
                        )
                        st.session_state.studio_variable_values[variable.name] = value
                    
                    elif variable.type == VariableType.TEXTAREA:
                        value = st.text_area(
                            label=f"{{{{ {variable.name} }}}}",
                            value=st.session_state.studio_variable_values.get(variable.name, variable.default_value or ""),
                            key=f"studio_var_{variable.name}",
                            height=100,
                            placeholder="Enter value"
                        )
                        st.session_state.studio_variable_values[variable.name] = value
                    
                    elif variable.type == VariableType.SELECT:
                        if variable.options:
                            current_value = st.session_state.studio_variable_values.get(variable.name, variable.default_value or variable.options[0])
                            value = st.selectbox(
                                label=f"{{{{ {variable.name} }}}}",
                                options=variable.options,
                                index=variable.options.index(current_value) if current_value in variable.options else 0,
                                key=f"studio_var_{variable.name}"
                            )
                            st.session_state.studio_variable_values[variable.name] = value
                    
                    elif variable.type == VariableType.NUMBER:
                        value = st.number_input(
                            label=f"{{{{ {variable.name} }}}}",
                            value=float(st.session_state.studio_variable_values.get(variable.name, variable.default_value or 0)),
                            key=f"studio_var_{variable.name}"
                        )
                        st.session_state.studio_variable_values[variable.name] = str(value)
                
                st.markdown("---")
                
                # Real-time preview with variables substituted
                st.markdown("**📋 Live Preview:**")
                
                preview_text, missing_vars = VariableParser.generate_live_preview(
                    st.session_state.studio_content,
                    st.session_state.studio_variable_values
                )
                
                # Show missing variables warning
                if missing_vars:
                    st.warning(f"⚠️ Missing values: {', '.join([f'{{{{' + v + '}}}}' for v in missing_vars])}")
                
                # Display preview in a container
                with st.container(border=True):
                    st.text(preview_text)
                
                # Copy to clipboard button
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy Preview", use_container_width=True):
                        try:
                            import pyperclip
                            pyperclip.copy(preview_text)
                            st.success("✅ Copied to clipboard!")
                        except:
                            st.warning("Could not copy. Please copy manually.")
                
                with col2:
                    if st.button("💾 Use & Copy", use_container_width=True):
                        try:
                            import pyperclip
                            pyperclip.copy(preview_text)
                            st.success("✅ Preview copied!")
                        except:
                            st.info("Preview ready!")
            
            else:
                st.info("📝 No variables detected. Start typing {{variable_name}} in the editor to add variables!")
        
        else:
            st.info("📝 Start typing in the editor to see the preview!")
        
        # Statistics
        st.markdown("---")
        st.markdown("**📊 Statistics:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            char_count = len(st.session_state.studio_content)
            st.metric("Characters", char_count)
        with col2:
            word_count = len(st.session_state.studio_content.split())
            st.metric("Words", word_count)
        with col3:
            var_count = len(st.session_state.studio_variables)
            st.metric("Variables", var_count)


def handle_save(prompt_service: PromptService, db: Database) -> None:
    """Handle saving the prompt from studio"""
    # Validate
    is_valid, error_msg = ValidationUtil.validate_prompt_data(
        title=st.session_state.studio_title,
        content=st.session_state.studio_content,
        category=st.session_state.studio_category,
    )
    
    if not is_valid:
        toast_error(error_msg)
        return
    
    try:
        if st.session_state.studio_prompt_id:
            # Update existing prompt
            prompt_service.update_prompt(
                st.session_state.studio_prompt_id,
                title=st.session_state.studio_title,
                content=st.session_state.studio_content,
                category=st.session_state.studio_category,
                tags=st.session_state.studio_tags,
                variables=st.session_state.studio_variables,
            )
            toast_success("✅ Prompt updated!")
        else:
            # Create new prompt
            prompt_service.create_prompt(
                title=st.session_state.studio_title,
                content=st.session_state.studio_content,
                category=st.session_state.studio_category,
                tags=st.session_state.studio_tags,
                variables=st.session_state.studio_variables,
            )
            toast_success("✅ Prompt created!")
        
        st.rerun()
    
    except Exception as e:
        toast_error(f"Error saving: {str(e)}")


if __name__ == "__main__":
    initialize_studio_session_state()
    render_studio()
