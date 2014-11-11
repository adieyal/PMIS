var path = require("path");
var webpack = require("webpack");
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var loadersByExtension = require("./config/loadersByExtension");
var joinEntry = require("./config/joinEntry");

module.exports = function(options) {
	var entry = {
		main: reactEntry("Main")
		// second: reactEntry("Second")
	};
	var loaders = {
		"coffee": "coffee-redux",
		"jsx": options.hotComponents ? ["react-hot", "jsx?harmony"] : "jsx",
		"json": "json",
		"json5": "json5",
		"txt": "raw",
		"png|jpg|jpeg|gif|svg": "url?limit=10000",
		"woff": "url?limit=100000",
		"ttf|eot": "file",
		"wav|mp3": "file",
		"html": "html",
		"md|markdown": ["html", "markdown"],
	};
	var stylesheetLoaders = {
		"css": "css",
		"less": "css!less",
		"styl": "css!stylus",
		"sass|scss": "css!sass",
	};
	var additionalLoaders = [
		// { test: /some-reg-exp$/, loader: "any" }
	];
	var alias = {

	};
	var aliasLoader = {

	};
	var externals = [

	];
	var modulesDirectories = ["web_modules", "node_modules"];
	var extensions = ["", ".web.js", ".js", ".jsx"];
	var root = path.join(__dirname, "app");
	var output = {
		path: path.join(__dirname, "build", options.prerender ? "prerender" : "public"),
		publicPath: "/",
		filename: "[name].js" + (options.longTermCaching && !options.prerender ? "?[chunkhash]" : ""),
		chunkFilename: (options.devServer ? "[id].js" : "[name].js") + (options.longTermCaching && !options.prerender ? "?[chunkhash]" : ""),
		sourceMapFilename: "debugging/[file].map",
		libraryTarget: options.prerender ? "commonjs2" : undefined,
		pathinfo: options.debug,
	};
	var plugins = [
		function() {
			if(!options.prerender) {
				this.plugin("done", function(stats) {
					require("fs").writeFileSync(path.join(__dirname, "build", "stats.json"), JSON.stringify(stats.toJson({
						chunkModules: true,
						exclude: [
							/node_modules[\\\/]react/
						]
					})));
				});
			}
		},
		new webpack.PrefetchPlugin("react"),
		new webpack.PrefetchPlugin("react/lib/ReactComponentBrowserEnvironment")
	];
	if(options.prerender) {
		aliasLoader["react-proxy$"] = "react-proxy/unavailable";
		externals.push(/^react(\/.*)?$/, /^reflux(\/.*)?$/);
		plugins.push(new webpack.optimize.LimitChunkCountPlugin({ maxChunks: 1 }));
	}
	if(options.commonsChunk) {
		plugins.push(new webpack.optimize.CommonsChunkPlugin("commons", "commons.js" + (options.longTermCaching && !options.prerender ? "?[chunkhash]" : "")));
	}


	function reactEntry(name) {
		return (options.prerender ? "./config/prerender?" : "./config/app?") + name;
	}
	if(options.devServer) {
		if(options.hot) {
			entry = joinEntry("webpack/hot/dev-server", entry);
		}
		entry = joinEntry("webpack-dev-server/client?http://localhost:2992", entry);
	}
	Object.keys(stylesheetLoaders).forEach(function(ext) {
		var loaders = stylesheetLoaders[ext];
		if(Array.isArray(loaders)) loaders = loaders.join("!");
		if(options.prerender) {
			stylesheetLoaders[ext] = "null";
		} else if(options.separateStylesheet) {
			stylesheetLoaders[ext] = ExtractTextPlugin.extract("style", loaders);
		} else {
			stylesheetLoaders[ext] = "style!" + loaders;
		}
	});
	if(options.separateStylesheet && !options.prerender) {
		plugins.push(new ExtractTextPlugin("[name].css"));
	}
	if(options.minimize) {
		plugins.push(
			new webpack.optimize.UglifyJsPlugin(),
			new webpack.optimize.DedupePlugin(),
			new webpack.DefinePlugin({
				"process.env": {
					NODE_ENV: JSON.stringify("production")
				}
			})
		);
	}

	return {
		entry: entry,
		output: output,
		target: options.prerender ? "node" : "web",
		module: {
			loaders: loadersByExtension(loaders).concat(loadersByExtension(stylesheetLoaders))
		},
		devtool: options.devtool,
		debug: options.debug,
		resolveLoader: {
			root: path.join(__dirname, "node_modules"),
			alias: aliasLoader
		},
		externals: externals,
		resolve: {
			root: root,
			modulesDirectories: modulesDirectories,
			extensions: extensions,
			alias: alias,
		},
		plugins: plugins
	};
};
