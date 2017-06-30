var page = require('webpage').create();

page.viewportSize = {width: 826, height: 1122 };
page.paperSize = {
    margin: {top: 0, right: 0, bottom: 0, left: 0},
    width: '826px',
    height: '1122px'
};
page.open('templates/html/rendered.html', function(status) {
    window.setTimeout(function() {
        document.body.style.width = "826px";
        document.body.style.height = "1122px";
        page.render('analytics.png');
        phantom.exit();
    }, 5000);
})
