# 🌌 Prompt Galaxy - 3D Knowledge Graph

The **Prompt Galaxy** transforms your prompt library into an interactive 3D universe where prompts are represented as glowing nodes floating in space, connected by similarity bonds.

## ✨ Features

### 🎯 Interactive 3D Visualization
- **Glowing Nodes**: Each prompt appears as a colored sphere with size based on usage and favorites
- **3D Navigation**: Rotate, zoom, and pan through your prompt universe
- **Hover Details**: Hover over nodes to see prompt information
- **Click to Select**: Click nodes to view prompt details and take actions

### 🧬 Intelligent Clustering
- **Gravity-Based Layout**: Similar prompts automatically cluster together
- **Multi-Factor Similarity**: Connections based on:
  - Shared categories (40% weight)
  - Common tags (50% weight) 
  - Similar titles (10% weight)
- **Hidden Connections**: Discover unexpected relationships between prompts

### 🎛️ Advanced Controls
- **Category Filtering**: Focus on specific prompt categories
- **Favorites Only**: Show just your starred prompts
- **Connection Threshold**: Adjust similarity requirements for connections
- **Visual Tuning**: Control node size, opacity, and visual effects

### 📊 Galaxy Statistics
- **Total Connections**: Number of similarity relationships discovered
- **Cluster Analysis**: Connected groups of related prompts
- **Average Similarity**: Overall coherence of your prompt library
- **Usage Insights**: Most connected and frequently used categories

## 🚀 How It Works

### Similarity Algorithm
The galaxy uses a sophisticated similarity scoring system:

1. **Category Matching** (40% weight): Prompts in the same category are pulled closer
2. **Tag Overlap** (50% weight): Shared tags create strong gravitational bonds
3. **Title Similarity** (10% weight): Word overlap in titles creates minor connections

### 3D Positioning
- **Force-Directed Layout**: Uses NetworkX spring layout algorithm
- **Usage-Based Depth**: Frequently used prompts appear closer to the viewer
- **Favorite Enhancement**: Starred prompts get special positioning and coloring
- **Random Variation**: Small random offsets prevent perfect overlaps

### Visual Encoding
- **Node Size**: Proportional to usage count and favorite status
- **Color Coding**: Each category has a unique color
- **Favorites**: Golden color for starred prompts
- **Connection Lines**: Semi-transparent lines showing similarity strength

## 🎨 Visual Design

### Color Palette
- **Development**: Blue (#3498db)
- **Marketing**: Red (#e74c3c)
- **Research**: Orange (#f39c12)
- **Writing**: Purple (#9b59b6)
- **Analysis**: Teal (#1abc9c)
- **Planning**: Yellow (#f1c40f)
- **Communication**: Green (#2ecc71)
- **Documentation**: Gray (#95a5a6)
- **Testing**: Orange (#e67e22)
- **Design**: Pink (#ff69b4)
- **Favorites**: Gold (#ffd700)

### Node Sizing
- **Base Size**: 8 units
- **Favorites**: +4 units
- **Usage Bonus**: Up to +8 units (based on use_count / 2)

## 🎮 Usage Guide

### Navigation
1. **Rotate**: Click and drag to rotate the galaxy
2. **Zoom**: Use mouse wheel or trackpad scroll
3. **Pan**: Hold Shift + drag to pan
4. **Reset View**: Double-click to reset camera

### Interaction
1. **Hover**: Preview prompt information
2. **Click**: Select prompt for detailed view
3. **Filter**: Use controls to focus on specific types
4. **Explore**: Follow connection lines to discover related prompts

### Best Practices
- Start with a broad view to see overall structure
- Use category filters to focus on specific areas
- Follow connection lines to find similar prompts
- Look for isolated clusters to identify unique prompt types

## 🔧 Technical Implementation

### Dependencies Added
- **Plotly**: 3D interactive visualization
- **NetworkX**: Graph algorithms and layout computation
- **NumPy**: Numerical computations for positioning

### Architecture
- **GalaxyService**: Core logic for similarity calculation and positioning
- **3D Visualization**: Plotly-based interactive 3D scatter plot
- **Real-time Updates**: Responsive to filter changes and new prompts

### Performance
- **Efficient Layout**: NetworkX optimized for medium-sized datasets
- **Smart Filtering**: Client-side filtering for responsive interaction
- **Caching**: Galaxy data computed once per session

## 🌟 User Benefits

### Discovery
- **Hidden Patterns**: Find unexpected relationships between prompts
- **Cluster Analysis**: Identify thematic groupings in your library
- **Gap Identification**: Spot areas needing more prompts

### Organization  
- **Visual Hierarchy**: See your most important prompts at a glance
- **Relationship Mapping**: Understand how prompts connect and relate
- **Usage Insights**: Identify your most and least used prompt types

### Workflow Enhancement
- **Quick Access**: Find related prompts instantly
- **Inspiration**: Discover similar prompts when creating new ones
- **Quality Assurance**: Ensure prompts cover all necessary categories

## 🎯 Use Cases

### Content Creators
- Find related writing prompts quickly
- Discover content gaps in your library
- Organize prompts by theme and style

### Developers
- Cluster technical documentation templates
- Find related code review and bug report prompts
- Organize API documentation by technology

### Researchers
- Group research methodology prompts
- Find related survey and analysis templates
- Organize academic writing prompts

### Marketers
- Cluster campaign planning prompts
- Find related content marketing templates
- Organize customer communication prompts

---

*The Prompt Galaxy turns the mundane task of prompt management into an engaging exploration of your creative universe. Discover hidden connections, organize your thoughts in 3D space, and find inspiration in the relationships between your prompts.*