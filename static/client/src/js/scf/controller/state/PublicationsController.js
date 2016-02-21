function PublicationsController($scope, $stateParams, Restangular) {
	$scope.isCollapsed = true;

	$scope.getPublication = function(id) {
		Restangular.one('mag/publication', id).get().then(function(data) {
			console.log(data)
			$scope.publicationResult = data;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
	
	
	// Get routing params
	$scope.getPublication($stateParams.id);

}

PublicationsController.$inject = ['$scope', '$stateParams', 'Restangular'];

module.exports = PublicationsController;