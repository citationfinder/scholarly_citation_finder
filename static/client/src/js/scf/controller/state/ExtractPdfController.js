function ExtractPdfController($scope, Restangular) {
	console.log('yolo');
	
	$scope.extractFile = function(url) {
		Restangular.all('extractor').getList({url: url}).then(function(items) {
			$scope.extractFileResult = items;
		}, function(data) {
			console.log('error');
			$scope.extractFileResult = data;
			console.warn(data);
		});
	};
}

ExtractPdfController.$inject = ['$scope', 'Restangular'];

module.exports = ExtractPdfController;