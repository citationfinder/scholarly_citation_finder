function MagCitationsController($scope, $stateParams, Restangular) {
	
	$scope.task = {};
	$scope.isCollapsed = true;
	$scope.taskType = 'author'; // select default
	
	$scope.getTask = function(item) {
		$scope.task = item;
		if ($scope.task.status == 'SUCCESS') {
			Restangular.one('citation/mag/', item.id).getList().then(function(items) {
				console.log(items);
				$scope.task['result'] = items;
			}, function(data) {
				console.warn(data);
				$scope.addAlert(data.data);
			});
		}
	};
	
	$scope.submitTask = function(type, name, id) {
		Restangular.all('citation').customGET('mag/', {
			type: type,
			name: name,
			id: id
		}).then(function(data) {
			console.log(data);
			//$scope.getTasks();
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});		
	};
	
}

MagCitationsController.$inject = ['$scope', '$stateParams', 'Restangular'];

module.exports = MagCitationsController;