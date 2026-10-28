# Offline forum fixtures

These fixtures preserve the SMF structure of three MHTML pages supplied by the
theme author on October 28, 2026:

| Fixture | Saved page | Coverage |
| --- | --- | --- |
| `index.html` | TIGSource Forums - Index | Fixed-height board tiles, section labels, child-board footers, account panel, search |
| `board.html` | Townhall | Topic table, action buttons, pagination, jump menu |
| `topic.html` | Neofeud | Posts, author columns, signatures, images, embedded videos |

The captures' frozen Midnight Grid CSS and unrelated browser-extension styles
have been removed. The preview server loads the current repository CSS last,
on every request, so refreshing after an edit tests the new source.

Session tokens, hidden inputs, original form actions, account details, profile
names, and external link destinations are removed or replaced. Post prose and
signatures use synthetic text with similar lengths. User images and video embeds
are local placeholders; common image formats preserve their original dimensions.
Only the four public forum sections are included in the index fixture.
The original MHTML files are excluded from Git.

## Preview

From the repository root, using Python 3.10 or later:

```sh
python tools/preview.py
```

Open **http://127.0.0.1:8914/** and choose one of the three pages. Each has a
current-theme view and an original-skin view. Stylus is not required for these
local previews. The server unwraps the single TIGSource `@-moz-document` block
for local testing; the installed style's domain scope is unchanged.

The preview binds to localhost, serves only fixtures and the compiled theme,
blocks form submission and remote requests with a Content Security Policy,
and does not execute archived scripts. It is a layout preview, not a working
forum: posting, login, search, navigation, and remote videos are not simulated.

Check 1920px, 1280px, 900px, and 390px viewports, plus widths around the theme's
breakpoints. Refresh after a CSS edit. For a quick layout report, paste the
expression from `../layout_probe.js` into the preview tab's developer console.
It checks column counts, fixed tile heights and gutters, column-major order,
visible tile content, child-board footer placement, readable board-title widths,
search-control heights, overlapping reply/view counts, page overflow, panel
bounds, and image loading.
Check screenshots too; the probe cannot verify every visual detail or real
forum interaction.

## Verify fixture integrity

```sh
python -m unittest discover -s tests -v
```

The checks cover three page structures, local asset completeness, removal of
active remote content and frozen theme CSS, preview route isolation, the
original-skin toggle, and loading CSS edits without rebuilding the fixtures.

## Regenerate from new captures

```sh
python tools/build_fixtures.py --index "path/to/index.mhtml" --board "path/to/board.mhtml" --topic "path/to/topic.mhtml"
```

The importer uses only Python's standard library. Review generated changes and
run the checks before committing. Keep raw captures outside the repository or
in the ignored `tests/.local/` directory. They can contain session data.

## Source material

The legacy CSS and interface images under `assets/legacy/`, and the original
forum markup structure, come from TIGSource's SMF skin and retain their original
ownership. They are preserved only as layout-test references and are not
relicensed by the project's MIT license. Synthetic text, generated placeholders,
the importer, and the preview tooling are project code under MIT.
