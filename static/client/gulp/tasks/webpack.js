/*global require, module, __dirname */
var config = require('../config').webpack,
	webpack = require('webpack'),
	gulp = require('gulp'),
	$ = require('gulp-load-plugins')();

gulp.task('webpack', function(callback) {
    webpack(require(config.src), function(err, stats) {
        if(err) throw new $.util.PluginError('webpack', err);
        $.util.log('[webpack]', stats.toString({
            // output options
        }));
        callback();
    });
});