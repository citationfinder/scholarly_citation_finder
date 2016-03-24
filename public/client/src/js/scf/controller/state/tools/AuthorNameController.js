function AuthorNameController($scope, Restangular) {

	$scope.parsedName = undefined;

	$scope.parsename = function(name, normalize) {
		Restangular.all('tools/nameparser').customGET('humanname/', {
			name: name,
			normalize: normalize
		}).then(function(item) {
			$scope.parsedName = item;
			console.log(item);
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
}

AuthorNameController.$inject = ['$scope', 'Restangular'];

module.exports = AuthorNameController;