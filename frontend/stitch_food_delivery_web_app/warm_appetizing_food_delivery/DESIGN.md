---
name: Warm & Appetizing Food Delivery
colors:
  surface: '#fbf9f5'
  surface-dim: '#dbdad6'
  surface-bright: '#fbf9f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3ef'
  surface-container: '#efeeea'
  surface-container-high: '#eae8e4'
  surface-container-highest: '#e4e2de'
  on-surface: '#1b1c1a'
  on-surface-variant: '#59413a'
  inverse-surface: '#30312e'
  inverse-on-surface: '#f2f0ed'
  outline: '#8d7169'
  outline-variant: '#e1bfb5'
  surface-tint: '#ac3403'
  primary: '#a93101'
  on-primary: '#ffffff'
  primary-container: '#cb491b'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb59e'
  secondary: '#8e4e14'
  on-secondary: '#ffffff'
  secondary-container: '#ffab69'
  on-secondary-container: '#783d01'
  tertiary: '#00685d'
  on-tertiary: '#ffffff'
  tertiary-container: '#008376'
  on-tertiary-container: '#f4fffb'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbd0'
  primary-fixed-dim: '#ffb59e'
  on-primary-fixed: '#3a0b00'
  on-primary-fixed-variant: '#842400'
  secondary-fixed: '#ffdcc4'
  secondary-fixed-dim: '#ffb780'
  on-secondary-fixed: '#2f1400'
  on-secondary-fixed-variant: '#6f3800'
  tertiary-fixed: '#8cf5e4'
  tertiary-fixed-dim: '#6fd8c8'
  on-tertiary-fixed: '#00201c'
  on-tertiary-fixed-variant: '#005048'
  background: '#fbf9f5'
  on-background: '#1b1c1a'
  surface-variant: '#e4e2de'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system is built for a modern food delivery application, balancing operational clarity with a warm, inviting, and appetizing aesthetic. The brand personality is friendly, contemporary, and indulgent yet reliable. It evokes the sensory delight of a great meal before the first bite is even taken.

We adopt a refined **Glassmorphism-infused Modern** style, combining clean structural layouts with translucent floating navigation layers, warm organic color pairings, and high-fidelity micro-interactions that signal readiness, speed, and culinary care.

## Colors

The palette is centered around a rich terracotta primary (`#D95325`) that stimulates appetite and establishes a strong brand anchor. This is complemented by a soft amber accent (`#F4A261`) for highlights, promotions, and active states. A fresh culinary teal (`#2A9D8F`) serves as a tertiary color for dietary badges, success states, and healthy options. 

Neutrals are warm and creamy (`#FDFBF7` for backgrounds, shifting to deep charcoal `#2B2D2F` for high-contrast text) to avoid stark clinical whites and maintain a comforting, kitchen-warm atmosphere.

## Typography

We utilize **Plus Jakarta Sans** for its soft, rounded geometric forms that feel welcoming and modern. The type scale is optimized for high-density food browsing menus while maintaining effortless legibility at a glance. Headlines use tighter letter spacing to create compact, appetizing headers for restaurant names and dish titles.

## Layout & Spacing

A fluid grid system is employed, structured around a 12-column setup for desktop viewports and a flexible single-column stack for mobile devices. Content layout relies on consistent 1.25rem outer margins and 1rem gutters to give food photography ample breathing room. 

Spacing tokens (`space-xs` through `space-xl`) strictly govern padding within menu cards, chips, and list rows, ensuring a rhythmic, predictable layout that prevents visual clutter.

## Elevation & Depth

Depth is communicated through warm, ambient shadows and translucent tonal layers. Surfaces lift slightly off the creamy background using low-opacity, terracotta-tinted shadows (`rgba(217, 83, 37, 0.08)`) that enhance the organic feel of the app. 

Floating elements—such as bottom checkout bars and sticky category filters—utilize a frosted glass effect with a subtle backdrop blur and high-contrast borders to maintain legibility over scrolling food imagery.

## Shapes

The shape language relies heavily on pill-shaped (`roundedeness: 3`) and heavily rounded containers. Buttons, category chips, search inputs, and image cards utilize generous radii (`1rem` to `2rem` for large containers) to reinforce the soft, approachable, and friendly nature of the brand. Sharp corners are entirely avoided to create a smooth, tactile browsing experience.

## Components

### Buttons
Primary action buttons are filled with the rich terracotta color, featuring pill-shaped geometry and subtle scale micro-interactions on tap. Secondary buttons use transparent backgrounds with a soft terracotta outline.

### Chips & Tags
Category selectors and dietary filters (e.g., "Vegan", "Spicy", "Fast Delivery") use pill-shaped chips with soft amber or neutral backgrounds, transitioning to solid primary fills when selected.

### Input Fields
Search bars and delivery address inputs feature fully rounded, soft-bordered containers with subtle inner shadows and clear leading icons for quick scanning.

### Cards
Restaurant and menu cards feature generous rounded corners, edge-to-edge photography, and floating badges for ratings and delivery time. Tapping a card triggers a delightful spring animation.

### Checkboxes & Radios
Customized with the primary terracotta hue and smooth checkmark transitions, ensuring delightful friction-free order customization.

### Additional Components
- **Floating Cart Bar:** A sticky bottom sheet with glassmorphism blur, displaying live order totals and a high-contrast checkout CTA.
- **Delivery Progress Tracker:** A step-by-step visual timeline featuring animated culinary icons (prep, oven, rider, delivered).