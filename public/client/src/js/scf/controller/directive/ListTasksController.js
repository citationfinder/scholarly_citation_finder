function ListTasksController($scope, ApiFactory) {
	
	console.log($scope.tasktype);
	
	$scope.getTasks = function() {
		ApiFactory.getTasks($scope.tasktype, function(items) {
			$scope.tasks = items;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
	
	
	$scope.getTasks();
}

ListTasksController.$inject = ['$scope', 'ApiFactory'];

module.exports = ListTasksController;