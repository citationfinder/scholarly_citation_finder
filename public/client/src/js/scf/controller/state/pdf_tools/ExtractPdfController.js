function ExtractPdfController($scope, Restangular) {
	$scope.extractFile = function(url) {
		$scope.showProgress = true;
		Restangular.all('extractor').getList({url: url}).then(function(items) {
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