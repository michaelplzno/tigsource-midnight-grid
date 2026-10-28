# Changelog

## 1.3.0 — 2026-10-28

- Make each board an independent tile; categories are lightweight section headings.
- Use column-major order within each section with three, two, or one columns.
- Set all tiles to 400px, above the largest natural tile measured across the supplied fixtures and tested widths.
- Keep child-board links inside their parent tile's footer without adding internal scrolling.
- Check tile heights, content bounds, child-footer placement, and column-major order.

## 1.2.0 — 2026-10-28

- Restore the category-card grid: three columns from 1440px, two from 1000px, and one below 1000px.
- Align card tops and bottoms within each row and use consistent 20px gutters.
- Keep uniform board-entry padding and the typography, controls, and mobile fixes from 1.1.0.
- Check card widths, matching row heights, gutters, and readable board-title widths in the layout probe.

## 1.1.0 — 2026-10-28

- Replace uneven category columns with full-width sections and aligned board rows.
- Apply the same responsive rows to board pages' child-board tables.
- Use a consistent, smaller default type scale and a centered 1600px content width.
- Align search fields and buttons, with larger touch targets on narrow screens.
- Refine topic metadata, post columns, media sizing, and mobile pagination.
- Consolidate repeated layout overrides and action-button styles; retain the embedded icons.
- Extend layout checks to cover category alignment, control heights, and overlapping reply/view counts.

## 1.0.0 — 2026-10-28

- Package the author's existing Midnight Grid Stylus theme as a standalone UserCSS file.
- Add project metadata, MIT licensing, and a stable update URL.
- Document installation, customization, contributions, and publishing.

The initial release preserved the theme rules from the supplied Stylus export.
