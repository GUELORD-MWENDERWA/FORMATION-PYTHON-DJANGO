# Component catalog

Everything below lives inside `.app-content-scroll` (see
`architecture.md`). All components read colour from the CSS custom
properties in `design-tokens.md`, so they automatically follow the
light/dark theme — never hardcode a colour in a component, always use
a `var(--...)`.

Icons throughout are inline `feather`-style SVGs (24x24 viewBox,
`stroke="currentColor"`, `stroke-width="2"`, round caps/joins) sized
down with `width`/`height` attributes. Keeping them inline (not an
icon font/sprite request) means they inherit `currentColor` and never
cause a flash-of-unstyled-icon or an extra network request.

## Page header (every page)

```html
<div class="app-content-header">
  <h1 class="app-content-headerText">Titre de la page</h1>
  {% include "partials/theme_switch.html" %}
  <a href="{% url 'xxx_form' %}" class="app-content-headerButton">Ajouter un X</a>
</div>
```

- Sticky at the top of the scroll area (see architecture.md §3).
- `.mode-switch` (theme toggle) uses `margin-left: auto` so it's
  always pushed to the trailing side of the row regardless of what
  else is present.
- On a form/detail page, prepend a `.back-button` (see
  architecture.md §6) before the `<h1>`.
- `flex-wrap: wrap` is on by design: on very narrow screens, a long
  title + button pair drops the button to its own line rather than
  clipping or overflowing.

## Buttons

```html
<button class="btn btn-primary">Enregistrer</button>
<a href="..." class="btn btn-secondary">Annuler</a>
<button class="btn btn-danger">Supprimer</button>
```

Use `<a class="btn ...">` whenever the action is navigation (cancel,
back to list) — never a `<button>` with no handler. A button that
does nothing is a dead end for a user who has no other way back.

## Status pill

```html
<span class="status active">Actif</span>
<span class="status disabled">Desactive</span>
<span class="status warning">Stock faible</span>
<span class="status danger">Rupture</span>
<span class="status info">En cours</span>
```

## Stat cards (KPI row, e.g. dashboard header numbers)

```html
<div class="stat-cards">
  <div class="stat-card">
    <div class="stat-card-icon"><svg>...</svg></div>
    <div>
      <div class="stat-card-value">128</div>
      <div class="stat-card-label">Produits references</div>
    </div>
  </div>
  <!-- .stat-card-icon can also be .success / .warning / .danger -->
</div>
```

Grid: 4 columns desktop → 2 columns ≤1024px → 1 column ≤520px.

## Panel (generic card used for widgets, grouped settings, charts)

```html
<div class="panel">
  <div class="panel-header">
    <h2 class="panel-title">Titre du panneau</h2>
    <a href="..." class="panel-link">Voir tout</a>
  </div>
  <!-- content: .simple-list, .form-grid, .bar-chart, anything -->
</div>
```

`.panels-row` lays two panels side by side (`1.4fr 1fr`) → stacks to
one column ≤820px.

## Simple list (recent activity, alerts, notifications)

```html
<ul class="simple-list">
  <li class="simple-list-item">
    <div class="simple-list-icon warning"><svg>...</svg></div>
    <div class="simple-list-content">
      <p class="simple-list-title">Titre de la ligne</p>
      <p class="simple-list-meta">Sous-texte / horodatage</p>
    </div>
  </li>
</ul>
```

`.simple-list-icon` accepts no modifier (primary/blue), or `.warning`
/ `.danger`.

## Data table (clients, ventes, factures, stock — any flat list)

```html
<div class="data-table-wrapper">
  <div class="data-table-header">
    <div class="data-cell grow">Nom</div>
    <div class="data-cell">Telephone</div>
    <div class="data-cell shrink">Statut</div>
  </div>
  <div class="data-row">
    <div class="data-cell grow">Jean Kalombo</div>
    <div class="data-cell">+243 970 000 001</div>
    <div class="data-cell shrink"><span class="status active">Actif</span></div>
  </div>
</div>
```

- `.data-cell` defaults to `flex: 1`; use `.grow` (flex 1.6) for the
  primary/name column and `.shrink` (flex 0.6) for short columns
  (status, a short numeric id).
- `.data-table-wrapper` has `overflow-x: auto` as a safety net, but
  the real responsive strategy is **hiding non-essential columns**
  at narrower widths (see the `.product-cell` media queries in
  `products_table.html`'s CSS for the pattern) — copy that approach
  for any new table rather than relying on horizontal scroll alone,
  since a horizontally-scrolling data table is a worse mobile
  experience than a shorter, essential-columns-only one.
- Column headers are **not** sticky (see architecture.md §5) — only
  the page header is.

## Products table (list/grid toggle + sort buttons + filter menu)

This is the richest table variant (`partials/products_toolbar.html` +
`partials/products_table.html`). Reuse this pattern for any entity
that benefits from a visual grid view (things with a "face" — product
photos, thumbnails) in addition to a dense list view.

```html
{# toolbar: search + filter + list/grid switch #}
<div class="app-content-actions">
  <input class="search-bar" placeholder="Rechercher..." type="text" />
  <div class="app-content-actions-wrapper">
    <div class="filter-button-wrapper">
      <button class="action-button filter jsFilter"><span>Filtrer</span><svg>...</svg></button>
      <div class="filter-menu">
        <label>Categorie</label>
        <select>...</select>
        <div class="filter-menu-buttons">
          <button class="filter-button reset">Reinitialiser</button>
          <button class="filter-button apply">Appliquer</button>
        </div>
      </div>
    </div>
    <button class="action-button list active" title="Vue liste"><svg>...</svg></button>
    <button class="action-button grid" title="Vue grille"><svg>...</svg></button>
  </div>
</div>

{# table: wrapper starts in tableView; script.js toggles it to gridView #}
<div class="products-area-wrapper tableView">
  <div class="products-header">
    <div class="product-cell image">Articles<button class="sort-button"><svg>...</svg></button></div>
    ...
  </div>
  <div class="products-row">
    <button class="cell-more-button"><svg>...</svg></button>
    <div class="product-cell image">
      <span class="product-thumb" style="width:32px;height:32px;border-radius:6px;...">D</span>
      <span>Doliprane 1000mg</span>
    </div>
    <div class="product-cell category"><span class="cell-label">Categorie:</span>Medicaments</div>
    ...
  </div>
</div>
```

`.jsFilter` toggles `.filter-menu.active`; `.list`/`.grid` buttons
toggle `.tableView`/`.gridView` on `.products-area-wrapper` — both
wired in `script.js`, both guarded by an existence check so pages
without a toolbar don't error.

`.filter-menu` is `right: 0` (not a fixed negative offset) with
`max-width: calc(100vw - 32px)` specifically so it can never overflow
the viewport horizontally on a narrow screen — `.app-content-scroll`
allows horizontal overflow as a fallback, but a floating menu that
runs off-screen is a real "can't reach this control" bug, not just a
cosmetic one. Keep any future absolutely-positioned popover
(dropdown, tooltip, context menu) anchored the same way: to `right: 0`
/ `left: 0` of its own relatively-positioned wrapper, with a
`max-width: calc(100vw - <2x page padding>)` clamp — never a fixed
negative pixel offset.

## Form card

```html
<form class="form-card">
  <div class="form-grid">
    <div class="form-group">
      <label for="id">Label</label>
      <input type="text" id="id" name="name" placeholder="..." />
    </div>
    <div class="form-group full-width">
      <label for="notes">Notes</label>
      <textarea id="notes" name="notes"></textarea>
    </div>
  </div>
  <div class="form-actions">
    <a href="{% url 'xxx_liste' %}" class="btn btn-secondary">Annuler</a>
    <button type="submit" class="btn btn-primary">Enregistrer</button>
  </div>
</form>
```

`.form-grid` is 2 columns → 1 column ≤620px. `.form-group.full-width`
spans both columns at any width (`grid-column: 1 / -1`).

## Auth card (`base_auth.html` — no sidebar)

```html
<div class="auth-card">
  <div class="auth-logo"><svg>...</svg></div>
  <h1 class="auth-title">AppName</h1>
  <p class="auth-subtitle">Sous-titre</p>
  <form>
    <div class="form-group">...</div>
    <div class="auth-options">
      <label><input type="checkbox" /> Se souvenir</label>
      <a href="#">Mot de passe oublie ?</a>
    </div>
    <button type="submit" class="btn btn-primary">Se connecter</button>
  </form>
  <p class="auth-footer">... <a href="#">lien</a></p>
</div>
```

`.auth-wrapper` (the parent in `base_auth.html`) centers this card and
is itself `overflow-y: auto; min-height: 100dvh` so a tall card (long
error list, autofill-expanded fields) never gets clipped on a short
viewport — the same "always scrollable" rule as the main shell,
applied to the one page that doesn't use `.app-content-scroll`.

## Point-of-sale layout (catalog + running cart)

```html
<div class="pos-layout">
  <div class="pos-catalog">
    <div class="pos-product-card">
      <p class="pos-product-name">Doliprane 1000mg</p>
      <span class="pos-product-price">3 €</span>
    </div>
  </div>
  <div class="cart-panel">
    <div class="form-group"><label>Client</label><select>...</select></div>
    <div class="cart-items">
      <div class="cart-item">
        <div>Doliprane 1000mg<div class="cart-item-qty">2 x 3 €</div></div>
        <div>6 €</div>
      </div>
    </div>
    <div class="cart-totals">
      <div class="cart-total-row"><span>Sous-total</span><span>8 €</span></div>
      <div class="cart-total-row grand-total"><span>Total</span><span>8 €</span></div>
    </div>
    <div class="form-actions">...</div>
  </div>
</div>
```

`.pos-layout` is a 2-column grid (`1.6fr 1fr`) → 1 column ≤900px, and
is a normal (non-scrolling) block: the whole page scrolls as one, via
`.app-content-scroll`. The only intentionally bounded sub-scroll is
`.cart-items` (`max-height: 40vh; overflow-y: auto`) so a long cart
doesn't push the totals/checkout button far down the page — this is a
plain contained-overflow box, not `position: sticky`, so it can't
collide with the page header (see architecture.md §5 for why that
distinction matters).

## Invoice / printable detail card

```html
<div class="invoice-card">
  <div class="invoice-header">
    <div><h2>Company name</h2><p>address</p></div>
    <div class="invoice-meta"><p><strong>Facture N°</strong> ...</p></div>
  </div>
  <div class="invoice-parties">...</div>
  <div class="data-table-wrapper">...</div>
  <div class="invoice-totals">...</div>
  <div class="invoice-actions">
    <button class="btn btn-secondary">Telecharger en PDF</button>
    <button class="btn btn-primary">Imprimer</button>
  </div>
</div>
```

Pair with the `@media print` block in `style.css` (hides sidebar,
overlay, mobile topbar, theme toggle, `.invoice-actions`, and forces
`height: auto; overflow: visible` on the shell so the full document
prints instead of just the on-screen viewport).

## Bar chart (pure CSS, no chart library)

```html
<div class="bar-chart">
  <div class="bar-chart-col">
    <div class="bar-chart-bar" style="height: 40%;"></div>
    <span class="bar-chart-label">Lun</span>
  </div>
</div>
```

Fine for a quick static mock; swap for a real charting library before
shipping real data (this pattern hardcodes bar heights inline).

## Empty state

```html
<div class="empty-state">
  <p>Aucun element pour le moment.</p>
</div>
```
