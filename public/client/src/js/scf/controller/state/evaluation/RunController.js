function RunController($scope, Restangular) {
	
	//$scope.isCollapsed = true;
	//$scope.task = {};
	
	$scope.submitTask = function(name, strategy) {
		Restangular.one('citation/evaluation/run/', name + '/').customPOST(strategy, '', {}, {}).then(function(data) {
			console.log(data);
			$scope.addAlert('Create task');
			//$scope.isCollapsed = true;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});		
	};

}

RunController.$inject = ['$scope', 'Restangular'];

module.exports = RunController;