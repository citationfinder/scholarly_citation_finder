require('angular');
require('angular-ui-router'); // exports: ui.router ($stateProvider, $urlRouterProvider)
require('lodash')
require('restangular');

require('angular-bootstrap');

angular.module('scf', ['ui.router', 'restangular', 'ui.bootstrap'])
	
	// config
	.config(require('./config/api'))
	.config(require('./config/routing'))

;