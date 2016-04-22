function FindCitationsController($scope, Restangular) {
	
	$scope.task = {};
	//$scope.isCollapsed = true;
	$scope.taskType = 'author'; // select default
	
	$scope.getTask = function(item) {
		$scope.task = item;
		if ($scope.task.status == 'SUCCESS') {
			// TODO: see MagCitationsController
		}
	};

	$scope.submitTask = function(type, name, id, strategy) {
		Restangular.all('citation/citations/').customPOST(strategy, 'find/', {
			type: type,
			name: name,
			id: id
		}, {}).then(function(data) {
			console.log(data);
			$scope.addAlert('Create task');
			//$scope.isCollapsed = true;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});		
	};

}

FindCitationsController.$inject = ['$scope', 'Restangular'];

module.exports = FindCitationsController;