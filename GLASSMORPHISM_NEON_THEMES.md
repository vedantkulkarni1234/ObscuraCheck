# ✨ Glassmorphism & Neon Themes - CSS Overhaul

## Overview

The Prompt Manager now features two premium modern themes that instantly elevate the visual appeal and user experience:

1. **💎 Glassmorphism Theme** - A sophisticated frosted-glass aesthetic with animated gradients
2. **⚡ Neon Theme** - A high-contrast cyberpunk style with glowing accents

## Features

### Glassmorphism Theme

**Visual Characteristics:**
- **Frosted Glass Cards**: Translucent, semi-transparent cards with backdrop blur effects
- **Animated Gradient Background**: Subtle, continuously shifting mesh gradients in the background
- **Cyan Glow Effects**: Neon glow on input fields and buttons when focused/hovered
- **Deep Dark Color Palette**: Dark backgrounds create stunning contrast with glass elements
- **Smooth Transitions**: 300ms animations for hover and focus states

**Technical Implementation:**
- `backdrop-filter: blur(10px)` on cards for frosted glass effect
- `background-size: 400% 400%` with keyframe animations for mesh gradients
- `box-shadow` with rgba colors for glow effects
- `rgba()` backgrounds for transparency layering

**Colors:**
- Primary: #06B6D4 (Cyan)
- Secondary: #8B5CF6 (Purple)
- Accent: #EC4899 (Pink)
- Background: #0F172A (Deep dark)
- Status: Green/Orange/Red/Cyan

### Neon Theme

**Visual Characteristics:**
- **Bold Neon Colors**: Pure neon cyan, magenta, and yellow accents
- **High Contrast Backgrounds**: Very dark backgrounds amplify neon brightness
- **Glowing Borders**: 2px borders with box-shadow glow effects
- **Cyberpunk Aesthetic**: Futuristic, gaming-inspired visual style
- **Radial Gradient Overlays**: Subtle colored light circles in background

**Technical Implementation:**
- `border: 2px solid` with neon colors
- `box-shadow: 0 0 30px rgba(0, 255, 255, 0.5)` for glow effects
- `radial-gradient()` background patterns
- High saturation RGB colors (e.g., #00FFFF for pure cyan)

**Colors:**
- Primary: #00FFFF (Neon Cyan)
- Secondary: #FF00FF (Neon Magenta)
- Accent: #FF0080 (Neon Pink)
- Background: #0A0E27 (Near black)
- Status: #00FF41 (Neon Green) / #FFFF00 (Neon Yellow) / #FF0041 (Neon Red)

## Usage

### Switching Themes

1. Navigate to **⚙️ Settings** page
2. Click the **Preferences** tab
3. Select theme from dropdown:
   - 🌀 Auto
   - ☀️ Light
   - 🌙 Dark
   - 💎 Glassmorphism
   - ⚡ Neon

4. Theme applies instantly with smooth transition

### Theme Persistence

- Selected theme is saved to user settings
- Persists across browser sessions
- Default theme: Auto (uses system preference)

## Technical Architecture

### Config (`config.py`)

New theme constants added:
```python
GLASSMORPHISM_THEME: Dict[str, str]  # Color palette
NEON_THEME: Dict[str, str]           # Color palette

class ThemeMode(str, Enum):
    GLASSMORPHISM = "glassmorphism"
    NEON = "neon"
```

### Styles (`styles.py`)

New functions for theme generation:
- `get_glassmorphism_css()` - Glassmorphism-specific CSS
- `get_neon_css()` - Neon-specific CSS
- `inject_css(theme_mode)` - Enhanced to support new themes

### Key CSS Variables

All themes use consistent CSS variables:
```css
:root {
    --color-primary: #06B6D4;
    --color-primary-hover: #0891B2;
    --color-bg-primary: #0F172A;
    --color-bg-secondary: rgba(15, 23, 42, 0.7);
    /* ... etc */
}
```

### Component Styles

Enhanced styling for:
- Input fields (.stTextInput, .stTextArea, .stSelectbox)
- Buttons (.stButton)
- Cards (.card)
- Expanders (.streamlit-expanderHeader)
- Tabs (.stTabs)

## Visual Enhancements

### Glassmorphism Effects

#### Backdrop Filter
```css
backdrop-filter: blur(10px);
-webkit-backdrop-filter: blur(10px);
```

#### Animated Gradient
```css
@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

body {
    animation: gradient-shift 15s ease infinite;
}
```

#### Glow on Focus
```css
box-shadow: 0 0 20px rgba(6, 182, 212, 0.5),
            0 0 40px rgba(6, 182, 212, 0.3);
```

### Neon Effects

#### Bold Borders
```css
border: 2px solid #FF00FF;
```

#### Intense Glow
```css
box-shadow: 0 0 30px rgba(0, 255, 255, 0.5),
            0 0 60px rgba(255, 0, 255, 0.3);
```

#### Background Gradients
```css
background-image: 
    radial-gradient(circle at 20% 50%, rgba(0, 255, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 0, 255, 0.05) 0%, transparent 50%);
```

## Settings UI

Added theme descriptions in Settings > Preferences:

```
🌀 Auto - System theme
☀️ Light - Clean bright interface
🌙 Dark - Easy on the eyes
💎 Glassmorphism - Frosted glass aesthetic with animated gradients and cyan glow effects
⚡ Neon - High-contrast cyberpunk style with neon glows and vibrant accents
```

## Browser Compatibility

### Glassmorphism
- Requires: Modern browser with backdrop-filter support
- Chrome/Edge: ✓ (all versions)
- Firefox: ✓ (v103+)
- Safari: ✓ (11+)
- Fallback: Works with semi-transparent backgrounds

### Neon
- Works in all modern browsers
- Pure CSS, no special requirements
- Graceful degradation in older browsers

## Performance Considerations

### Glassmorphism
- Animated gradients: 15s keyframe loop (minimal performance impact)
- Backdrop blur: GPU accelerated on most devices
- No JavaScript required

### Neon
- Static backgrounds with radial gradients (excellent performance)
- Heavy use of box-shadow for glow (GPU accelerated)
- No JavaScript required

## Customization

### Modifying Glassmorphism Theme

Edit in `config.py`:
```python
GLASSMORPHISM_THEME: Dict[str, str] = {
    "primary": "#06B6D4",  # Change cyan to different color
    "bg_primary": "#0F172A",  # Darker/lighter background
    # ... more colors
}
```

Then update CSS in `styles.py`:
```python
def get_glassmorphism_css() -> str:
    return """
    body {
        background: linear-gradient(-45deg, #0F172A, #1E293B, ...);
    }
    """
```

### Modifying Neon Theme

Similarly edit colors in `config.py` and update CSS in `styles.py`:
```python
NEON_THEME: Dict[str, str] = {
    "primary": "#00FFFF",  # Change to different neon color
    "secondary": "#FF00FF",
    # ... more colors
}
```

## Files Modified

1. **config.py**
   - Added ThemeMode.GLASSMORPHISM
   - Added ThemeMode.NEON
   - Added GLASSMORPHISM_THEME dictionary
   - Added NEON_THEME dictionary

2. **styles.py**
   - Updated imports for new themes
   - Added get_glassmorphism_css()
   - Added get_neon_css()
   - Updated inject_css() to handle new themes

3. **pages/4_⚙️_Settings.py**
   - Updated theme selectbox options
   - Added theme descriptions

4. **main.py**
   - Enhanced initialize_theme() for new modes

## Testing the Themes

### Glassmorphism
1. Go to Settings > Preferences
2. Select "glassmorphism" theme
3. Observe:
   - Animated background gradient
   - Frosted glass card appearance
   - Cyan glow on input focus
   - Smooth hover effects

### Neon
1. Go to Settings > Preferences
2. Select "neon" theme
3. Observe:
   - Dark background with colored light circles
   - Neon magenta/cyan borders on cards
   - Intense glow effects on hover
   - High-contrast text and elements

## Future Enhancements

- [ ] Additional theme variants (e.g., "Glass Dark", "Neon Pink")
- [ ] Theme customizer UI for color picking
- [ ] Theme export/import
- [ ] Per-component theme overrides
- [ ] Animation speed preferences
- [ ] Accessibility high-contrast mode

## References

- [Glassmorphism Design](https://glassmorphism.com/)
- [CSS backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter)
- [CSS Gradients](https://developer.mozilla.org/en-US/docs/Web/CSS/gradient)
- [Neon Design Trend](https://www.awwwards.com/trendy-web-designs-using-neon-signs.html)

## Support

For issues or theme-related bugs:
1. Check browser compatibility
2. Clear browser cache
3. Try switching to a different theme
4. Check console for CSS errors

---

**Version**: 1.0.0  
**Added**: Premium Theme Support  
**Status**: Stable
