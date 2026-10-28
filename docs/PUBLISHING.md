# Publishing and releases

The install and update URLs point to:

`michaelplzno/tigsource-midnight-grid`, branch `main`.

The raw install URL works once the public repository contains `tigsource-midnight-grid.user.css` on that branch. No website deployment, build service, npm package, or GitHub Pages configuration is required.

## First publication

Create a **public**, empty GitHub repository named `tigsource-midnight-grid` under `michaelplzno`. Do not initialize it with a generated README, license, or `.gitignore` if you will push the prepared local repository.

From the project directory, if the local repository has not yet been initialized:

```sh
git init -b main
git add .
git commit -m "Release Midnight Grid 1.0.0"
```

Connect the repository and push:

```sh
git remote add origin https://github.com/michaelplzno/tigsource-midnight-grid.git
git push -u origin main
```

Alternatively, after authenticating the GitHub CLI, use this in place of creating the remote separately:

```sh
gh repo create michaelplzno/tigsource-midnight-grid --public --source=. --remote=origin --push --description "A dark, responsive Stylus theme for the TIGSource forums"
```

Open the README's install link with Stylus enabled and confirm the installation screen shows Midnight Grid, version `1.0.0`, and MIT licensing. Install it, disable any earlier copy, and verify the forum index, board list, and topic view.

If publishing under a different owner, repository name, or branch, update the URLs in the UserCSS metadata, README, and this document before publishing. Keep `@name` and `@namespace` stable after the first public release so Stylus can recognize the style.

## Later releases

1. Edit the single `.user.css` source file and verify the affected forum pages.
2. Increment `@version` using semantic versioning and update `CHANGELOG.md`.
3. Merge or push the change to `main`. Stylus reads updates from the stable raw URL.
4. Optionally create a Git tag and GitHub release matching the version, such as `v1.0.1`.

Do not put a commit hash or release tag in `@updateURL`; it should continue to point at `main`. Readers can inspect each change through the repository's commit history.

## Files to keep private

Do not commit complete Stylus backup JSON files. They include extension settings and can include unrelated styles. Publish the extracted UserCSS file instead.
