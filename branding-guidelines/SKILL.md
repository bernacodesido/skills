---
name: branding-guidelines
description: >
  Applies RootstockLabs's official brand colors and typography to any sort of artifact that may benefit from having RootstockLabs's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
  Use when the user asks to design something visual, says "create slides" or
  "design slides" o "create a design following branding rules".
  Key capabilities: creates objects following RootstockLabs branding rules.
license: MIT
compatibility: Works with Claude.ai, Claude Code, and the Claude API.
metadata:
  author: Bernardo Codesido
  version: 1.0.0
---

# RootstockLabs Brand Styling

## Overview

To access RootstockLabs's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, RootstockLabs brand, visual formatting, visual design

## Brand Guidelines

### Colors

**Main Colors:**

- **Rootstock Black** — `#000000` — Primary color for all text, icons, and wordmark
- **Rootstock Off White** — `#FAFAF5` — Primary background color across all materials

**Accent Colors:**

The accent palette is shared with Rootstock and RIF, providing ecosystem consistency. Each color exists as a full tone and a lighter tint variant.

| Name | Full Tone | Tint |
|------|-----------|------|
| Rootstock Pink | `#FF70E0` | light pink |
| Rootstock Purple | `#9E75FF` | light lavender |
| RIF Blue | `#4B5CF0` | `#B3BBFF` |
| Rootstock Orange | `#FF9100` | `#FED8A7` |
| Rootstock Teal | `#08FFD1` | `#E2FBF1` |
| Rootstock Yellow | `#DEFF19` | `#F0FF96` |

### Typography

RootstockLabs uses **Rootstock Sans** exclusively for all headlines and body copy.

**Headline settings:**
- Tracking: -2.4%
- Leading: 90%
- Weight: Bold / Black

**Body copy settings:**
- Tracking: -2.4%
- Leading: 110%
- Weight: Regular

## Features

### Smart Font Application

Accent colors are applied selectively to **key conceptual words** in large display headlines only — never to body text. The color coding maps to brand themes:

- **Pink** (`#FF70E0`) → infrastructure / tools / innovation
- **Orange** (`#FF9100`) → ecosystem / community / economic concepts
- **Purple** (`#9E75FF`) → everyday use / advocacy / accessibility

All body copy and supporting text remains **Rootstock Black** (`#000000`) on **Rootstock Off White** (`#FAFAF5`). When no accent color is needed, headlines are also black.

### Text Styling

- Headlines use Rootstock Sans Bold/Black at large sizes with tight 90% leading and -2.4% tracking
- Body copy uses Rootstock Sans Regular with looser 110% leading and -2.4% tracking
- No italic or serif variants — all type is set in Rootstock Sans
- Color is applied to single words or short phrases, not full sentences
- Annotation badges (rounded-rectangle pill shapes) use accent color fills with black text set in small caps or uppercase Rootstock Sans

### Shape and Accent Colors

Color enters compositions primarily through:

1. **Key words in headlines** — single words colored with Pink, Orange, or Purple mapped to content theme
2. **Annotation badges** — rounded-rectangle callouts using accent color fills to label concepts alongside large display text
3. **3D assets** — reflective chrome shapes placed over photography (world context) or on plain backgrounds (reflecting code/Bitcoin context)
4. **Data visualisation** — full tones for outlines/strokes; tints as fill colors within chart elements

All typographic frames and backgrounds remain monochromatic. Accent colors never appear as background fills for full slides or sections.

## Technical Details

### Font Management

- **Primary typeface:** Rootstock Sans — used for 100% of text across all materials, including the wordmark
- The font is shared with the Rootstock brand; RootstockLabs does not have a separate typeface
- No secondary or fallback typeface is defined in the brand guidelines
- The wordmark "RootstockLabs" is set in Rootstock Sans Bold — do not recreate it from scratch; always use the approved asset file

### Color Application

The RootstockLabs colour strategy is **monochromatic-first with selective accent colour**:

1. **Base layer** — all backgrounds use Off White (`#FAFAF5`), all text and UI chrome use Black (`#000000`)
2. **Accent layer** — colour is added on top of the monochromatic base via specific elements:
   - Individual words in large display headlines
   - Data visualisation fills (tints) and strokes (full tones)
   - 3D asset shapes overlaid on photography or plain backgrounds
3. **Data vis rule** — use full-tone colours for outlines/borders and tint variants as area fills; use no more than two brand colour tones per chart
4. **Never** use accent colours as full-slide or section backgrounds; never apply accent colour to body copy

When generating or styling visual content, default to black-on-off-white and introduce accent colour only through the mechanisms above.

