# TIGSource — Midnight Grid

A dark, responsive theme for the [TIGSource forums](https://forums.tigsource.com/), installed with the [Stylus browser extension](https://github.com/openstyles/stylus).

**[Install Midnight Grid](https://raw.githubusercontent.com/michaelplzno/tigsource-midnight-grid/main/tigsource-midnight-grid.user.css)** · [Report a bug](https://github.com/michaelplzno/tigsource-midnight-grid/issues)

Midnight Grid gives the forum aligned category sections, responsive board rows, readable posts, and embedded SVG interface icons. It uses system fonts and adds no remote fonts, scripts, analytics, or image downloads. The forum's existing logo, avatars, and posted artwork remain part of the site.

## Install

1. Install the **Stylus** extension for your browser: [Chrome / Edge / Brave and other Chromium browsers](https://chromewebstore.google.com/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne) or [Firefox](https://addons.mozilla.org/firefox/addon/styl-us/). These are the store listings linked by the [official Stylus project](https://github.com/openstyles/stylus#releases).
2. In the same browser, open **[Install Midnight Grid](https://raw.githubusercontent.com/michaelplzno/tigsource-midnight-grid/main/tigsource-midnight-grid.user.css)**. Stylus should open its installation screen.
3. Click **Install style**. Leave **Check for updates** enabled to receive future theme releases through Stylus.
4. Visit or refresh [forums.tigsource.com](https://forums.tigsource.com/).

You do not need a GitHub account, a downloaded ZIP, or any manual CSS copying for this method. It changes how the forum looks in your own browser.

If the link shows plain CSS, confirm Stylus is enabled and its option to open the installer for `.user.css` URLs is enabled. The install link must open the **raw** file rather than GitHub's file viewer.

Already using the original exported style named `forums.tigsource.com`? Disable that copy before enabling Midnight Grid so the two styles do not overlap. This release has its own name and namespace and will install as a separate style.

You can also install without a hosted repository: open the Stylus manager, enable **UserCSS** (sometimes labeled **as UserCSS**), choose **Write new style**, paste the complete contents of [`tigsource-midnight-grid.user.css`](tigsource-midnight-grid.user.css), and save. A pasted copy does not automatically subscribe to updates; reinstall from the raw link to use hosted updates.

## Updates and removal

Users who install from the link above and leave style updates enabled receive future releases through Stylus's update checks. Updates are periodic, rather than immediate. You can also check for updates from the Stylus manager. If you installed an earlier copy by pasting CSS, install from the hosted link once to subscribe to updates.

Stylus checks the `@updateURL` in the style metadata. Maintainers increment `@version` when publishing a change.

To restore the original forum appearance, disable or remove Midnight Grid in Stylus. The theme applies only to `https://forums.tigsource.com/` and does not change forum posts or account settings.

## Share on TIGSource

[Copy the ready-to-post announcement](docs/tigsource-post.txt) into a reply in the [original theme thread](https://forums.tigsource.com/index.php?topic=77372.0). The announcement uses the forum's BBCode link format.

## Customize

Edit the style in Stylus and find the first `:root` block:

```css
--tig-width: 1600px;
--tig-text-scale: 1.1;
```

`--tig-width` controls the maximum content width. `--tig-text-scale` controls text sizing; for example, `1.0` is smaller than the default `1.1`. Color variables are nearby. Local edits may be replaced by a future update, so keep a copy of your changes.

## Compatibility

Use a current browser that supports Stylus, CSS Grid, `:has()`, `:is()`, and CSS custom properties. Layouts adapt to smaller viewports, but installing the theme on a phone also requires a browser that supports Stylus.

The theme targets TIGSource's existing SMF markup. Site changes can require selector updates. Some button captions are English. The source has been preserved from the author's Stylus export; packaging validation does not establish that every forum screen works in every browser.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for local development and a manual verification checklist. There is no build step: the `.user.css` file is the source and the installable release.

Three [offline page fixtures](tests/fixtures/README.md) let contributors preview
the current CSS against the forum index, a board, and a topic. Run
`python tools/preview.py` from the repository root and open `http://127.0.0.1:8914/`.

See [docs/PUBLISHING.md](docs/PUBLISHING.md) for repository setup and future releases.

## License and credits

The theme code and embedded replacement SVG icons are available under the [MIT License](LICENSE). Created by [michaelplzno](https://github.com/michaelplzno).

This is an independent community theme. It is not affiliated with or endorsed by TIGSource or Simple Machines. The screenshot includes site branding and forum content belonging to their respective owners; those materials are not relicensed by this project's MIT license.
