function FindPdfController($scope, Restangular) {
	console.log('yolo');
	
	$scope.htmlParser = function(url) {
		Restangular.all('crawler/htmlparser').getList({url: url}).then(function(items) {
			$scope.htmlParserResult = items;
		}, function(data) {
			console.log('error');
			console.log(data);
		});
	};
	
	$scope.searchEngine = function(keywords) {
		Restangular.all('crawler/duckduckgo').getList({keywords: keywords}).then(function(items) {
			$scope.searchEngineResult = items;
		}, function(data) {
			console.log('error');
			console.log(data);
		});
		
	};
}

FindPdfController.$inject = ['$scope', 'Restangular'];

module.exports = FindPdfController;