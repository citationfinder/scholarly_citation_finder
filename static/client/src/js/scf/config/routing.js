/**
 * Configure the routing of the Angular module. For routing the module uses
 * the "ui.router" module.
 * 
 * @param {Object} $stateProvider From module ui.router
 * @param {Object} $urlRouterProvider From module ui.router
 */
function routing($stateProvider, $urlRouterProvider) {
	// Default route
	$urlRouterProvider.otherwise('/home');

	// Set up the states
	$stateProvider
	.state('home', {
		url: '/home',
		template: require('../view/state/home.html')
	})
	.state('find-pdf', {
		url: '/find-pdf',
		controller: require('../controller/state/FindPdfController'),
		template: require('../view/state/find-pdf.html')
	})
	.state('extract-pdf', {
		url: '/extract-pdf',
		controller: require('../controller/state/ExtractPdfController'),
		template: require('../view/state/extract-pdf.html')
	})
	;		
}

routing.$inject = ['$stateProvider', '$urlRouterProvider'];
	
module.exports = routing;