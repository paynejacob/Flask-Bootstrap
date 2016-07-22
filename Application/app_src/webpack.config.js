var path = require("path");
var webpack = require("webpack");

var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
var multi = require("multi-loader");

var rootAssetPath = ".";
var file_loader = "file?context=" + rootAssetPath + "&name=[path][name].[hash].[ext]";

module.exports = {
  entry: {
    "app_js": "./lib/app.js",
    "app_style": "./styles/styles.scss",
  } ,
  output: {
    path: "../static",
    publicPath:"/static/",
    filename: "[name].[hash].js"
  },
  // devtool: "source-map",
  module: {
    loaders: [
      //Sass
      {
        test: /\.s(c|a)ss$/,
        // loader: multi(
        loaders :
                      ["style", "css", "resolve-url?fail", "sass?sourceMap"]
                      // ["file?context=" + rootAssetPath + "&name=[path][name].[hash].css", "extract", "css?sourceMap", "resolve-url", "sass?sourceMap"].join("!")
                      // )
      },
      //Vue
      {
        test: /\.vue$/,
        loaders: ["vue"]
      },
      //Fonts
      {
        test : /\.(ttf|svg|eot|woff|woff2)$/,
        loaders: [file_loader]
      }
    ]
  },
  plugins:[
    new ManifestRevisionPlugin(path.join(rootAssetPath, "manifest.json"), {
      rootAssetPath: rootAssetPath,
      ignorePaths: ["node_modules", "webpack.config.js", "manifest.json", "package.json", "partials"]
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    })
  ]
};
