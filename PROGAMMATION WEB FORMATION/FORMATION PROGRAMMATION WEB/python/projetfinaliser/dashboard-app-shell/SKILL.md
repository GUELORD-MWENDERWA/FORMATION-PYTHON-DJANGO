---
name: dashboard-app-shell
description: Responsive sidebar + content dashboard shell (Django templates, vanilla CSS/JS) with a mobile off-canvas nav drawer, a single guaranteed-scrollable content area, and a "never get stuck" back-navigation pattern. Use whenever building or extending an admin/back-office/CRUD-style app with a sidebar of modules (products, clients, sales-type entities) — list pages, forms, detail pages, a dashboard, dark/light theme. Also use when asked to make an existing dashboard-style layout responsive, fix a page that can't be scrolled to the bottom, or fix navigation that disappears/gets stuck on mobile.
---

# Dashboard app shell

A reusable design system extracted from GestionPharmacie's frontend
(`products/templates/`, `products/static/css/style.css`,
`products/static/js/script.js`). It is the reference to follow for
**any similar app**: sidebar of modules, list/form/detail pages per
module, a dashboard landing page, dark/light theme, works from a
narrow phone up to a wide desktop.

Keep this skill updated as the pattern evolves — it's meant to be
improved over time, not treated as frozen documentation.

## The three rules that matter most

1. **One scroll container per page, always present.** Every page's
   content sits inside `.app-content-scroll`. Never build a page
   whose content can silently overflow past the visible area with no
   way to reach it — see `references/architecture.md` §1–3 for why
   the naive "fixed-height app shell" approach breaks this, and the
   exact CSS that fixes it for good at the shell level (so individual
   pages don't have to think about it).
2. **Navigation is never more than one tap away.** The sidebar
   collapses into an off-canvas drawer below 1024px, but the
   hamburger button that opens it lives in a non-scrolling top bar
   that is part of the shell (`base.html`), not any individual page —
   so it's impossible to build a new page that forgets it. See
   `references/architecture.md` §2, §4.
3. **Every form/detail page has a real way back**, in addition to the
   drawer: a back-arrow next to the title, and a "Cancel" button that
   is an actual link to the parent list — never a dead `<button>`.
   See `references/architecture.md` §6.

## File map

```
products/templates/
  base.html                 shell: sidebar + overlay + mobile topbar + scroll area
  base_auth.html             lighter shell for pre-login pages (no sidebar)
  partials/sidebar.html      nav list, active-state logic, mobile close button
  partials/theme_switch.html dark/light toggle button
  <module>/liste.html        list/table page for one module
  <module>/form.html         create/edit form for one module
  <module>/detail.html       read-only detail page (if the module has one)
products/static/css/style.css   all component + shell + responsive CSS
products/static/js/script.js    theme toggle, drawer toggle, filter menu, grid/list toggle
```

## Quick start — adding a new module (e.g. "Commandes")

1. **URL + view**: add `commandes_liste`, `commandes_form` (and
   `commandes_detail` if needed) to `urls.py`/`views.py`, following
   the existing `<module>_liste` / `<module>_form` / `<module>_detail`
   naming — the sidebar active-state logic and the checklist below
   both depend on this convention.
2. **Sidebar entry** (`partials/sidebar.html`): copy an existing
   `<li class="sidebar-list-item...">` block, swap the icon/label/url
   names, and update the `{% if request.resolver_match.url_name ==
   ... %}` conditions to the new url names (see
   `references/architecture.md` §7).
3. **List page** (`commandes/liste.html`): extend `base.html`, use
   `.app-content-header` + `.app-content-actions` (search bar) +
   `.data-table-wrapper`/`.data-row` (or the richer
   `.products-area-wrapper` grid/list variant if items need visual
   thumbnails) — see `references/components.md`.
4. **Form page** (`commandes/form.html`): `.app-content-header` with a
   `.back-button` to the list, `.form-card` > `.form-grid` >
   `.form-group`s, `.form-actions` with a Cancel `<a>` (to the list)
   and a submit `.btn-primary`.
5. **Don't touch** `base.html`'s shell structure, the mobile topbar,
   or the scroll-container CSS — those are shared infrastructure; a
   new module should only ever add markup *inside*
   `{% block content %}`.
6. **Sanity-check responsiveness** at ~375px (phone), ~768px
   (tablet), and ~1440px (desktop) width: confirm the page scrolls to
   its very last element, the hamburger opens/closes the drawer, and
   the back-button/Cancel link both work.

## Reference files (load as needed)

- `references/architecture.md` — the scroll model, the mobile drawer
  system (full CSS + JS), the sticky-header collision rule, the
  back-navigation pattern, active nav-state detection. Read this
  before touching `base.html`, `style.css`'s shell rules, or
  `script.js`'s drawer logic.
- `references/components.md` — every reusable component
  (buttons, status pills, stat cards, panels, data tables, the
  richer products-table with grid/list + filter, forms, POS layout,
  invoice/print layout, auth card) with ready-to-copy HTML.
- `references/design-tokens.md` — the full colour variable table
  (dark + light), typography, spacing, icon convention, and the
  breakpoint table with the reasoning behind each value — reuse these
  exact breakpoints for any new responsive component instead of
  picking new ones.
- `references/reproduction-prompt.md` — a self-contained, copy-paste
  prompt (in French) that describes this entire design system in
  plain language, for handing to a tool/AI that does **not** have
  access to this repo's source and needs to reproduce the same
  sidebar/navigation/tables-not-cards/pages-per-module result from
  scratch. Keep it in sync with the three files above when the design
  changes.

## Known gaps in the current project (not part of this skill's scope, but worth knowing)

- Forms are static markup — no `{% csrf_token %}`, no model binding,
  no server-side validation yet (explicitly deferred to the Django
  integration pass per the templates' own comments).
- Search bars, filter menus, and sort buttons are visual only; no
  actual filtering logic is wired up yet.
- `auth/login.html` has no real authentication behind it yet.

None of that affects the layout/navigation patterns this skill
documents — those are already final and meant to be built on top of
as the real backend logic gets added.
