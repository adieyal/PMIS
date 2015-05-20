module.exports = require("./make-webpack-config")({
    node_env: 'development',
	hot: true,
	devServer: true,
	hotComponents: true,
	devtool: "eval",
	debug: true
});
