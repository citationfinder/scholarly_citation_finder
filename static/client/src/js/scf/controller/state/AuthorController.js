function AuthorController($scope, Restangular) {
	
	$scope.getAuthor = function(name) {
		Restangular.one('citation/author/').get({author_name: name}).then(function(data) {
			console.log(data);
			$scope.authorResult = data;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
}

AuthorController.$inject = ['$scope', 'Restangular'];

module.exports = AuthorController;