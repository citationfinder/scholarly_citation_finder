function DoiController($scope, Restangular) {

	$scope.queryDoiResult = undefined;
	$scope.queryResult = undefined;

	$scope.queryDoi = function(doi) {
		$scope.showProgressDoi = true;
		Restangular.all('tools/crawler').customGET('crossref', {
			doi: doi
		}).then(function(item) {
			$scope.queryDoiResult = item;
			console.log(item);
			$scope.showProgressDoi = false;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
			$scope.showProgressDoi = false;
		});
	};

	$scope.query = function(query) {
		$scope.showProgress = true;
		Restangular.all('tools/crawler/crossref').getList({
			query: query
		}).then(function(item) {
			$scope.queryResult = item;
			console.log(item);
			$scope.showProgress = false;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
			$scope.showProgress = false;
		});
	};
}

DoiController.$inject = ['$scope', 'Restangular'];

module.exports = DoiController;