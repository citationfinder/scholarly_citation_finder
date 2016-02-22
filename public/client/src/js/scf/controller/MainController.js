function MainController($scope) {
	$scope.alerts = [];
	
	$scope.addAlert = function(msg) {
		$scope.alerts.push({msg: msg});
	};

	$scope.closeAlert = function(index) {
		$scope.alerts.splice(index, 1);
	};
}

MainController.$inject = ['$scope'];

module.exports = MainController;