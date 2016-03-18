function AuthorNameController($scope, Restangular) {

	$scope.parsedName = undefined;

	$scope.parsename = function(name) {
		Restangular.all('crawler/').customGET('nameparser/', {name: name}).then(function(item) {
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