var express = require("express");
var path = require("path");
var prerenderApplication  = require("../" + process.env.BUILD_FOLDER + "/prerender/main.js");
var stats = require("../" + process.env.BUILD_FOLDER + "/stats.json");

var STYLE_URL = "main.css?" + stats.hash;
var SCRIPT_URL = [].concat(stats.assetsByChunkName.main)[0];
var COMMONS_URL = [].concat(stats.assetsByChunkName.commons)[0];

var app = express();

app.use(express.static(path.join(__dirname, "..", process.env.BUILD_FOLDER, "public"), {
	maxAge: "200d"
}));

app.get("/*", function(req, res) {
	res.contentType = "text/html; charset=utf8";
	res.end(prerenderApplication(SCRIPT_URL, STYLE_URL, COMMONS_URL));
});

app.listen(+(process.env.PORT || 8082));
