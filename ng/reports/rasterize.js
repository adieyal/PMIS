var page = require('webpage').create(),
    system = require('system'),
    address, output, size;

if (system.args.length < 3 || system.args.length > 5) {
    console.log('Usage: rasterize.js URL filename');
    phantom.exit(1);
} else {
    address = system.args[1];
    output = system.args[2];
    page.viewportSize = { width: 2100, height: 2970 };
    page.paperSize = { width: '12375px', height: '17585px', border: '80px', dpi: 300 };
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
        } else {
            window.setTimeout(function () {
                page.render(output);
                phantom.exit();
            }, 1000);
        }
    });
}
