# Contributing

Bug reports, layout fixes, accessibility improvements, and browser compatibility fixes are welcome.

## Work on the theme

1. Fork and clone the repository.
2. Edit `tigsource-midnight-grid.user.css`. There is no build step or package installation.
3. In Stylus, create a style in **UserCSS** mode and paste the entire file, including the metadata and `@-moz-document` wrapper.
4. Disable other TIGSource styles while verifying your changes. Keep only one copy of Midnight Grid active.

For a hosted raw-file or local-file development workflow, see [Stylus's UserCSS documentation](https://github.com/openstyles/stylus/wiki/Writing-UserCSS).

## Verify changes

- Check the forum index, a board's topic list, and a topic with multiple posts.
- Check wide desktop, medium, and narrow viewports, especially around the 1850px, 1150px, 900px, and 640px breakpoints.
- Check logged-out pages and, if you have an account, logged-in controls and the post editor.
- Check long titles, child boards, pagination, quotes, code blocks, images, signatures, and action buttons.
- Navigate with the keyboard and confirm focus indicators remain visible.
- Keep styles scoped to `https://forums.tigsource.com/` and preserve the original links, forms, post content, and image alt text.
- Keep replacement icons embedded and avoid introducing remote asset requests.

## Report a problem

Include the page URL, browser and Stylus versions, viewport width or zoom level, and what you expected to see. A screenshot helps; crop or redact private messages, addresses, and other personal information before sharing it.

## Submit a change

Explain the visible problem and the resulting behavior in your pull request. Include before/after screenshots for layout changes and describe the pages and browsers you checked. Keep unrelated formatting changes separate. Maintainers update the version when preparing a release.

Contributions to the theme code and replacement SVG icons are made under the project's MIT license.
