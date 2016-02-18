require('angular');
require('angular-ui-router'); // exports: ui.router ($stateProvider, $urlRouterProvider)
require('lodash')
require('restangular');

angular.module('scf', ['ui.router', 'restangular'])
	
	// config
	.config(require('./config/api'))
	.config(require('./config/routing'))

;