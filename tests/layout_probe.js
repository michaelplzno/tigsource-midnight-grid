// Read-only browser probe. Paste this entire expression in the preview's console.
// An active style, zero page overflow, loaded assets, and fitting panels are the
// basic regression signals. Inspect screenshots as well: this is not a pixel test.
(() => {
    const box = element => {
        const rect = element.getBoundingClientRect();
        return {left: Math.round(rect.left), right: Math.round(rect.right), width: Math.round(rect.width)};
    };
    const categories = [...document.querySelectorAll('#mainbody > .tborder:has(> :is(.catbg, .catbg2) + table.bordercolor)')];
    const posts = [...document.querySelectorAll('.post')];
    const postBodies = [...document.querySelectorAll('table:has(> tbody > tr > td > .post) > tbody')];
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
        topicRows: document.querySelectorAll('#quickModForm > .tborder2 > table > tbody > tr').length,
        postCount: posts.length,
        postColumns: postBodies.length ? getComputedStyle(postBodies[0]).gridTemplateColumns : null,
        panelsOutsideViewport: outside([...categories, ...posts, ...document.querySelectorAll('#showcase, .postbuttons')]),
        brokenImages: [...document.images].filter(image => !image.complete || image.naturalWidth === 0).length,
        embeddedVideos: document.querySelectorAll('iframe').length,
    };
    report.pass = report.themeActive && report.documentOverflow <= 1 && report.panelsOutsideViewport.length === 0 && report.brokenImages === 0;
    return report;
})()
