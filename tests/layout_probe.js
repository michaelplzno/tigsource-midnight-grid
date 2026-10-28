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
    const categoryBoxes = categories.map(element => element.getBoundingClientRect());
    const gridRows = [];
    for (const rect of categoryBoxes) {
        let row = gridRows.find(row => Math.abs(row[0].top - rect.top) <= 1);
        if (!row) { row = []; gridRows.push(row); }
        row.push(rect);
    }
    const expectedColumns = innerWidth >= 1440 ? 3 : innerWidth >= 1000 ? 2 : 1;
    const alignedSections = categories.length ? gridRows.every((row, index) =>
        row.every((rect, column) => Math.abs(rect.bottom - row[0].bottom) <= 1 &&
            Math.abs(rect.width - categoryBoxes[0].width) <= 1 &&
            (!column || Math.abs(rect.left - row[column - 1].right - 20) <= 1)) &&
        (!index || Math.abs(row[0].top - gridRows[index - 1][0].bottom - 20) <= 1)
    ) : sectionBoxes.every((rect, index) => !index || (
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
    const infoWidths = boardRows.map(row => row.children[1]?.getBoundingClientRect().width).filter(width => width > 0);
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
        categoryColumns: categories.length ? getComputedStyle(document.querySelector('#mainbody')).gridTemplateColumns : null,
        expectedCategoryColumns: categories.length ? expectedColumns : null,
        actualCategoryColumns: categories.length ? Math.max(...gridRows.map(row => row.length)) : null,
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
    report.pass = report.themeActive && report.documentOverflow <= 1 && report.panelsOutsideViewport.length === 0 &&
        report.brokenImages === 0 && alignedSections && overlappingCounts === 0 &&
        (!categories.length || report.actualCategoryColumns === expectedColumns) &&
        (!infoWidths.length || Math.min(...infoWidths) >= 160) &&
        (!heights.length || Math.max(...heights) - Math.min(...heights) <= 1);
    return report;
})()
