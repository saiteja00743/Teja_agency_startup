---
name: Teja Labs
colors:
  surface: '#f9f9f8'
  surface-dim: '#dadad9'
  surface-bright: '#f9f9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f3'
  surface-container: '#eeeeed'
  surface-container-high: '#e8e8e7'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#45464d'
  inverse-surface: '#2f3130'
  inverse-on-surface: '#f1f1f0'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#9d4300'
  on-secondary: '#ffffff'
  secondary-container: '#fd761a'
  on-secondary-container: '#5c2400'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#07006c'
  on-tertiary-container: '#7073ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#ffdbca'
  secondary-fixed-dim: '#ffb690'
  on-secondary-fixed: '#341100'
  on-secondary-fixed-variant: '#783200'
  tertiary-fixed: '#e1e0ff'
  tertiary-fixed-dim: '#c0c1ff'
  on-tertiary-fixed: '#07006c'
  on-tertiary-fixed-variant: '#2f2ebe'
  background: '#f9f9f8'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-2xl:
    fontFamily: Inter
    fontSize: 72px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm-mono:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 48px
  xl: 80px
  2xl: 120px
  container-max: 1280px
  gutter: 24px
---

## Brand & Style

The design system is engineered for a premium, high-performance agency environment. It balances the precision of developer-centric tools like Linear and Vercel with the fluid, expressive aesthetics of Framer. The target audience includes high-growth startups and enterprise innovation labs looking for technical sophistication paired with high-end editorial flair.

The style is **Modern Professional with Glassmorphic accents**. It prioritizes extreme clarity, generous white space, and a feeling of "engineered luxury." Visual interest is generated through subtle micro-interactions, high-quality typography, and the strategic use of vibrant accent gradients against a disciplined, neutral backdrop.

## Colors

The palette is anchored by a deep Navy and a warm Stone background, creating a canvas that feels more sophisticated than pure white/black.

- **Primary (#0F172A):** Used for core branding, primary buttons, and deep background sections to ground the design.
- **Secondary (#F97316):** An energetic orange used for conversion points, progress indicators, and high-attention notifications.
- **Accent (#6366F1):** An indigo used for interactive states, secondary brand elements, and technical highlights.
- **Surface & Background:** The system uses `#FAFAF9` (Stone 50) for the main body to reduce eye strain, with pure `#FFFFFF` used for elevated cards to create subtle depth.

## Typography

This design system utilizes **Inter** for its primary communication due to its exceptional legibility and modern, "tech-standard" feel. **Geist** is introduced for labels and mono-spaced technical data to lean into the professional startup aesthetic.

Headlines should use tight letter spacing and heavy weights to create a sense of authority. Body text maintains a generous line height (1.5–1.6x) to ensure readability amidst large layouts. For mobile, headline sizes are aggressively scaled down to maintain visual balance without breaking layout containers.

## Layout & Spacing

The layout philosophy follows a **12-column fluid grid** for desktop, transitioning to a **4-column grid** for mobile. 

- **Vertical Rhythm:** A strict 8px-based spacing system is used. Sections are separated by `xl` (80px) or `2xl` (120px) padding to evoke a "premium" sense of scale.
- **Margins:** Page margins are set to `md` (24px) on mobile and scale to `lg` (48px) on larger screens.
- **Alignment:** Content is centered within a maximum container width of 1280px. Service cards and pricing tiers should be distributed evenly across the grid with `gutter` spacing.

## Elevation & Depth

Hierarchy is established through **Tonal Layering** and **Glassmorphism**. 

1.  **Base Layer:** `#FAFAF9` (Stone 50).
2.  **Raised Layer (Cards/Containers):** `#FFFFFF` with a very soft, multi-layered shadow (0 4px 6px -1px rgb(0 0 0 / 0.05)) and a 1px border of `#E7E5E4`.
3.  **Floating Layer (Navigation/Modals):** Semi-transparent white (`rgba(255, 255, 255, 0.7)`) with a `blur(12px)` backdrop filter. This creates the signature "Framer" feel.
4.  **Interactive Depth:** Elements should use a slight `y-axis` shift (up 2px or 4px) on hover rather than heavy shadow increases to maintain a clean aesthetic.

## Shapes

The shape language is overtly **Rounded and Friendly**. 
- **Small Elements (Inputs/Buttons):** Use `rounded-lg` (0.5rem / 8px).
- **Standard Cards:** Use `rounded-xl` (1rem / 16px).
- **Service & Hero Containers:** Use `rounded-3xl` (1.5rem / 24px) to create the distinct high-end startup look.
- **Avatars & Iconic Accents:** Utilize full `pill-shaped` rounding.

## Components

### Buttons
Primary buttons use the Primary Navy (`#0F172A`) with white text. Secondary buttons use a transparent background with a subtle border. Hover states for primary buttons should trigger a slight scaling effect (1.02x) rather than just a color change.

### Service Cards
Cards feature a subtle gradient border (Indigo to Orange at 10% opacity) that becomes more vivid on hover. The background is pure white to contrast against the stone page background.

### Statistic Cards
Use large `display-lg` typography for the numbers. Include a small Indigo (`#6366F1`) trend icon or a micro-sparkline to visualize growth.

### Horizontal Timeline
A 2px dashed border in `#E7E5E4` connects nodes. Active nodes are filled with the Secondary Orange, while upcoming nodes remain outlined in Indigo.

### Pricing Tiers
The "Featured" tier uses a Primary Navy background with a subtle "Glass" shine effect at the top. Use checkmark icons in Secondary Orange for feature lists to drive visual consistency.

### Input Fields
Clean, minimal inputs with a 1px border. On focus, the border transitions to Indigo with a 4px soft outer glow (indigo-50).