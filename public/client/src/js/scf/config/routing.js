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
	// PDF tools
	.state('find-pdf', {
		url: '/find-pdf',
		controller: require('../controller/state/pdf_tools/FindPdfController'),
		template: require('../view/state/pdf_tools/find_pdf.html')
	})
	.state('extract-pdf', {
		url: '/extract-pdf',
		controller: require('../controller/state/pdf_tools/ExtractPdfController'),
		template: require('../view/state/pdf_tools/extract_pdf.html')
	})
	// Other
	.state('find-citations', {
		url: '/find-citations',
		controller: require('../controller/state/FindCitationsController'),
		template: require('../view/state/find-citations.html')
	})
	.state('publications', {
		url: '/publications/:id',
		controller: require('../controller/state/PublicationsController'),
		template: require('../view/state/publications.html')
	})
	.state('mag-citations', {
		url: '/mag-citations',
		controller: require('../controller/state/MagCitationsController'),
		template: require('../view/state/mag-citations.html')
	})
	.state('harvester', {
		url: '/harvester',
		controller: require('../controller/state/HarvesterController'),
		template: require('../view/state/harvester.html')
	})
	.state('evaluation-authorset', {
		url: '/evaluation',
		controller: require('../controller/state/evaluation/AuthorSetController'),
		template: require('../view/state/evaluation/author_set.html')
	})
	.state('evaluation-run', {
		url: '/evaluation',
		controller: require('../controller/state/evaluation/RunController'),
		template: require('../view/state/evaluation/run.html')
	})
	;
}

routing.$inject = ['$stateProvider', '$urlRouterProvider'];
	
module.exports = routing;