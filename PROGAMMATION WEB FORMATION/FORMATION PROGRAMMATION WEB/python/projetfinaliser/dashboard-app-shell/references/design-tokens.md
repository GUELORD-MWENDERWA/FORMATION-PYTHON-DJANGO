# Design tokens, breakpoints, theming

## Colour variables

Defined once on `:root` (dark, the default), overridden on
`.light:root` (light mode). **Every component reads colour through
these variables — never hardcode a hex value in a component rule**,
or it won't follow the theme toggle.

| Variable | Dark (default) | Light | Used for |
|---|---|---|---|
| `--app-bg` | `#101827` | `#fff` | Page background, sticky header background |
| `--sidebar` | `rgba(21,30,47,1)` | `#f3f6fd` | Sidebar / auth-card background |
| `--sidebar-main-color` | `#fff` | `#1f1c2e` | Sidebar logo/close-button icon colour |
| `--sidebar-link` | `#fff` | `#1f1c2e` | Sidebar nav link text/icon |
| `--sidebar-hover-link` | `#1a2539` | `rgba(195,207,244,.5)` | Sidebar item hover |
| `--sidebar-active-link` | `#1d283c` | `rgba(195,207,244,1)` | Sidebar item active background |
| `--app-content-main-color` | `#fff` | `#1f1c2e` | Body text in the content column |
| `--app-content-secondary-color` | `#1d283c` | `#f3f6fd` | Card/panel/table-header background |
| `--action-color` | `#2869ff` | (same) | Primary brand/action colour (links, primary buttons, active states) |
| `--action-color-hover` | `#6291fd` | (same) | Hover state of the above |
| `--table-border` | `#1a2131` | (same) | Hairline borders (form inputs, mobile topbar border) |
| `--filter-shadow` | dark, two-layer shadow | soft single shadow | Any floating/elevated element (menus, auth card) |
| `--status-warning` | `#d69a2d` | (same) | `.status.warning`, low-stock etc. |
| `--status-danger` | `#e0555f` | (same) | `.status.danger`, expiring/out-of-stock etc. |
| `--status-info` | `#2869ff` | (same) | `.status.info` |

Theme toggle: `script.js` toggles `document.documentElement.classList`
(`light` class on `<html>`), and `.mode-switch` in the page header
toggles its own `.active` class to swap the moon icon fill. No
JS-side colour values are ever set directly — it's purely a class
toggle, all colour comes from the CSS variables re-resolving.

## Typography

- Font: Google Fonts "Poppins", weights 300/400/500, loaded via
  `@import` at the top of `style.css`.
- Page title (`.app-content-headerText`): 24px / line-height 32px.
- Body/table text: 14px. Secondary/meta text: 12–13px at `opacity:
  0.6–0.7` (never a separate grey variable — dim the main-color token
  instead, so it still contrasts correctly in both themes).

## Spacing

- Page gutter: 16px (`.app-content-scroll` padding), reduced to 4px
  for the inner content wrappers' own horizontal padding (so total
  inset from the viewport edge is a consistent 20px).
- Card/panel padding: 16px (form cards use 24px, being a more
  deliberate focal surface).
- Border radius: 4px almost everywhere (8px only for `.auth-card` and
  `.pos-product-card` type "big tappable surface" elements).

## Icons

Inline SVG, "feather icons" convention: `viewBox="0 0 24 24"`,
`fill="none"`, `stroke="currentColor"`, `stroke-width="2"`,
`stroke-linecap="round"`, `stroke-linejoin="round"`. Sized via the
`width`/`height` attributes (18px in the sidebar, 16–22px elsewhere).
Keeping icons inline means `currentColor` correctly reflects the
button/link's text colour in both themes without any per-icon CSS.

## Breakpoints in use

| Width | What changes | Why this value |
|---|---|---|
| **1024px** | Sidebar becomes an off-canvas drawer; mobile topbar (hamburger) appears; stat-cards drop to 2 columns | Tablet-and-below cutoff — the fixed 200px sidebar plus a usable content area stops being comfortable around here |
| 900px | POS layout (`pos-layout`) drops from 2 columns to 1 | The catalog grid needs real width to stay usable; below this, stacking beats squeezing |
| 820px | `.panels-row` (dashboard widgets) drops to 1 column | Two side-by-side panels get too narrow to read comfortably |
| 780px | Table cell font drops to 12px; product image cell shrinks | Keeps dense tables from wrapping awkwardly before column-hiding kicks in |
| 620px | `.form-grid` drops from 2 columns to 1 | Two form columns become cramped on phone-sized widths |
| 520px | Stat-cards go to 1 column; `.app-content-actions` (search+filters row) stacks vertically; grid-view product cards go full width | General "phone portrait" breakpoint |
| 480px | Table hides the stock column, price cell widens | Last-resort column trimming for the narrowest common phones |

When adding a new responsive component, reuse these exact breakpoints
rather than inventing new ones — consistency here is what makes the
whole app feel coherent as the window is resized, rather than
different sections snapping at random widths.

## Reduced-motion / accessibility notes already in place

- `aria-current="page"` on the active sidebar link.
- `aria-expanded` / `aria-controls` / `aria-label` on the hamburger
  button, kept in sync by `script.js`.
- `aria-label` on the back-button (icon-only links must always have
  one).
- Drawer closes via overlay click, X button, `Escape`, or choosing a
  link — covers mouse, touch, and keyboard users equally (the project
  brief explicitly calls out not assuming a touchscreen).
