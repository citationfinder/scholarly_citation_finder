function FindPdfController($scope, Restangular) {
	
	$scope.htmlParser = function(url) {
		Restangular.all('tools/crawler/htmlparser').getList({
			url: url
		}).then(function(items) {
			$scope.htmlParserResult = items;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
	
	$scope.searchEngine = function(keywords) {
		Restangular.all('tools/crawler/duckduckgo').getList({
			keywords: keywords
		}).then(function(items) {
			$scope.searchEngineResult = items;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
		
	};
}

FindPdfController.$inject = ['$scope', 'Restangular'];

module.exports = FindPdfController;