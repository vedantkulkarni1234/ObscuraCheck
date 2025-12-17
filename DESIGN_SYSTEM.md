# Prompt Manager - Visual Design System

## Color Palette

### Light Theme
```
Primary:
  - primary:        #2563EB (Blue - actions, links, focus states)
  - primary_hover:  #1D4ED8 (Darker blue)
  - primary_light:  #DBEAFE (Light blue background)

Secondary:
  - secondary:      #8B5CF6 (Purple - secondary actions)
  - secondary_hover: #7C3AED
  - secondary_light: #EDE9FE

Accent:
  - accent:         #EC4899 (Pink - highlights, favorites)
  - accent_light:   #FCE7F3

Background:
  - bg_primary:     #FFFFFF (White)
  - bg_secondary:   #F9FAFB (Light gray)
  - bg_tertiary:    #F3F4F6 (Slightly darker gray)

Text:
  - text_primary:   #1F2937 (Dark gray)
  - text_secondary: #6B7280 (Medium gray)
  - text_tertiary:  #9CA3AF (Light gray)

Status:
  - success:        #10B981 (Green)
  - warning:        #F59E0B (Amber)
  - danger:         #EF4444 (Red)
  - info:           #3B82F6 (Blue)

Neutral:
  - border:         #E5E7EB (Light border)
  - divider:        #D1D5DB (Medium divider)
  - overlay:        rgba(0, 0, 0, 0.5)
```

### Dark Theme
```
Primary:
  - primary:        #60A5FA (Bright blue)
  - primary_hover:  #93C5FD (Lighter blue)
  - primary_light:  #1E3A8A (Dark blue background)

Secondary:
  - secondary:      #A78BFA (Bright purple)
  - secondary_hover: #C4B5FD
  - secondary_light: #4C1D95

Accent:
  - accent:         #F472B6 (Bright pink)
  - accent_light:   #831843

Background:
  - bg_primary:     #111827 (Very dark gray)
  - bg_secondary:   #1F2937 (Dark gray)
  - bg_tertiary:    #374151 (Medium gray)

Text:
  - text_primary:   #F9FAFB (Off-white)
  - text_secondary: #D1D5DB (Light gray)
  - text_tertiary:  #9CA3AF (Medium gray)

Status:
  - success:        #34D399 (Green)
  - warning:        #FBBF24 (Amber)
  - danger:         #F87171 (Red)
  - info:           #60A5FA (Blue)

Neutral:
  - border:         #374151 (Dark border)
  - divider:        #4B5563 (Dark divider)
  - overlay:        rgba(0, 0, 0, 0.8)
```

## Typography Scale

| Usage | Size | Weight | Line Height | Letter Spacing |
|-------|------|--------|-------------|----------------|
| H1 (Page Title) | 32px | 700 | 1.2 | -0.5px |
| H2 (Section Title) | 24px | 600 | 1.3 | -0.25px |
| H3 (Subsection) | 18px | 600 | 1.4 | 0px |
| Body Large | 16px | 400 | 1.5 | 0px |
| Body Regular | 14px | 400 | 1.5 | 0.25px |
| Body Small | 12px | 400 | 1.4 | 0.25px |
| Label | 12px | 500 | 1.4 | 0.5px |
| Code | 13px | 400 | 1.6 | 0px |

**Font Family**: Inter, system sans-serif

## Spacing System

All spacing uses 4px base unit:
```
4px   - xs  (extra small detail)
8px   - sm  (small gaps, padding)
12px  - md  (medium spacing)
16px  - lg  (standard padding)
24px  - xl  (large sections)
32px  - 2xl (major sections)
48px  - 3xl (page sections)
```

Application:
- **Component Padding**: 12px (md)
- **Container Padding**: 24px (xl)
- **Page Margins**: 32px (2xl) top/bottom, 24px (xl) sides
- **Gap Between Cards**: 16px (lg)
- **Internal Element Gap**: 8px (sm)

## Border Radius

| Element | Value |
|---------|-------|
| Buttons | 6px |
| Input Fields | 6px |
| Cards | 8px |
| Dialogs | 10px |
| Badges/Tags | 4px |
| Large Sections | 12px |

## Shadows

| Layer | Definition |
|-------|-----------|
| Subtle (xs) | 0 1px 2px rgba(0,0,0,0.05) |
| Small (sm) | 0 1px 3px rgba(0,0,0,0.1) |
| Medium (md) | 0 4px 6px rgba(0,0,0,0.1) |
| Large (lg) | 0 10px 15px rgba(0,0,0,0.1) |
| XL | 0 20px 25px rgba(0,0,0,0.1) |
| Overlay | 0 25px 50px rgba(0,0,0,0.15) |

Apply shadow-md to cards, shadow-lg to dialogs/modals.

## Component Specifications

### Button
- **States**: Default, Hover, Active, Disabled
- **Sizes**: Small (32px), Medium (40px), Large (48px)
- **Variants**: Primary (blue), Secondary (purple), Danger (red), Ghost (outline)
- **Padding**: 8px 16px (medium)
- **Transition**: 150ms ease-in-out

### Input Fields
- **Height**: 40px
- **Padding**: 10px 12px
- **Border**: 1px solid border color
- **Border Radius**: 6px
- **Focus**: Blue outline (2px), no shadow
- **Placeholder**: text_tertiary color, reduced opacity

### Card
- **Border Radius**: 8px
- **Padding**: 16px
- **Background**: bg_secondary (light) / bg_secondary (dark)
- **Border**: 1px solid border color
- **Shadow**: shadow-sm
- **Hover**: Slight background change, shadow-md

### Search Bar
- **Height**: 44px
- **Padding**: 12px 16px
- **Icon**: text_secondary color
- **Background**: bg_tertiary
- **Debounce**: 300ms

### Tag/Badge
- **Padding**: 4px 8px
- **Font Size**: 12px
- **Border Radius**: 4px
- **Background**: Varies by category color
- **Font Weight**: 500

### Modal/Dialog
- **Border Radius**: 10px
- **Shadow**: shadow-xl
- **Backdrop**: overlay color
- **Padding**: 24px
- **Title Font**: H2 (24px, 600 weight)

## Animation & Micro-interactions

### Transitions
- **Quick**: 150ms (hover states, color changes)
- **Standard**: 300ms (drawer open/close, fade in)
- **Smooth**: 500ms (page transitions)

### Effects
```css
/* Smooth fade in/out */
transition: all 300ms ease-in-out;

/* Hover scale for interactive elements */
transform: scale(1.02) on hover;

/* Focus ring */
outline: 2px solid primary;
outline-offset: 2px;
```

### Toast Notifications
- **Duration**: 3000ms for success/info, 5000ms for error
- **Position**: Top-right
- **Animation**: Slide in from top, fade out
- **Sound**: Subtle 100ms beep (optional)

## Responsive Design

### Breakpoints
- **Mobile**: < 640px (not supported)
- **Tablet**: 640px - 1024px (limited support)
- **Desktop**: 1024px - 1440px (primary target)
- **Wide**: > 1440px (optimized)

### Layout
- **Single Column**: < 1200px
- **Two Columns**: 1200px - 1600px
- **Three Columns**: > 1600px

## Dark Mode Implementation

1. **CSS Variables**: Define all colors as CSS variables
2. **Media Query**: Detect via `prefers-color-scheme`
3. **Manual Toggle**: Override detection in settings
4. **Persistence**: Save preference to JSON config
5. **Smooth Transition**: 300ms transition on theme change

## Accessibility Standards

- **WCAG 2.1 AA** compliance target
- **Color Contrast**: Minimum 4.5:1 for text
- **Focus Indicators**: Visible 2px outline
- **Keyboard Navigation**: Tab order logical, all interactive elements accessible
- **Form Labels**: Every input has associated label
- **Error Messages**: Clear, in-context, and connected to input

## Design Tokens (CSS Variables)

```css
/* Colors */
--color-primary: #2563EB;
--color-secondary: #8B5CF6;
--color-accent: #EC4899;
--color-success: #10B981;
--color-warning: #F59E0B;
--color-danger: #EF4444;
--color-info: #3B82F6;

--color-bg-primary: #FFFFFF;
--color-bg-secondary: #F9FAFB;
--color-text-primary: #1F2937;
--color-text-secondary: #6B7280;

/* Spacing */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 12px;
--space-lg: 16px;
--space-xl: 24px;
--space-2xl: 32px;

/* Typography */
--font-family-base: 'Inter', system-ui, sans-serif;
--font-size-h1: 32px;
--font-size-h2: 24px;
--font-size-body: 14px;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

/* Border Radius */
--radius-sm: 4px;
--radius-md: 6px;
--radius-lg: 8px;
--radius-xl: 10px;

/* Shadows */
--shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
--shadow-md: 0 4px 6px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
```
