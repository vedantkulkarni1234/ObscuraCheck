# Theme Usage Examples

## Quick Start

### Switching Between Themes

1. **Via Settings Page**
   - Open app and go to ⚙️ Settings
   - Click "Preferences" tab
   - Select theme from dropdown
   - Theme applies immediately

2. **Programmatically** (for development)
   ```python
   from utils import SettingsManager
   
   settings_manager = SettingsManager()
   settings_manager.set("theme", "glassmorphism")
   ```

## Theme Preview

### Light Theme
```
☀️ Clean, bright interface
- White background (#FFFFFF)
- Blue primary color (#2563EB)
- Perfect for daytime use
- Standard Material Design aesthetic
```

### Dark Theme
```
🌙 Easy on the eyes
- Dark background (#111827)
- Light blue primary (#60A5FA)
- Reduced eye strain
- High contrast for readability
```

### Glassmorphism Theme ⭐
```
💎 Modern frosted glass aesthetic
- Deep dark background (#0F172A) with animated gradients
- Cyan primary color (#06B6D4)
- Translucent cards with backdrop blur
- Glowing cyan effects on interaction
- Perfect for: Premium feel, modern design showcase
```

### Neon Theme ⭐⭐
```
⚡ High-contrast cyberpunk style
- Near-black background (#0A0E27)
- Neon colors: Cyan (#00FFFF), Magenta (#FF00FF), Pink (#FF0080)
- Bold 2px borders on all elements
- Intense glowing effects
- Perfect for: Gaming enthusiasts, futuristic UI, attention-grabbing
```

## CSS Properties Used by Each Theme

### Common to All Themes
```css
--color-primary: Primary action color
--color-secondary: Secondary action color
--color-accent: Accent highlights
--color-bg-primary: Main background
--color-bg-secondary: Secondary background
--color-text-primary: Main text color
--color-success: Success state (#10B981, #34D399, etc.)
--color-warning: Warning state
--color-danger: Error/danger state
--color-border: Border color
```

### Glassmorphism Specific
```css
/* Animated gradient background */
@keyframes gradient-shift { }

/* Frosted glass effect */
backdrop-filter: blur(10px);
-webkit-backdrop-filter: blur(10px);

/* Cyan glow on input focus */
box-shadow: 0 0 20px rgba(6, 182, 212, 0.5),
            0 0 40px rgba(6, 182, 212, 0.3);

/* Translucent backgrounds */
background: rgba(30, 41, 59, 0.4);
```

### Neon Specific
```css
/* Bold borders */
border: 2px solid #FF00FF;

/* Intense glow effects */
box-shadow: 0 0 30px rgba(0, 255, 255, 0.5),
            0 0 60px rgba(255, 0, 255, 0.3);

/* Radial gradient background */
radial-gradient(circle at 20% 50%, rgba(0, 255, 255, 0.05) 0%, transparent 50%)
```

## Component Styling

### Input Fields
```python
# All themes style input fields:
# - Border radius: 6px
# - Padding: 10px 12px
# - Focus state: colored outline + glow

# Glassmorphism:
# - Semi-transparent dark background
# - Cyan glow on focus
# - Subtle border

# Neon:
# - Solid dark background
# - Neon magenta border (2px)
# - Cyan glow on focus (intense)
```

### Buttons
```python
# All themes:
# - Smooth transitions (150ms)
# - Hover lift effect (translateY -2px)
# - Active state collapse

# Glassmorphism:
# - Cyan color with subtle glow
# - Smooth fade transitions

# Neon:
# - Magenta border with semi-transparent background
# - Changes to cyan on hover
# - Intense glow effects
```

### Cards
```python
# All themes:
# - Border radius: 8px
# - Padding: 16px
# - Hover state elevation

# Glassmorphism:
# - 40% opacity background
# - Backdrop blur: 10px
# - Subtle shadow
# - Hover: Border glows cyan

# Neon:
# - 2px magenta border
# - Dark solid background
# - Intense shadow with glow
# - Hover: Border changes to cyan
```

## Color Values Quick Reference

### Glassmorphism Palette
```
Primary Colors:
  Cyan:    #06B6D4 (primary)
  Purple:  #8B5CF6 (secondary)
  Pink:    #EC4899 (accent)

Background:
  Deep:    #0F172A (bg_primary)
  Trans:   rgba(15, 23, 42, 0.7) (bg_secondary)

Status Colors:
  Success: #10B981
  Warning: #F59E0B
  Danger:  #EF4444
  Info:    #06B6D4
```

### Neon Palette
```
Primary Colors:
  Cyan:    #00FFFF (pure, intense)
  Magenta: #FF00FF (pure, bold)
  Pink:    #FF0080 (neon accent)

Background:
  Deep:    #0A0E27 (near black)
  Dark:    #1A1F3A

Status Colors:
  Success: #00FF41 (neon green)
  Warning: #FFFF00 (neon yellow)
  Danger:  #FF0041 (neon red)
  Info:    #00FFFF (neon cyan)
```

## Browser Preview

### Glassmorphism
- Background: Smooth gradient animation (15s loop)
- Cards: Frosted glass, semi-transparent
- Interactions: Glowing cyan accents
- Text: Light on dark, excellent contrast

### Neon
- Background: Dark with subtle colored light circles
- Cards: Bold magenta borders with glow
- Text: Bright white on dark background
- Interactions: Intense cyan/magenta glow effects

## Customization Guide

### Change Glassmorphism Primary Color

1. Edit `config.py`:
```python
GLASSMORPHISM_THEME: Dict[str, str] = {
    "primary": "#FF0099",  # Changed from cyan to pink
    # ... rest of colors
}
```

2. Update `styles.py` glow color:
```python
def get_glassmorphism_css() -> str:
    return """
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 20px rgba(255, 0, 153, 0.5);
    }
    """
```

### Change Neon Secondary Color

1. Edit `config.py`:
```python
NEON_THEME: Dict[str, str] = {
    "secondary": "#FFFF00",  # Bright yellow
    # ... rest
}
```

2. Update borders in `styles.py`:
```python
def get_neon_css() -> str:
    return """
    .card, .stContainer {
        border: 2px solid #FFFF00;
    }
    """
```

## Performance Tips

### Glassmorphism
- Blur animation runs in 15s cycle (minimal CPU impact)
- GPU-accelerated on modern browsers
- Backdrop blur supported on 95%+ of users' browsers

### Neon
- Pure CSS, no animation overhead
- Simple radial gradients in background
- Very performant on all devices

## Accessibility Considerations

### Contrast Ratios
- **Light Theme**: WCAG AAA compliant
- **Dark Theme**: WCAG AAA compliant
- **Glassmorphism**: WCAG AA (frosted glass may reduce contrast)
- **Neon**: WCAG AA+ (high contrast neon)

### Recommendations
- For accessibility, use Light or Dark themes
- Glassmorphism for design-focused users
- Neon may cause eye strain for extended use

## Known Limitations

### Glassmorphism
- Requires modern browser (Chrome 76+, Firefox 103+, Safari 11+)
- Backdrop blur may not work on older mobile devices
- Some CSS features degrade gracefully

### Neon
- Very high contrast may cause eye strain
- Recommended viewing distance: slightly further than normal
- Not ideal for dark environments

## Troubleshooting

### Theme not applying?
1. Clear browser cache (Ctrl+Shift+Delete)
2. Refresh page (Ctrl+Shift+R)
3. Check settings were saved

### Glassmorphism looks flat?
- Check browser supports backdrop-filter
- Enable hardware acceleration in browser settings
- Try a different browser

### Neon colors look washed out?
- Check screen brightness
- Adjust monitor color settings
- Try full-screen mode

## Future Theme Ideas

- [ ] Glass Dark - Dark mode with glassmorphism effects
- [ ] Neon Pink - Alternative neon color scheme
- [ ] Sunset - Warm gradient theme
- [ ] Ocean - Cool blue gradient theme
- [ ] Forest - Green natural theme
- [ ] High Contrast - Accessibility-focused theme

---

**Last Updated**: December 2024
**Status**: Production Ready
