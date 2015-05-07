module.exports = [
	require("./make-webpack-config")({
		// commonsChunk: true,
		longTermCaching: true,
		separateStylesheet: false,
		minimize: true,
		output_path: "build/production"
		// devtool: "source-map"
	}),
	require("./make-webpack-config")({
		prerender: true,
		output_path: "build/production"
	})
];
