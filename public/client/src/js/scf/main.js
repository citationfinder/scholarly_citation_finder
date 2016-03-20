require('angular');
require('angular-ui-router'); // exports: ui.router ($stateProvider, $urlRouterProvider)
require('lodash');
require('restangular');
//require('bootstrap-css-only'); // Bootstrap CSS

require('angular-bootstrap');

angular.module('scf', ['ui.router', 'restangular', 'ui.bootstrap'])
	
	// config
	.config(require('./config/api'))
	.config(require('./config/routing'))

	// controller
	.controller('mainController', require('./controller/MainController'))
	
	// factory
	.factory('ApiFactory', require('./factory/ApiFactory'))
	
	// directive
	.directive('listtasks', require('./directive/ListTasks'))
	.directive('listpublication', require('./directive/ListPublication'))
;