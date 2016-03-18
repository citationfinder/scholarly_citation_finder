function ExtractPdfController($scope, Restangular) {
	
	$scope.extractors = [
		{id: 'grobid', label: 'Grobid'},
		{id: 'citeseer', label: 'Citeseer'}
	];
	
	$scope.taskExtractor = $scope.extractors[0].id;

	$scope.extractFile = function(extractor, url) {
		$scope.showProgress = true;
		Restangular.all('tools/extractor/' + extractor + '/').getList({url: url}).then(function(items) {
			$scope.extractFileResult = items;
			$scope.showProgress = false;
		}, function(data) {
			$scope.showProgress = false;
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
}

ExtractPdfController.$inject = ['$scope', 'Restangular'];

module.exports = ExtractPdfController;