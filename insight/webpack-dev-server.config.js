module.exports = require("./make-webpack-config")({
    node_env: 'development',
	devServer: true,
	devtool: "eval",
	debug: true,
	// commonsChunk: true
});
