/*global require, module, __dirname */
var config = require('../config').watch,
	browserSync = require('browser-sync'),
	path = require('path'),
	gulp = require('gulp');

gulp.task('watch', ['serve'], function () {
    //gulp.watch(config.styles, ['styles']);
	gulp.watch(config.webpack, ['webpack']);
	gulp.watch(config.reload).on('change', browserSync.reload);
});