# HackMission design system

Extracted from [docs/mocks](../mocks/README.md) on 26 October 2026. Open [index.html](index.html) locally (`?theme=dark` forces dark; press `t` to toggle).

Brand: ink `#0B1B3A`, gold `#E8A33D`, paper `#F7F4EE`, Manrope 500/700/800 (from the Magic Patterns logo spec). Light is paper with ink actions; dark is ink with gold actions. Both pass WCAG 2.2 AA on every declared pair.

## Foundations

| Page | Covers |
|---|---|
| [Color](foundations/color.html) | Ink, gold, paper; status; contrast |
| [Typography](foundations/typography.html) | Manrope, scale, roles |
| [Spacing](foundations/spacing.html) | 4px scale, inside/between |
| [Layout](foundations/layout.html) | Breakpoints, grid, templates |
| [Elevation](foundations/elevation.html) | Shadows, surfaces, z |
| [Shape](foundations/shape.html) | Radii, borders |
| [Motion](foundations/motion.html) | Durations, easings |
| [Iconography](foundations/iconography.html) | Inline SVG icons |
| [Theming](foundations/theming.html) | Light, dark, brand themes |
| [Responsive](foundations/responsive.html) | Per-component behaviour |
| [Accessibility](foundations/accessibility.html) | WCAG 2.2 AA commitments |
| [Content](foundations/content.html) | Voice and microcopy |

## Components

| Component | Group |
|---|---|
| [Button](components/button.html) | Actions |
| [Button group](components/button-group.html) | Actions |
| [Link](components/link.html) | Actions |
| [Menu (dropdown)](components/menu.html) | Actions |
| [Text field](components/text-field.html) | Inputs |
| [Textarea](components/textarea.html) | Inputs |
| [Select](components/select.html) | Inputs |
| [Checkbox](components/checkbox.html) | Inputs |
| [Radio group](components/radio-group.html) | Inputs |
| [Switch](components/switch.html) | Inputs |
| [Form field](components/form-field.html) | Inputs |
| [Form layout](components/form-layout.html) | Inputs |
| [Site header](components/site-header.html) | Navigation |
| [Sidebar navigation](components/sidebar-nav.html) | Navigation |
| [Tabs](components/tabs.html) | Navigation |
| [Breadcrumb](components/breadcrumb.html) | Navigation |
| [Pagination](components/pagination.html) | Navigation |
| [Site footer](components/site-footer.html) | Navigation |
| [Skip link](components/skip-link.html) | Navigation |
| [Card](components/card.html) | Containers & overlays |
| [Accordion](components/accordion.html) | Containers & overlays |
| [Dialog](components/dialog.html) | Containers & overlays |
| [Drawer / sheet](components/drawer.html) | Containers & overlays |
| [Tooltip](components/tooltip.html) | Containers & overlays |
| [Divider](components/divider.html) | Containers & overlays |
| [Container, grid & stack](components/layout-primitives.html) | Containers & overlays |
| [Table](components/table.html) | Data display |
| [List](components/list.html) | Data display |
| [Description list](components/description-list.html) | Data display |
| [Avatar](components/avatar.html) | Data display |
| [Badge](components/badge.html) | Data display |
| [Chip](components/chip.html) | Data display |
| [Toast](components/toast.html) | Feedback |
| [Alert / banner](components/alert.html) | Feedback |
| [Inline message](components/inline-message.html) | Feedback |
| [Progress bar](components/progress.html) | Feedback |
| [Spinner](components/spinner.html) | Feedback |
| [Skeleton](components/skeleton.html) | Feedback |
| [Empty state](components/empty-state.html) | Feedback |
| [Error page](components/error-page.html) | Feedback |
| [Logo](components/logo.html) | Brand & marketing |
| [Hero](components/hero.html) | Brand & marketing |
| [Video player](components/video.html) | Brand & marketing |
| [Steps](components/steps.html) | Brand & marketing |
| [Schedule](components/schedule.html) | Brand & marketing |
| [Statement](components/statement.html) | Brand & marketing |

Every component page has the same thirteen sections (overview, anatomy, variants, sizes, states, responsive, theming, accessibility, content, do/don't, tokens, code, sources) with the full state matrix in both themes.

## Patterns

| Pattern | Covers |
|---|---|
| [Forms](patterns/forms.html) | Layout, validation, summaries |
| [Feedback & loading](patterns/feedback.html) | Toast vs alert; skeleton vs spinner |
| [Empty & error states](patterns/empty-error.html) | Formulas and when |
| [Navigation & page structure](patterns/navigation.html) | Shell, header, anchors |
| [Dialogs & overlays](patterns/dialogs.html) | Dialog vs drawer vs page |
| [Data tables & lists](patterns/tables.html) | Density, sorting, pagination |
| [Notifications](patterns/notifications.html) | Priority and dismissal |
| [Content & tone](patterns/content.html) | Voice applied per page |

## Tokens

- [`tokens/tokens.css`](tokens/tokens.css) — source of truth: primitives, semantic tokens, light and dark themes, reduced-motion and forced-colors handling.
- [`tokens/tokens.json`](tokens/tokens.json) — DTCG export generated by `tokens_to_json.py`.
- [`tokens/contrast-pairs.json`](tokens/contrast-pairs.json) — every fg/bg pairing the components rely on; checked in both themes.
- [`assets/components.css`](assets/components.css) — the component kit, token-driven, with `data-state` hooks.

## Drift found in the mocks

| Mock | Issue | Resolution |
|---|---|---|
| `assets/brand.css` | Components referenced primitives directly (`--palette-gold`, `--palette-ink`, `--palette-ink-800`, `--palette-mist`). | Added semantic tokens `--color-brand-gold`, `--color-fg-on-gold`, `--color-bg-hero*`, `--color-fg-hero*`, `--color-border-hero`, `--color-hero-danger`, `--color-focus-ring-on-hero`; components.css reads only those. |
| `assets/brand.css` | `--font-size-base` used but never defined (`.schedule__city .text-muted`). | Mapped to `--font-size-md`. |
| `assets/brand.css` | `.hero__inner`, `.hero__lede`, `.accordion--plain`, `.video__play` declared twice with later overrides. | Merged into single declarations in components.css. |
| `assets/brand.css` | Focus ring on hero hard-wired to the gold primitive; the light-theme ring (gold-700) is only 2.95:1 on ink. | New `--color-focus-ring-on-hero` (gold-500, 7.3:1 on ink) with an ink gap. |
| `assets/brand.css` | Manrope 800 used as a literal `font-weight: 800`. | Added `--font-weight-extrabold`. |
| `assets/tokens.css` | Dark `--color-bg-surface-sunken` equal to the surface, so sunken and surface were identical. | Sunken = ink-950 (canvas) in dark; surface = ink-900. |
| `pages/home/*` | Early mocks rendered the wordmark as “Hack Mission” (SVG + two inline siblings in a flex row). | `.logo__word` wrapper is now the rule. |
| `pages/home/*` | Video tile carried a “0:20 · narrated · captions” badge; captions were on by default. | Badge removed; `.video__meta` kept for a plain duration; `<track>` has no `default`. |
| `pages/home/invalid` | Error text wrapped in an extra `<span>` to fix wrapping. | `.field__error` wraps on its own; wrapper optional. |
| `mocks (various)` | Inline `style="flex:1"` on dialog and toast bodies. | Documented `.toast__body` / header `div` with flex in components.css; mocks keep working. |

## Verification

```
python ~/.claude/skills/extracting-design-systems/scripts/check_contrast.py docs/design-system/tokens/tokens.css
python ~/.claude/skills/extracting-design-systems/scripts/tokens_to_json.py docs/design-system/tokens/tokens.css
python ~/.claude/skills/extracting-design-systems/scripts/check_design_system.py docs/design-system
python .claude/skills/writing-html-mocks/scripts/screenshot_mocks.py docs/design-system --out docs/design-system/.cache/shots
```

Results are recorded below after each run.

<!-- verification:start -->
26 October 2026:

- `check_contrast.py`: 73 pairs, both themes, 0 failures.
- `tokens_to_json.py`: 279 tokens exported.
- `check_design_system.py`: 67 pages (46 components, 8 patterns, 12 foundations, index), 0 errors, 0 warnings.
- Screenshots reviewed at 360 and 1280 px in light and dark: index, button, hero, dialog, color (`.cache/shots/`).
- Mocks re-pointed at `tokens/tokens.css` + `assets/components.css`; `check_mocks.py`: 22 mocks, 0 errors; home/default and home/invalid re-screenshot and unchanged.
<!-- verification:end -->

## Regenerating

The pages are generated from a Python script kept outside the repo (scratchpad `ds/build.py`); edit the HTML directly for small changes, or ask for the generator to be re-run when adding a component.
