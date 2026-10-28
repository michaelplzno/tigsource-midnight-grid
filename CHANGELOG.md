# Changelog

## 1.6.1 — 2026-10-28

- Refresh documentation, the preview, and fixture validation.
- Limit fixture imports to the public forum sections.

## 1.6.0 — 2026-10-28

- Put post and topic counts directly beneath each board title, above the description.
- Align the first latest-post line at the same height in every tile, including tiles with child-board links.
- Add muted section colors through labels, a thin left accent, and a faint background tint.
- Preserve four-column layouts, fixed 240px tiles, column-major order, and full-size joysticks.
- Check title/count order, latest-post alignment, description clearance, and distinct section colors across responsive widths.

## 1.5.0 — 2026-10-28

- Use four columns from 1800px while preserving global column-major order and fixed 240px tiles.
- Place latest-post details directly beneath the statistics, removing the empty middle gap.
- Restore the original 39 × 58px joystick icons and reserve space beside board titles.
- Check the four-column breakpoint, compact metadata spacing, and full-size icons alongside the existing layout checks.

## 1.4.0 — 2026-10-28

- Combine every board into one continuous grid, preserving global column-major order.
- Put the section name on each tile instead of separate category headings.
- Pack full-width descriptions, compact statistics, and latest-post details into fixed 240px tiles, down from 400px.
- Use 16px gutters and keep child-board links within their parent tile.
- Check ordering across section boundaries, section labels, fixed heights, and fully visible tile content.

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
