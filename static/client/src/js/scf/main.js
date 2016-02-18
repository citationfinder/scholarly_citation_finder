require('angular');
require('angular-ui-router'); // exports: ui.router ($stateProvider, $urlRouterProvider)
//require('restangular');

angular.module('scf', ['ui.router'])
	
	// config
	.config(require('./config/routing'));

;