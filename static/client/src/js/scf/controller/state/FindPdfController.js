function FindPdfController($scope, Restangular) {
	
	$scope.htmlParser = function(url) {
		Restangular.all('crawler/htmlparser').getList({url: url}).then(function(items) {
			$scope.htmlParserResult = items;
		}, function(data) {
			console.warn('error');
			console.warn(data);
		});
	};
	
	$scope.searchEngine = function(keywords) {
		Restangular.all('crawler/duckduckgo').getList({keywords: keywords}).then(function(items) {
			$scope.searchEngineResult = items;
		}, function(data) {
			console.warn('error');
			console.warn(data);
		});
		
	};
}

FindPdfController.$inject = ['$scope', 'Restangular'];

module.exports = FindPdfController;