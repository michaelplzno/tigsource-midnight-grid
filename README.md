# TIGSource — Midnight Grid

A dark, responsive theme for the [TIGSource forums](https://forums.tigsource.com/), installed with the [Stylus browser extension](https://github.com/openstyles/stylus).

**[Install Midnight Grid](https://raw.githubusercontent.com/michaelplzno/tigsource-midnight-grid/main/tigsource-midnight-grid.user.css)** · [Report a bug](https://github.com/michaelplzno/tigsource-midnight-grid/issues)

Midnight Grid turns the forum index into a responsive grid, gives topics and posts more room, and replaces many small interface icons with embedded SVGs. It uses system fonts and adds no remote fonts, scripts, analytics, or image downloads. The forum's existing logo, avatars, and posted artwork remain part of the site.

*Earlier preview supplied by the author. The current defaults use a darker palette.*

## Install

1. Install **Stylus** using the browser-store links in its [official project README](https://github.com/openstyles/stylus#releases).
2. Open **[Install Midnight Grid](https://raw.githubusercontent.com/michaelplzno/tigsource-midnight-grid/main/tigsource-midnight-grid.user.css)**. Stylus should open its installation screen.
3. Click **Install style**. Leave **Check for updates** enabled if you want updates.
4. Visit or refresh [forums.tigsource.com](https://forums.tigsource.com/).

If the link shows plain CSS, confirm Stylus is enabled and its option to open the installer for `.user.css` URLs is enabled. The install link must open the **raw** file rather than GitHub's file viewer.

Already using the original exported style named `forums.tigsource.com`? Disable that copy before enabling Midnight Grid so the two styles do not overlap. This release has its own name and namespace and will install as a separate style.

You can also install without a hosted repository: open the Stylus manager, enable **UserCSS** (sometimes labeled **as UserCSS**), choose **Write new style**, paste the complete contents of [`tigsource-midnight-grid.user.css`](tigsource-midnight-grid.user.css), and save. A pasted copy does not automatically subscribe to updates; reinstall from the raw link to use hosted updates.

## Updates and removal

Stylus checks the `@updateURL` in the style metadata. Maintainers increment `@version` when publishing a change. You can also check for updates from the Stylus manager.

To restore the original forum appearance, disable or remove Midnight Grid in Stylus. The theme applies only to `https://forums.tigsource.com/` and does not change forum posts or account settings.

## Customize

Edit the style in Stylus and find the first `:root` block:

```css
--tig-width: 2400px;
--tig-text-scale: 1.4;
```

`--tig-width` controls the maximum content width. `--tig-text-scale` controls text sizing; for example, `1.2` is smaller than the default `1.4`. Color variables are nearby, although some later rules set colors directly. Local edits may be replaced by a future update, so keep a copy of your changes.

## Compatibility

Use a current browser that supports Stylus, CSS Grid, `:has()`, `:is()`, and CSS custom properties. Layouts adapt to smaller viewports, but installing the theme on a phone also requires a browser that supports Stylus.

The theme targets TIGSource's existing SMF markup. Site changes can require selector updates. Some button captions are English. The source has been preserved from the author's Stylus export; packaging validation does not establish that every forum screen works in every browser.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for local development and a manual verification checklist. There is no build step: the `.user.css` file is the source and the installable release.

See [docs/PUBLISHING.md](docs/PUBLISHING.md) for repository setup and future releases.

## License and credits

The theme code and embedded replacement SVG icons are available under the [MIT License](LICENSE). Created by [michaelplzno](https://github.com/michaelplzno).

This is an independent community theme. It is not affiliated with or endorsed by TIGSource or Simple Machines. The screenshot includes site branding and forum content belonging to their respective owners; those materials are not relicensed by this project's MIT license.
