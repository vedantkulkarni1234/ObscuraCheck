"""
Prompt Manager - Theming and CSS Injection
"""

from typing import Dict

from config import (
    LIGHT_THEME,
    DARK_THEME,
    FONT_FAMILY,
    SPACING,
    BORDER_RADIUS,
    SHADOWS,
)


# ============================================================================
# THEME CSS GENERATION
# ============================================================================

def get_theme_css(theme: Dict[str, str]) -> str:
    """
    Generate CSS for a theme
    
    Args:
        theme: Color dictionary
        
    Returns:
        CSS string with CSS variables
    """
    css = """
    :root {
        /* Colors */
        --color-primary: """ + theme['primary'] + """;
        --color-primary-hover: """ + theme['primary_hover'] + """;
        --color-primary-light: """ + theme['primary_light'] + """;
        --color-secondary: """ + theme['secondary'] + """;
        --color-secondary-hover: """ + theme['secondary_hover'] + """;
        --color-secondary-light: """ + theme['secondary_light'] + """;
        --color-accent: """ + theme['accent'] + """;
        --color-accent-light: """ + theme['accent_light'] + """;
        
        --color-success: """ + theme['success'] + """;
        --color-warning: """ + theme['warning'] + """;
        --color-danger: """ + theme['danger'] + """;
        --color-info: """ + theme['info'] + """;
        
        --color-bg-primary: """ + theme['bg_primary'] + """;
        --color-bg-secondary: """ + theme['bg_secondary'] + """;
        --color-bg-tertiary: """ + theme['bg_tertiary'] + """;
        --color-text-primary: """ + theme['text_primary'] + """;
        --color-text-secondary: """ + theme['text_secondary'] + """;
        --color-text-tertiary: """ + theme['text_tertiary'] + """;
        
        --color-border: """ + theme['border'] + """;
        --color-divider: """ + theme['divider'] + """;
        
        /* Typography */
        --font-family: """ + FONT_FAMILY + """;
        --font-size-h1: 32px;
        --font-size-h2: 24px;
        --font-size-h3: 18px;
        --font-size-body-lg: 16px;
        --font-size-body: 14px;
        --font-size-body-sm: 12px;
        --font-size-label: 12px;
        --font-size-code: 13px;
        
        /* Spacing */
        --space-xs: """ + SPACING['xs'] + """;
        --space-sm: """ + SPACING['sm'] + """;
        --space-md: """ + SPACING['md'] + """;
        --space-lg: """ + SPACING['lg'] + """;
        --space-xl: """ + SPACING['xl'] + """;
        --space-2xl: """ + SPACING['2xl'] + """;
        --space-3xl: """ + SPACING['3xl'] + """;
        
        /* Border Radius */
        --radius-sm: """ + BORDER_RADIUS['sm'] + """;
        --radius-md: """ + BORDER_RADIUS['md'] + """;
        --radius-lg: """ + BORDER_RADIUS['lg'] + """;
        --radius-xl: """ + BORDER_RADIUS['xl'] + """;
        --radius-2xl: """ + BORDER_RADIUS['2xl'] + """;
        
        /* Shadows */
        --shadow-xs: """ + SHADOWS['xs'] + """;
        --shadow-sm: """ + SHADOWS['sm'] + """;
        --shadow-md: """ + SHADOWS['md'] + """;
        --shadow-lg: """ + SHADOWS['lg'] + """;
        --shadow-xl: """ + SHADOWS['xl'] + """;
        --shadow-2xl: """ + SHADOWS['2xl'] + """;
    }
    """
    return css


def get_base_css() -> str:
    """Get base CSS for all themes"""
    return """
    * {
        font-family: var(--font-family);
        box-sizing: border-box;
    }
    
    body {
        background-color: var(--color-bg-primary);
        color: var(--color-text-primary);
        transition: background-color 0.3s, color 0.3s;
    }
    
    /* Headings */
    h1 {
        font-size: var(--font-size-h1);
        font-weight: 700;
        line-height: 1.2;
        color: var(--color-text-primary);
    }
    
    h2 {
        font-size: var(--font-size-h2);
        font-weight: 600;
        line-height: 1.3;
        color: var(--color-text-primary);
    }
    
    h3 {
        font-size: var(--font-size-h3);
        font-weight: 600;
        line-height: 1.4;
        color: var(--color-text-primary);
    }
    
    /* Text */
    p, span, div {
        font-size: var(--font-size-body);
        line-height: 1.5;
        color: var(--color-text-primary);
    }
    
    /* Links */
    a {
        color: var(--color-primary);
        text-decoration: none;
        transition: color 0.15s;
    }
    
    a:hover {
        color: var(--color-primary-hover);
    }
    
    /* Code */
    code, pre {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: var(--font-size-code);
        background-color: var(--color-bg-tertiary);
        color: var(--color-text-primary);
        border-radius: var(--radius-md);
        padding: 2px 6px;
    }
    
    pre {
        padding: var(--space-md);
        overflow-x: auto;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--color-bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--color-border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--color-text-secondary);
    }
    """


def get_component_css() -> str:
    """Get CSS for custom components"""
    return """
    /* Streamlit overrides */
    .stButton > button {
        border-radius: var(--radius-md);
        border: none;
        font-weight: 500;
        transition: all 0.15s;
        height: 40px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border-radius: var(--radius-md);
        border: 1px solid var(--color-border);
        font-size: var(--font-size-body);
        padding: 10px 12px;
        transition: all 0.15s;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        outline: 2px solid var(--color-primary);
        outline-offset: 0px;
        border-color: var(--color-primary);
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: var(--color-bg-secondary);
    }
    
    /* Divider */
    .stDivider {
        border-color: var(--color-border);
    }
    
    /* Cards and containers */
    .stContainer {
        border-radius: var(--radius-lg);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: var(--color-bg-tertiary);
        border-radius: var(--radius-md);
        transition: all 0.15s;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: var(--color-bg-secondary);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: var(--radius-md);
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: var(--color-primary);
        border-bottom: 2px solid var(--color-primary);
    }
    
    /* Success/Error messages */
    .stSuccess, .stAlert {
        border-radius: var(--radius-md);
        border-left: 4px solid var(--color-success);
    }
    
    .stError, .stAlert {
        border-left-color: var(--color-danger);
    }
    
    .stWarning, .stAlert {
        border-left-color: var(--color-warning);
    }
    
    .stInfo, .stAlert {
        border-left-color: var(--color-info);
    }
    
    /* Custom badge class */
    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: var(--radius-sm);
        font-size: var(--font-size-body-sm);
        font-weight: 500;
        background-color: var(--color-primary-light);
        color: var(--color-primary);
    }
    
    .badge.secondary {
        background-color: var(--color-secondary-light);
        color: var(--color-secondary);
    }
    
    .badge.accent {
        background-color: var(--color-accent-light);
        color: var(--color-accent);
    }
    
    /* Custom card class */
    .card {
        background-color: var(--color-bg-secondary);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        box-shadow: var(--shadow-sm);
        transition: all 0.15s;
    }
    
    .card:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--color-primary);
    }
    
    /* Custom button classes */
    .btn-primary {
        background-color: var(--color-primary);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: var(--radius-md);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s;
    }
    
    .btn-primary:hover {
        background-color: var(--color-primary-hover);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .btn-ghost {
        background-color: transparent;
        color: var(--color-primary);
        border: 1px solid var(--color-primary);
        padding: 8px 16px;
        border-radius: var(--radius-md);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s;
    }
    
    .btn-ghost:hover {
        background-color: var(--color-primary-light);
    }
    
    /* Search bar styling */
    .search-container {
        position: relative;
        display: flex;
        align-items: center;
    }
    
    .search-icon {
        position: absolute;
        left: 12px;
        color: var(--color-text-secondary);
        pointer-events: none;
    }
    
    .search-input {
        padding-left: 36px;
    }
    
    /* Modal/Dialog overlay */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        animation: fadeIn 0.3s;
    }
    
    .modal-content {
        background-color: var(--color-bg-primary);
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-2xl);
        padding: var(--space-xl);
        max-width: 600px;
        width: 90%;
        max-height: 90vh;
        overflow-y: auto;
        animation: slideUp 0.3s;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes slideUp {
        from {
            transform: translateY(20px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Utility classes */
    .text-center { text-align: center; }
    .text-right { text-align: right; }
    .text-left { text-align: left; }
    .text-muted { color: var(--color-text-secondary); }
    .text-small { font-size: var(--font-size-body-sm); }
    .text-large { font-size: var(--font-size-body-lg); }
    
    .mt-sm { margin-top: var(--space-sm); }
    .mt-md { margin-top: var(--space-md); }
    .mt-lg { margin-top: var(--space-lg); }
    .mt-xl { margin-top: var(--space-xl); }
    
    .mb-sm { margin-bottom: var(--space-sm); }
    .mb-md { margin-bottom: var(--space-md); }
    .mb-lg { margin-bottom: var(--space-lg); }
    .mb-xl { margin-bottom: var(--space-xl); }
    
    .p-sm { padding: var(--space-sm); }
    .p-md { padding: var(--space-md); }
    .p-lg { padding: var(--space-lg); }
    .p-xl { padding: var(--space-xl); }
    
    .gap-sm { gap: var(--space-sm); }
    .gap-md { gap: var(--space-md); }
    .gap-lg { gap: var(--space-lg); }
    
    .flex { display: flex; }
    .flex-col { flex-direction: column; }
    .items-center { align-items: center; }
    .justify-between { justify-content: space-between; }
    .justify-center { justify-content: center; }
    
    .opacity-50 { opacity: 0.5; }
    .opacity-75 { opacity: 0.75; }
    
    .cursor-pointer { cursor: pointer; }
    
    .rounded { border-radius: var(--radius-lg); }
    .rounded-full { border-radius: 9999px; }
    
    .shadow { box-shadow: var(--shadow-sm); }
    .shadow-md { box-shadow: var(--shadow-md); }
    .shadow-lg { box-shadow: var(--shadow-lg); }
    """


def inject_css(theme_mode: str = "light") -> str:
    """
    Generate complete CSS for injection
    
    Args:
        theme_mode: "light" or "dark"
        
    Returns:
        Complete CSS string
    """
    theme = LIGHT_THEME if theme_mode == "light" else DARK_THEME
    return f"""
    <style>
    {get_theme_css(theme)}
    {get_base_css()}
    {get_component_css()}
    </style>
    """
