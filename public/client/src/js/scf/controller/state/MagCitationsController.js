function MagCitationsController($scope, $stateParams, Restangular) {
	
	$scope.task = {};
	$scope.tasks = [];
	$scope.isCollapsed = true;
	
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
	
	$scope.submitTask = function(author_name, author_id) {
		Restangular.all('citation/mag/').customGET('', {
			author_name: author_name,
			author_id: author_id
		}).then(function(data) {
			console.log(data);
			$scope.getTasks();
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});		
	};
	
	
	$scope.getTasks()
}

MagCitationsController.$inject = ['$scope', '$stateParams', 'Restangular'];

module.exports = MagCitationsController;