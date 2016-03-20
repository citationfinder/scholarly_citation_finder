function ExtractPdfController($scope, Restangular) {
	
	$scope.extractors = [
		{id: 'grobid', label: 'Grobid'},
		{id: 'citeseer', label: 'Citeseer'}
	];
	
	$scope.taskExtractor = $scope.extractors[0].id;

	$scope.extractFile = function(extractor, url) {
		$scope.showProgress = true;
		Restangular.one('tools/extractor').customGET(extractor + '/', {url: url}).then(function(item) {
			$scope.extractFileDocumentMeta = item.document_meta;
			$scope.extractFileReferences = item.references;
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