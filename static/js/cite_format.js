var cite_formatter = {
    'gost': {'journal-article': createGostArticle, 'book': createGostBook, 'book-chapter': createGostArticle},
    'apa': {'journal-article': createApaArticle, 'book': createApaBook, 'book-chapter': createApaArticle},
    'harvard': {
        'journal-article': createHarvardArticle,
        'book': createHarvardBook,
        'book-chapter': createHarvardArticle
    },
    'ieee': {'journal-article': createIeeeArticle, 'book': createIeeeArticle, 'book-chapter': createIeeeArticle}
};

function createGostArticle(author, title, container, issued, volume, issue, page, publisher) {
    var authors = author.split(', ');
    if (authors.length > 3)
        authors = authors.slice(0, 1).join(', ') + ' и др.';
    else
        authors = authors.join(', ');
    var gost = `${authors} ${title} // ${container}. – ${issued}.`;
    if (volume.length > 0)
        gost += ` – Т. ${volume}.`;
    if (issue.length > 0)
        gost += ` – №. ${issue}.`;
    if (page.length > 0)
        gost += ` – С. ${page.replace('-', '–')}.`;
    return gost
}

function createGostBook(author, title, container, issued, volume, issue, page, publisher) {
    var authors = author.split(', ');
    if (authors.length > 3)
        authors = authors.slice(0, 1) + ' и др.';
    else
        authors = authors.join(', ');
    var gost = `${authors} ${title}. – ${publisher}, – ${issued}.`;
    return gost;
}

function createApaArticle(author, title, container, issued, volume, issue, page, publisher) {
    var authors = author.split(', ');
    authors.forEach(function (val, i, a) {
        a[i] = val.replace(' ', ', ')
    });
    authors = formatArray(authors);
    var apa = `${authors} (${issued}). ${title}. ${container}, `;

    if (volume.length > 0) {
        apa += volume
    }
    if (issue.length > 0) {
        apa += `(${issue})`
    }
    if (page.length > 0) {
        if (page.includes('-'))
            apa += `, pp. ${page}.`;
        else
            apa += `, p. ${page}.`;
    }


    return apa
}

function createApaBook(author, title, container, issued, volume, issue, page, publisher) {
    var authors = author.split(', ');
    authors.forEach(function (val, i, a) {
        a[i] = val.replace(/ /g, ', ')
    });
    authors = formatArray(authors);
    var apa = `${authors} (${issued}). ${title}. ${publisher}`;
    return apa
}

function createHarvardArticle(author, title, container, issued, volume, issue, page, publisher) {
    var authors = author.split(', ');
    authors.forEach(function (val, i, a) {
        a[i] = val.replace(/ /g, ', ')
    });
    authors = formatArray(authors);
    var harvard = `${authors} (${issued}). ${title}. ${container}`;

    if (volume.length > 0) {
        addComma();
        harvard += `Volume ${volume}`
    }
    if (issue.length > 0) {
        addComma();
        harvard += ` (${issue})`
    }
    if (page.length > 0) {
        if (page.includes('-'))
            harvard += `, pp. ${page}.`;
        else
            harvard += `, p. ${page}.`;
    }

    var comma = false;

    function addComma() {
        if (!comma)
            harvard += ', ';
        comma = true;
    }

    return harvard
}

function createHarvardBook(author, title, container, issued, volume, issue, page, publisher) {
    var authors = author.split(', ');
    authors.forEach(function (val, i, a) {
        a[i] = val.replace(' ', ', ')
    });
    authors = formatArray(authors);
    var harvard = `${authors} (${issued}). ${title}. ${publisher}`;
    return harvard
}

function createIeeeArticle(author, title, container, issued, volume, issue, page, publisher) {
    var authors = author.split(', ');
    authors.forEach(function (val, i, a) {
        var parts = val.split(' ');
        a[i] = parts[1].replace(/\./g, '. ') + parts[0];
    });
    authors = formatArray(authors);
    var ieee = `${authors}, "${title}" in ${container}`

    if (volume.length > 0)
        ieee += `, Vol. ${volume}`;
    if (issue.length > 0)
        ieee += `, no. ${issue}`;
    if (publisher.length > 0)
        ieee += `, ${publisher}`;
    ieee += `, ${issued}`;
    if (page.length > 0) {
        if (page.includes('-'))
            ieee += `, pp. ${page}.`;
        else
            ieee += `, p. ${page}.`;
    }
    return ieee
}


function formatArray(arr) {
    var outStr = "";
    if (arr.length === 1) {
        outStr = arr[0];
    } else if (arr.length === 2) {
        //joins all with "and" but no commas
        //example: "bob and sam"
        outStr = arr.join(' and ');
    } else if (arr.length > 2) {
        //joins all with commas, but last one gets ", and" (oxford comma!)
        //example: "bob, joe, and sam"
        outStr = arr.slice(0, -1).join(', ') + ', and ' + arr.slice(-1);
    }
    return outStr;
}