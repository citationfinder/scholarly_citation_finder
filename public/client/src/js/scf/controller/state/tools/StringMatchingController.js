function StringMatchingController($scope, Restangular) {

	$scope.stringmatchingResult = undefined;

	$scope.stringmatching = function(first, second) {
		Restangular.all('tools/nameparser').customGET('stringmatching/', {
			first: first,
			second: second
		}).then(function(item) {
			$scope.stringmatchingResult = item;
			console.log(item);
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
}

StringMatchingController.$inject = ['$scope', 'Restangular'];

module.exports = StringMatchingController;