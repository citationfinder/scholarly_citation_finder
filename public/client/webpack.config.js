// webpack.config.js
var path = require("path");
var webpack = require('webpack');

module.exports = {
    entry: {
        'scf': './src/js/scf/main.js'
    },
    output: {
        filename: 'dist/[name].min.js'
    },
    module: {
        loaders: [
            { test: /\.css$/, loader: 'style-loader!css-loader' },
            { test: /\.html$/, loader: 'html' }
        ]
     },
     resolve: {
         root: [path.join(__dirname, './bower_components')]
     },
     plugins: [
         new webpack.ResolverPlugin(
             new webpack.ResolverPlugin.DirectoryDescriptionFilePlugin('bower.json', ['main'])
         )
     ]
};