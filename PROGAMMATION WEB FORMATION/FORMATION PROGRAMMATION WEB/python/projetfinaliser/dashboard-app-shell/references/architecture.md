# Architecture — app shell, scroll model, mobile navigation

This file has the copy-paste-ready code for the structural layer. Read
`components.md` for the visual building blocks that go *inside* the
content area, and `design-tokens.md` for the colour/spacing system.

## 1. The core problem this solves

A sidebar+content admin layout is usually built as a fixed-height "app
shell" (`html, body { height: 100% } body { overflow: hidden }`) so it
feels like a native app instead of a plain document. That's good for
desktop, but it silently causes two very common bugs if you stop
there:

1. **Content gets clipped, not scrollable.** If a page's markup isn't
   individually wrapped in its own `overflow: auto` container, and
   that container's height is even slightly off, the bottom of the
   page is simply unreachable — no scrollbar, nothing. This is easy to
   get wrong per-page and easy to forget on new pages.
2. **The sidebar has nowhere to go on narrow screens.** The common
   naive fix is `.sidebar { display: none }` under some breakpoint,
   which **removes all navigation** with nothing replacing it. Any
   user on a phone/tablet, or a resized desktop window, gets stuck on
   whatever page they're on.

The fix used across every page of this project:

- Exactly **one** scroll container per page: `.app-content-scroll`.
  Nothing else in the content column scrolls independently (except a
  couple of deliberately bounded lists, see §4). Every page is
  reachable to the bottom no matter its length, without having to
  remember to wrap it in anything.
- The sidebar never fully disappears. Below 1024px it becomes an
  **off-canvas drawer** you open with a hamburger button that is
  *itself* always on screen (in a non-scrolling top bar), so
  navigation is never more than one tap away, on any page, at any
  scroll position.

## 2. HTML skeleton (`base.html`)

Every page extends this. Do not touch this structure per-page —
pages only fill `{% block content %}`.

```html
<body>
  <div class="app-container">
    {% include "partials/sidebar.html" %}

    {# Backdrop for the mobile drawer; closes it on click. #}
    <div class="sidebar-overlay" id="sidebarOverlay"></div>

    <div class="app-content">
      {# Non-scrolling. Always visible. Holds the hamburger. #}
      <div class="mobile-topbar">
        <button type="button" class="menu-toggle" id="menuToggle"
                aria-label="Ouvrir le menu de navigation"
                aria-controls="sidebar" aria-expanded="false">
          <!-- hamburger svg -->
        </button>
        <div class="mobile-topbar-brand">
          <!-- small logo svg --><span>AppName</span>
        </div>
      </div>

      {# The ONE scrolling element for the whole page. #}
      <div class="app-content-scroll">
        {% block content %}{% endblock %}
      </div>
    </div>
  </div>
  <script src="{% static 'js/script.js' %}"></script>
</body>
```

Why the hamburger lives in `base.html` and not per-page: if it were
part of each page's own header markup, every new page template would
need to remember to add it. Putting it in the shell means new pages
get correct mobile navigation for free.

## 3. CSS skeleton (shell rules)

```css
html, body {
  margin: 0; padding: 0;
  height: 100%;
  height: 100dvh;      /* dvh accounts for mobile browser chrome (URL bar) */
  width: 100%;
}
body { overflow: hidden; }   /* the shell itself never scrolls */

.app-container {
  height: 100%; max-height: 100%;
  display: flex; overflow: hidden;
  position: relative;          /* anchors the fixed drawer/overlay */
}

.app-content {
  height: 100%; max-height: 100%;
  flex: 1; min-width: 0;
  display: flex; flex-direction: column;   /* topbar row + scroll row */
}

/* THE single scroll container. */
.app-content-scroll {
  flex: 1; min-height: 0;      /* required for flex children to be scrollable */
  overflow-y: auto;
  overflow-x: auto;            /* never clip — let the user scroll sideways
                                   instead of hiding an overflowing element */
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-y: contain;
  padding: 0 16px 16px;
  scrollbar-width: thin;
  scrollbar-color: var(--app-content-secondary-color) transparent;
}
.app-content-scroll::-webkit-scrollbar { width: 10px; height: 10px; }
.app-content-scroll::-webkit-scrollbar-thumb {
  background-color: var(--app-content-secondary-color);
  border-radius: 8px;
}
.app-content-scroll::-webkit-scrollbar-track { background: transparent; }

/* Each page's own header row lives INSIDE .app-content-scroll and
   sticks to the top of it while the rest of the page scrolls under
   it. This is the only sticky element inside the scroll container —
   see the warning in §5 before adding a second one. */
.app-content-header {
  display: flex; align-items: center; flex-wrap: wrap; row-gap: 8px;
  justify-content: space-between;
  padding: 16px 4px 8px;
  position: sticky; top: 0;
  background-color: var(--app-bg);
  z-index: 5;
}
```

### Mobile drawer (sidebar) + overlay + topbar

```css
@media screen and (max-width: 1024px) {
  .sidebar {
    position: fixed; top: 0; left: 0;
    height: 100%; height: 100dvh; max-height: none;
    width: 260px; max-width: 82vw;
    z-index: 50;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    box-shadow: rgba(0, 0, 0, 0.35) 4px 0 24px;
  }
  .sidebar.open { transform: translateX(0); }
  .sidebar-close { display: inline-flex; }   /* X button, hidden on desktop */
}

.sidebar-overlay { display: none; }
@media screen and (max-width: 1024px) {
  .sidebar-overlay {
    display: block; position: fixed; inset: 0;
    background-color: rgba(8, 12, 22, 0.55);
    opacity: 0; pointer-events: none;
    transition: opacity 0.25s ease;
    z-index: 40;
  }
  .sidebar-overlay.open { opacity: 1; pointer-events: auto; }
}

.mobile-topbar { display: none; }
.menu-toggle { display: none; /* ... button styling ... */ }
@media screen and (max-width: 1024px) {
  .mobile-topbar {
    display: flex; align-items: center; gap: 8px;
    padding: 10px 16px;
    border-bottom: 1px solid var(--table-border);
    flex-shrink: 0;                 /* never let the flex column shrink this */
  }
  .menu-toggle { display: inline-flex; }
}
```

`position: fixed` on the drawer and overlay is what lets them escape
`.app-container`'s `overflow: hidden` and sit above the whole viewport
— fixed positioning always paints relative to the viewport regardless
of an ancestor's overflow clipping.

## 4. JS behaviour (`script.js`)

Guard every listener behind an existence check — `script.js` is
loaded on every page but not every page has every element (e.g. the
filter menu only exists on list pages with a toolbar).

```js
var menuToggle = document.querySelector(".menu-toggle");
var sidebar = document.querySelector(".sidebar");
var sidebarOverlay = document.querySelector(".sidebar-overlay");
var sidebarClose = document.querySelector(".sidebar-close");

function openSidebar() {
  if (!sidebar) return;
  sidebar.classList.add("open");
  if (sidebarOverlay) sidebarOverlay.classList.add("open");
  if (menuToggle) menuToggle.setAttribute("aria-expanded", "true");
}
function closeSidebar() {
  if (!sidebar) return;
  sidebar.classList.remove("open");
  if (sidebarOverlay) sidebarOverlay.classList.remove("open");
  if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
}

if (menuToggle && sidebar) {
  menuToggle.addEventListener("click", function () {
    sidebar.classList.contains("open") ? closeSidebar() : openSidebar();
  });
}
if (sidebarOverlay) sidebarOverlay.addEventListener("click", closeSidebar);
if (sidebarClose) sidebarClose.addEventListener("click", closeSidebar);
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") closeSidebar();
});
// Closing on link click matters: without it, picking a page from the
// drawer on mobile leaves the drawer open over the new page.
if (sidebar) {
  sidebar.querySelectorAll(".sidebar-list-item a").forEach(function (a) {
    a.addEventListener("click", closeSidebar);
  });
}
```

Close triggers implemented, and why each exists:
| Trigger | Why it matters |
|---|---|
| Click the overlay | Expected behaviour on every mobile app drawer (Gmail, Drive...) |
| Click the `.sidebar-close` (X) | Discoverable without knowing you can tap outside |
| `Escape` key | Keyboard-only / non-touch users must be able to dismiss it too |
| Click a nav link | Otherwise the drawer stays open over the destination page |

## 5. Why table headers and the cart panel are *not* `position: sticky`

Two `position: sticky; top: 0` elements inside the **same** scroll
container will collide once you scroll past the first one's height,
because sticky doesn't auto-stack — the second element would need
`top: <exact pixel height of the first>`, which is fragile and breaks
the moment the first element wraps to two lines (e.g. a long page
title next to a header button on a narrow screen).

Rule of thumb used throughout this project: **at most one
`position: sticky` element per scroll container** (`.app-content-header`
holds that slot). If you want a second sticky element (a sticky table
header, a sticky "add to cart" panel...), either:

- give it its own **separate, smaller** scroll container with a
  bounded height (see `.cart-items { max-height: 40vh; overflow-y: auto }`
  in `components.md` — this is a self-contained overflow area, not a
  sticky element, so it can't collide with anything), or
- accept it scrolling away with the rest of the content — usually not
  a real loss once the persistent mobile hamburger already guarantees
  navigation is never blocked.

## 6. Never leave a dead-end control

Every form and detail page must give the user two ways back to where
they came from, in addition to the sidebar/drawer:

1. A **back arrow** (`.back-button`) in `.app-content-header`, before
   the `<h1>`, linking to the parent list view.
2. A working **"Cancel" button that is an `<a>` to that same list**,
   not a `<button>` that does nothing. A cancel button with no `href`
   is a dead end — on mobile, before the drawer existed, that was a
   real "stuck" bug in this project; keep it a habit even though the
   drawer now provides a fallback.

```html
<div class="app-content-header">
  <a href="{% url 'produits_liste' %}" class="back-button" aria-label="Retour aux produits">
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
  </a>
  <h1 class="app-content-headerText">Ajouter un produit</h1>
  {% include "partials/theme_switch.html" %}
</div>
...
<div class="form-actions">
  <a href="{% url 'produits_liste' %}" class="btn btn-secondary">Annuler</a>
  <button type="submit" class="btn btn-primary">Enregistrer</button>
</div>
```

## 7. Active nav-state (where am I?)

`request` must be in `TEMPLATES[0].OPTIONS.context_processors`
(`django.template.context_processors.request`). Then in
`partials/sidebar.html`:

```html
<li class="sidebar-list-item{% if request.resolver_match.url_name == 'produits_liste' or request.resolver_match.url_name == 'produits_form' %} active{% endif %}">
  <a href="{% url 'produits_liste' %}"{% if request.resolver_match.url_name == 'produits_liste' or request.resolver_match.url_name == 'produits_form' %} aria-current="page"{% endif %}>
    ...
  </a>
</li>
```

Group every URL name that belongs to the same module (list + form +
detail) with `or`, so the item stays highlighted throughout that
module, not just on its exact list view. Explicit `==` comparisons
are used instead of Django's `in` on a string literal (which does a
*substring* match and can false-positive, e.g. `'ventes' in
'ventes_form'`-style checks going the wrong direction).
