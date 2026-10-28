// Read-only browser probe. Paste this entire expression in the preview's console.
// Check alignment, matching controls, separate counts, overflow, and local assets.
// Inspect screenshots as well: this is not a pixel test.
(() => {
    const box = element => {
        const rect = element.getBoundingClientRect();
        return {left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width)};
    };
    const categories = [...document.querySelectorAll('#mainbody > .tborder:has(> :is(.catbg, .catbg2) + table.bordercolor)')];
    const posts = [...document.querySelectorAll('.post')];
    const postBodies = [...document.querySelectorAll('table:has(> tbody > tr > td > .post) > tbody')];
    const sections = [...document.querySelectorAll('#mainbody > .tborder:has(> table.bordercolor a[name^="b"])')];
    const boardRows = [...document.querySelectorAll('#mainbody > .tborder > table.bordercolor:has(a[name^="b"]) > tbody > tr:not(:has(> td[colspan]))')];
    const searchControls = [...document.querySelectorAll('#showcase form input[type="text"], #showcase form input[type="submit"]')];
    const sectionBoxes = sections.map(element => element.getBoundingClientRect());
    const expectedColumns = innerWidth >= 1800 ? 4 : innerWidth >= 1440 ? 3 : innerWidth >= 1000 ? 2 : 1;
    const tileGrids = categories.length ? [document.querySelector('#mainbody')] : [];
    const tiles = categories.flatMap(category => [...category.querySelector(':scope > table.bordercolor > tbody').children]
        .filter(row => !row.querySelector(':scope > td[colspan]')));
    const tilesFor = () => tiles;
    const tileHeights = tiles.map(tile => tile.getBoundingClientRect().height);
    const expectedTileHeight = +getComputedStyle(document.documentElement).getPropertyValue('--tig-tile-height').trim().replace('px', '');
    const tileProblems = [];
    for (const grid of tileGrids) {
        const members = tilesFor(grid);
        const rowCount = Math.ceil(members.length / expectedColumns);
        const tracks = getComputedStyle(grid).gridTemplateColumns.trim().split(/\s+/).length;
        if (tracks !== expectedColumns) tileProblems.push('Incorrect column count');
        members.forEach((tile, index) => {
            const rect = tile.getBoundingClientRect();
            const style = getComputedStyle(tile);
            const column = Math.floor(index / rowCount);
            const row = index % rowCount;
            if (Math.abs(rect.height - expectedTileHeight) > 1) tileProblems.push('Tile does not match the configured fixed height');
            if (Number(style.gridColumnStart) !== column + 1 || Number(style.gridRowStart) !== row + 4)
                tileProblems.push('Incorrect column-major order');
            if (row) {
                const above = members[index - 1].getBoundingClientRect();
                if (Math.abs(rect.top - above.bottom - 16) > 1) tileProblems.push('Incorrect vertical gutter');
            }
            if (column) {
                const left = members[index - rowCount].getBoundingClientRect();
                if (Math.abs(rect.left - left.right - 16) > 1) tileProblems.push('Incorrect horizontal gutter');
            }
            if (tile.scrollHeight > tile.clientHeight + 2) tileProblems.push('Tile content exceeds its height');
            const stats = tile.children[2].getBoundingClientRect();
            const latest = tile.children[3].getBoundingClientRect();
            const title = tile.querySelector('a[name^="b"]').parentElement.getBoundingClientRect();
            if (stats.top < title.bottom || stats.top - title.bottom > 6)
                tileProblems.push('Counts are not directly beneath the board title');
            const firstTile = members[0].getBoundingClientRect();
            const firstLatest = members[0].children[3].getBoundingClientRect();
            if (Math.abs((latest.top - rect.top) - (firstLatest.top - firstTile.top)) > 1)
                tileProblems.push('Latest-post first lines do not align');
            const joystick = tile.children[0].querySelector('img');
            if (joystick) {
                const bounds = joystick.getBoundingClientRect();
                if (Math.abs(bounds.width - joystick.naturalWidth) > 1 || Math.abs(bounds.height - joystick.naturalHeight) > 1)
                    tileProblems.push('Joystick is not its original size');
                const description = tile.children[1].querySelector(':scope > span:not(:has(a[name^="b"]))');
                if (description && description.getBoundingClientRect().top < bounds.bottom)
                    tileProblems.push('Joystick overlaps the description');
            }
            const label = getComputedStyle(tile.children[1], '::before').content;
            if (!label || label === 'none' || label === '""') tileProblems.push('Tile is missing its section label');
            for (const cell of [...tile.children, ...tile.children[1].children]) {
                const bounds = cell.getBoundingClientRect();
                if (!bounds.width || !bounds.height) continue;
                if (bounds.top < rect.top || bounds.bottom > rect.bottom || bounds.left < rect.left || bounds.right > rect.right)
                    tileProblems.push('Cell extends outside its tile');
            }
            for (const part of tile.children[1].children) {
                const bounds = part.getBoundingClientRect();
                if (bounds.width && bounds.height && bounds.bottom > latest.top - 2)
                    tileProblems.push('Description or moderator overlaps latest post');
            }
            const footer = tile.nextElementSibling;
            if (footer?.querySelector(':scope > td[colspan]')) {
                const bounds = footer.getBoundingClientRect();
                const metadata = tile.children[3].getBoundingClientRect();
                if (bounds.left < rect.left || bounds.right > rect.right || bounds.bottom > rect.bottom + 1 ||
                    bounds.top < metadata.bottom + 8) tileProblems.push('Child-board footer does not fit its parent tile');
            }
        });
    }
    const alignedSections = categories.length ? tileProblems.length === 0 : sectionBoxes.every((rect, index) => !index || (
        Math.abs(rect.left - sectionBoxes[0].left) <= 1 &&
        Math.abs(rect.right - sectionBoxes[0].right) <= 1 &&
        rect.top >= sectionBoxes[index - 1].bottom
    ));
    const overlappingCounts = [...document.querySelectorAll('#quickModForm > .tborder2 > table > tbody > tr:not(:has(> .catbg3))')].filter(row => {
        if (row.children.length !== 8) return false;
        const replies = row.children[4].getBoundingClientRect();
        const views = row.children[5].getBoundingClientRect();
        return Math.min(replies.right, views.right) > Math.max(replies.left, views.left) + 1 &&
            Math.min(replies.bottom, views.bottom) > Math.max(replies.top, views.top) + 1;
    }).length;
    const heights = searchControls.map(element => element.getBoundingClientRect().height);
    const infoWidths = boardRows.map(row => {
        const info = row.children[1];
        return (getComputedStyle(info).display === 'contents' ? info.querySelector('a[name^="b"]').parentElement : info).getBoundingClientRect().width;
    }).filter(width => width > 0);
    const sectionColors = categories.map(category => getComputedStyle(category).getPropertyValue('--tig-section-accent').trim());
    if (sectionColors.some(color => !color) || new Set(sectionColors).size !== categories.length)
        tileProblems.push('Sections do not have distinct accent colors');
    const outside = elements => elements.filter(element => {
        const rect = element.getBoundingClientRect();
        return rect.width > 0 && (rect.left < -1 || rect.right > innerWidth + 1);
    }).map(element => ({tag: element.tagName, class: element.className, ...box(element)}));
    const report = {
        page: location.pathname,
        viewport: innerWidth,
        themeActive: getComputedStyle(document.documentElement).getPropertyValue('--tig-bg').trim() !== '',
        documentOverflow: Math.max(0, document.documentElement.scrollWidth - innerWidth),
        categoryCount: categories.length,
        categoryColumns: tileGrids.length ? getComputedStyle(tileGrids[0]).gridTemplateColumns : null,
        expectedCategoryColumns: categories.length ? expectedColumns : null,
        actualCategoryColumns: tileGrids.length ? getComputedStyle(tileGrids[0]).gridTemplateColumns.trim().split(/\s+/).length : null,
        boardTileCount: tiles.length,
        continuousGrid: tileGrids.length === 1,
        sectionLabels: [...new Set(tiles.map(tile => getComputedStyle(tile.children[1], '::before').content))],
        sectionColors,
        tileHeights: [...new Set(tileHeights.map(height => Math.round(height)))],
        tileProblems,
        alignedSections,
        boardRowCount: boardRows.length,
        minimumBoardInfoWidth: infoWidths.length ? Math.round(Math.min(...infoWidths)) : null,
        searchControlHeights: heights.map(value => Math.round(value * 100) / 100),
        overlappingCountCells: overlappingCounts,
        bodyFontSize: getComputedStyle(document.body).fontSize,
        topicRows: document.querySelectorAll('#quickModForm > .tborder2 > table > tbody > tr').length,
        postCount: posts.length,
        postColumns: postBodies.length ? getComputedStyle(postBodies[0]).gridTemplateColumns : null,
        panelsOutsideViewport: outside([...sections, ...boardRows, ...posts, ...document.querySelectorAll('#showcase, .postbuttons')]),
        brokenImages: [...document.images].filter(image => !image.complete || image.naturalWidth === 0).length,
        embeddedVideos: document.querySelectorAll('iframe').length,
    };
    report.pass = report.themeActive && tileProblems.length === 0 && report.documentOverflow <= 1 && report.panelsOutsideViewport.length === 0 &&
        report.brokenImages === 0 && alignedSections && overlappingCounts === 0 &&
        (!categories.length || report.actualCategoryColumns === expectedColumns) &&
        (!infoWidths.length || Math.min(...infoWidths) >= 160) &&
        (!heights.length || Math.max(...heights) - Math.min(...heights) <= 1);
    return report;
})()
