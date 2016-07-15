var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
var rootAssetPath = "."

module.exports = {
  entry: "./lib/app.js",
  output: {
    path: "../static",
    publicPath:"http://localhost:8081/",
    filename: "app.bundle.js"
  },
  module: {
    loaders: [
      //Sass
      {
        test: /\.scss$/,
        loaders: ["style", "css", "sass"]
        // "file?context=" + rootAssetPath + "&name=[path][name].[hash].[ext]"]
      },
      //Vue
      {
        test: /\.vue$/,
        loaders :["vue"]
      }
    ]
  },
  plugins:[
    new ManifestRevisionPlugin("./manifest.json", {
      rootAssetPath: rootAssetPath,
      ignorePaths: ["/node_modules", "webpack.config.js", "manifest.json", "package.json", "partials"]
    })
  ]
}
