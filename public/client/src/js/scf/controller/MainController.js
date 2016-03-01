function MainController($scope) {
	$scope.alerts = [];
	
	$scope.addAlert = function(msg) {
		$scope.alerts.push({msg: msg.substr(0, 300)});
	};

	$scope.closeAlert = function(index) {
		$scope.alerts.splice(index, 1);
	};
}

MainController.$inject = ['$scope'];

module.exports = MainController;