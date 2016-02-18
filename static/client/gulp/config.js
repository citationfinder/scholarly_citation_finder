/*global require, module, __dirname */
module.exports = {
	serve: {
		port: 4000
	},
	watch: {
		webpack: ['src/js/**/*.js', 'src/js/**/*.html'],
		reload: ['index.html', 'dist/scf.min.js']
	},
	webpack: {
		src: '../../webpack.config.js'
	}
};