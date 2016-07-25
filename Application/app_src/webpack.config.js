var path = require("path");
var webpack = require("webpack");

var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');

var rootAssetPath = "./";
var file_loader = "file?context=" + rootAssetPath + "&name=[path][name].[hash].[ext]";

module.exports = {
  entry: {
    "app_js": ["babel-polyfill", "./lib/app.js"],
    "app_style": ["./styles/styles.scss"],
  } ,
  output: {
    path: "../static",
    publicPath:"/static/",
    filename: "[name].[hash].js",
    chunkFilename: "[id].[chunkhash].js"
  },
  resolve: {
    extensions: ["", ".js", ".css"]
  },
  // devtool: "source-map",
  module: {
    loaders: [
      //Sass
      {
        test: /\.s(c|a)ss$/,
        // TODO: MAKE WORK IN PRODUCTION
        // loader: multi(
        //               ["file?context=" + rootAssetPath + "&name=[path][name].[hash].css", "extract", "css?sourceMap", "resolve-url", "sass?sourceMap"].join("!"),
        //               ["style", "css", "resolve-url?fail", "sass?sourceMap"].join("!")
        //               )
        loaders: ["style", "css?sourceMap", "resolve-url", "sass?sourceMap"]
      },
      //Vue
      {
        test: /\.vue$/,
        loaders: ["vue"]
      },
      //JS (ES6)
      {
        test: /\.js$/,
        loaders: ["babel"],
        exclude: /node_modules/
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
      ignorePaths: ["node_modules", "webpack.config.js", "manifest.json", "package.json", ".babelrc"],
      // extensionsRegex: /\.scss$/
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    })
  ]
};
