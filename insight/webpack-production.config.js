module.exports = require("./make-webpack-config")({
    // commonsChunk: true,
    node_env: 'production',
    longTermCaching: true,
    separateStylesheet: false,
    minimize: true
    // devtool: "source-map"
});
