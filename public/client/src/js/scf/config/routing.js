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
	// Tools
	.state('tools-find-pdf', {
		url: '/tools/find-pdf',
		controller: require('../controller/state/tools/FindPdfController'),
		template: require('../view/state/tools/find_pdf.html')
	})
	.state('tools-extract-pdf', {
		url: '/tools/extract-pdf',
		controller: require('../controller/state/tools/ExtractPdfController'),
		template: require('../view/state/tools/extract_pdf.html')
	})
	.state('tools-author-name', {
		url: '/tools/author-name',
		controller: require('../controller/state/tools/AuthorNameController'),
		template: require('../view/state/tools/author_name.html')
	})
	.state('tools-string-matching', {
		url: '/tools/string-matching',
		controller: require('../controller/state/tools/StringMatchingController'),
		template: require('../view/state/tools/string_matching.html')
	})
	.state('tools-doi', {
		url: '/tools/doi',
		controller: require('../controller/state/tools/DoiController'),
		template: require('../view/state/tools/doi.html')
	})	
	// Other
	.state('find-citations', {
		url: '/find-citations',
		controller: require('../controller/state/FindCitationsController'),
		template: require('../view/state/find-citations.html')
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
		url: '/evaluation-authorset',
		controller: require('../controller/state/evaluation/AuthorSetController'),
		template: require('../view/state/evaluation/author_set.html')
	})
	.state('evaluation-run', {
		url: '/evaluation-run',
		controller: require('../controller/state/evaluation/RunController'),
		template: require('../view/state/evaluation/run.html')
	})
	;
}

routing.$inject = ['$stateProvider', '$urlRouterProvider'];
	
module.exports = routing;