function EvaluationCitationsController($scope, $stateParams, Restangular) {
	
	$scope.isCollapsed = true;
	$scope.task = {};
	
	$scope.submitTask = function(name, setsize, num_min_publications) {
		Restangular.all('citation/evaluation/create/').customGET(name, {
			setsize: setsize,
			num_min_publications: num_min_publications
		}).then(function(data) {
			console.log(data);
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});		
	};
	
	$scope.getTask = function(item) {
		$scope.task = item;
		if ($scope.task.status == 'SUCCESS') {
			Restangular.one('citation/evaluation/create/', item.id).get().then(function(csv) {
				console.log(csv);
				$scope.task['result'] = csv;
			}, function(data) {
				console.warn(data);
				$scope.addAlert(data.data);
			});
		}
	};

}

EvaluationCitationsController.$inject = ['$scope', '$stateParams', 'Restangular'];

module.exports = EvaluationCitationsController;