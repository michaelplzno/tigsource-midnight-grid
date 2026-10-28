# Contributing

Bug reports, layout fixes, accessibility improvements, and browser compatibility fixes are welcome.

## Work on the theme

1. Fork and clone the repository.
2. Edit `tigsource-midnight-grid.user.css`. There is no build step or package installation.
3. In Stylus, create a style in **UserCSS** mode and paste the entire file, including the metadata and `@-moz-document` wrapper.
4. Disable other TIGSource styles while verifying your changes. Keep only one copy of Midnight Grid active.

For a hosted raw-file or local-file development workflow, see [Stylus's UserCSS documentation](https://github.com/openstyles/stylus/wiki/Writing-UserCSS).

## Verify changes

Use the [three offline fixtures](tests/fixtures/README.md) to check the forum
index, Townhall board, and Neofeud topic against the CSS you are editing:

```sh
python tools/preview.py
python -m unittest discover -s tests -v
```

The first command starts a local preview at `http://127.0.0.1:8914/`; leave it
running and use a second terminal for the checks. Refresh a fixture after
editing the theme. Archived styles are excluded, so the preview always tests
the current `.user.css` file. No Stylus installation or third-party packages
are needed. The fixtures contain anonymized text and media placeholders;
also check the live forum before releasing a layout change.

- Check the forum index, a board's topic list, and a topic with multiple posts.
- Check wide desktop, medium, and narrow viewports, especially around the 1150px, 900px, 720px, and 640px breakpoints.
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
