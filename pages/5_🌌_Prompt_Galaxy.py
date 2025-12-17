"""
Prompt Galaxy - 3D Knowledge Graph Visualization
Explore your prompt library as an interactive 3D universe
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

from database import Database
from services import GalaxyService, PromptService
from utils import ValidationUtil


def initialize_session_state() -> None:
    """Initialize session state variables"""
    if "selected_prompt_id" not in st.session_state:
        st.session_state.selected_prompt_id = None
    if "show_prompt_details" not in st.session_state:
        st.session_state.show_prompt_details = False


def render_galaxy_header() -> None:
    """Render the galaxy page header"""
    st.title("🌌 Prompt Galaxy")
    st.markdown(
        """
        Explore your prompt library as an interactive 3D universe. 
        **Click** on glowing nodes to inspect prompts, **hover** to see details,
        and discover hidden connections between your prompts.
        """
    )
    st.markdown("---")


def render_galaxy_controls(db: Database, galaxy_service: GalaxyService) -> Dict:
    """Render galaxy controls and filters"""
    st.subheader("🎛️ Galaxy Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filter by category
        categories = galaxy_service.db.get_all_categories()
        selected_categories = st.multiselect(
            "📂 Categories",
            options=categories,
            default=categories,
            help="Filter nodes by category"
        )
    
    with col2:
        # Show favorites only
        favorites_only = st.checkbox(
            "⭐ Favorites Only",
            value=False,
            help="Show only favorite prompts"
        )
    
    with col3:
        # Show connections
        show_connections = st.checkbox(
            "🔗 Show Connections",
            value=True,
            help="Show similarity connections between prompts"
        )
    
    # Advanced options
    with st.expander("🔧 Advanced Settings"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            node_size_factor = st.slider(
                "Node Size",
                min_value=0.5,
                max_value=3.0,
                value=1.0,
                step=0.1,
                help="Scale node sizes"
            )
        
        with col2:
            opacity = st.slider(
                "Opacity",
                min_value=0.3,
                max_value=1.0,
                value=0.8,
                step=0.1,
                help="Node transparency"
            )
        
        with col3:
            connection_threshold = st.slider(
                "Connection Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.1,
                step=0.05,
                help="Minimum similarity to show connection"
            )
    
    return {
        "selected_categories": selected_categories,
        "favorites_only": favorites_only,
        "show_connections": show_connections,
        "node_size_factor": node_size_factor,
        "opacity": opacity,
        "connection_threshold": connection_threshold
    }


def create_galaxy_visualization(galaxy_data: Dict, controls: Dict) -> go.Figure:
    """
    Create the 3D galaxy visualization
    
    Args:
        galaxy_data: Galaxy data from GalaxyService
        controls: User control settings
        
    Returns:
        Plotly figure object
    """
    # Filter nodes based on controls
    filtered_nodes = []
    for node in galaxy_data["nodes"]:
        # Apply category filter
        if controls["selected_categories"] and node["category"] not in controls["selected_categories"]:
            continue
        
        # Apply favorites filter
        if controls["favorites_only"] and not node["is_favorite"]:
            continue
            
        filtered_nodes.append(node)
    
    if not filtered_nodes:
        # Create empty plot with message
        fig = go.Figure()
        fig.add_annotation(
            text="No prompts match the current filters",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=20, color="gray")
        )
        fig.update_layout(
            title="Prompt Galaxy - No Results",
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig

    # Prepare node traces
    x_coords = [node["x"] for node in filtered_nodes]
    y_coords = [node["y"] for node in filtered_nodes]
    z_coords = [node["z"] for node in filtered_nodes]
    sizes = [node["size"] * controls["node_size_factor"] for node in filtered_nodes]
    colors = [node["color"] for node in filtered_nodes]
    labels = [node["label"] for node in filtered_nodes]
    ids = [node["id"] for node in filtered_nodes]
    
    # Create hover text
    hover_texts = []
    for node in filtered_nodes:
        tags_str = ", ".join(node["tags"]) if node["tags"] else "No tags"
        favorite_str = "⭐ " if node["is_favorite"] else ""
        hover_text = (
            f"<b>{favorite_str}{node['label']}</b><br>"
            f"Category: {node['category']}<br>"
            f"Tags: {tags_str}<br>"
            f"Usage: {node['use_count']} times"
        )
        hover_texts.append(hover_text)
    
    # Create node trace
    node_trace = go.Scatter3d(
        x=x_coords,
        y=y_coords,
        z=z_coords,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=controls["opacity"],
            line=dict(width=2, color="rgba(255,255,255,0.8)")
        ),
        text=labels,
        customdata=ids,
        hovertemplate='%{text}<extra></extra>',
        name='Prompts'
    )
    
    # Create the figure
    fig = go.Figure(data=[node_trace])
    
    # Add connection lines if enabled
    if controls["show_connections"]:
        # Filter edges to only include filtered nodes
        filtered_ids = set(ids)
        connection_lines = []
        
        # Create a mapping from original node indices to filtered node indices
        filtered_node_map = {}
        for i, node in enumerate(filtered_nodes):
            # Find original index
            for orig_idx, orig_node in enumerate(galaxy_data["nodes"]):
                if orig_node["id"] == node["id"]:
                    filtered_node_map[orig_idx] = i
                    break
        
        for edge in galaxy_data["edges"]:
            # Check if both nodes are in filtered set
            if edge["from"] in filtered_node_map and edge["to"] in filtered_node_map:
                connection_lines.append((edge, filtered_node_map[edge["from"]], filtered_node_map[edge["to"]]))
        
        if connection_lines:
            # Create line traces for connections
            for edge_data in connection_lines:
                edge, node1_idx, node2_idx = edge_data
                if edge["weight"] >= controls["connection_threshold"]:
                    x_line = [x_coords[node1_idx], x_coords[node2_idx], None]
                    y_line = [y_coords[node1_idx], y_coords[node2_idx], None]
                    z_line = [z_coords[node1_idx], z_coords[node2_idx], None]
                    
                    # Line opacity based on similarity
                    line_opacity = min(edge["weight"], 1.0) * 0.5
                    
                    fig.add_trace(go.Scatter3d(
                        x=x_line,
                        y=y_line,
                        z=z_line,
                        mode='lines',
                        line=dict(
                            width=1,
                            color=f"rgba(100, 150, 255, {line_opacity})"
                        ),
                        hoverinfo='none',
                        showlegend=False
                    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="🌌 Your Prompt Galaxy",
            x=0.5,
            font=dict(size=24, color="white")
        ),
        scene=dict(
            xaxis=dict(
                showbackground=False,
                showgrid=False,
                showticklabels=False,
                title="",
                visible=False
            ),
            yaxis=dict(
                showbackground=False,
                showgrid=False,
                showticklabels=False,
                title="",
                visible=False
            ),
            zaxis=dict(
                showbackground=False,
                showgrid=False,
                showticklabels=False,
                title="",
                visible=False
            ),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    
    return fig


def render_galaxy_statistics(galaxy_service: GalaxyService) -> None:
    """Render galaxy statistics"""
    st.subheader("📊 Galaxy Statistics")
    
    stats = galaxy_service.get_galaxy_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Prompts",
            stats["total_prompts"],
            help="Number of prompts in your galaxy"
        )
    
    with col2:
        st.metric(
            "Connections",
            stats["total_connections"],
            help="Similarity connections discovered"
        )
    
    with col3:
        st.metric(
            "Clusters",
            stats["cluster_count"],
            help="Connected groups of similar prompts"
        )
    
    with col4:
        st.metric(
            "Avg Similarity",
            f"{stats['avg_similarity']:.3f}",
            help="Average similarity score across all connections"
        )


def render_prompt_details_sidebar(prompt_service: PromptService) -> None:
    """Render prompt details in sidebar when a node is selected"""
    if st.session_state.selected_prompt_id and st.session_state.show_prompt_details:
        prompt = prompt_service.get_prompt(st.session_state.selected_prompt_id)
        
        if prompt:
            with st.sidebar:
                st.markdown("---")
                st.markdown("### 🎯 Selected Prompt")
                
                # Favorite indicator
                if prompt.is_favorite:
                    st.markdown("⭐ **Favorite**")
                
                # Prompt details
                st.markdown(f"**{prompt.title}**")
                st.markdown(f"📂 {prompt.category}")
                
                if prompt.tags:
                    tags_str = " ".join([f"`{tag}`" for tag in prompt.tags])
                    st.markdown(f"🏷️ {tags_str}")
                
                st.markdown(f"📈 Used {prompt.use_count} times")
                
                # Content preview
                if prompt.content:
                    st.markdown("**Content Preview:**")
                    content_preview = prompt.content[:200] + "..." if len(prompt.content) > 200 else prompt.content
                    st.code(content_preview, language="text")
                
                # Actions
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("▶️ Use", use_container_width=True):
                        st.session_state.selected_prompt_id = str(prompt.id)
                        st.session_state.show_prompt_details = False
                        st.switch_page("pages/3_▶️_Use.py")
                
                with col2:
                    if st.button("✏️ Edit", use_container_width=True):
                        st.session_state.edit_prompt_id = str(prompt.id)
                        st.session_state.show_prompt_details = False
                        st.switch_page("pages/2_✏️_Create.py")
                
                if st.button("❌ Close Details"):
                    st.session_state.show_prompt_details = False
                    st.rerun()


def handle_node_click() -> None:
    """Handle node click events"""
    if hasattr(st.session_state, 'galaxy_chart') and st.session_state.galaxy_chart:
        click_data = st.session_state.galaxy_chart
        if click_data and 'points' in click_data:
            for point in click_data['points']:
                if point.get('customdata'):
                    st.session_state.selected_prompt_id = point['customdata']
                    st.session_state.show_prompt_details = True
                    st.rerun()


def main() -> None:
    """Main galaxy page function"""
    # Initialize database and services
    db = Database()
    galaxy_service = GalaxyService(db)
    prompt_service = PromptService(db)
    
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_galaxy_header()
    
    # Render controls
    controls = render_galaxy_controls(db, galaxy_service)
    
    # Get galaxy data
    galaxy_data = galaxy_service.create_galaxy_data()
    
    # Create and display visualization
    if galaxy_data["nodes"]:
        fig = create_galaxy_visualization(galaxy_data, controls)
        
        # Display the chart
        chart = st.plotly_chart(
            fig, 
            use_container_width=True,
            config={"displayModeBar": True, "scrollZoom": True}
        )
        
        # Add manual selection interface for better interactivity
        st.markdown("### 🎯 Quick Actions")
        col1, col2 = st.columns(2)
        
        with col1:
            selected_prompt_title = st.selectbox(
                "Select a prompt to view details:",
                options=[node["label"] for node in filtered_nodes],
                key="manual_prompt_selector"
            )
            
            if selected_prompt_title:
                # Find the selected prompt
                selected_prompt = next(
                    node for node in filtered_nodes if node["label"] == selected_prompt_title
                )
                if st.button("View Details", use_container_width=True):
                    st.session_state.selected_prompt_id = selected_prompt["id"]
                    st.session_state.show_prompt_details = True
                    st.rerun()
                        
    else:
        st.info("🌌 No prompts found. Create some prompts to see your galaxy!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Create Your First Prompt", use_container_width=True):
                st.session_state.edit_prompt_id = None
                st.switch_page("pages/2_✏️_Create.py")
        
        with col2:
            if st.button("🏠 Browse Home", use_container_width=True):
                st.switch_page("pages/1_🏠_Home.py")
    
    st.markdown("---")
    
    # Render statistics
    render_galaxy_statistics(galaxy_service)
    
    # Render prompt details sidebar
    render_prompt_details_sidebar(prompt_service)


if __name__ == "__main__":
    main()