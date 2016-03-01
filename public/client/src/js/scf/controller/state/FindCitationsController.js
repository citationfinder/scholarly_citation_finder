function FindCitationsController($scope, Restangular) {
	
	//$scope.isCollapsed = true;
	
	$scope.submitTask = function(author_name, author_id, strategy) {
		// POST /accounts/123/messages?param=myParam with the body of name: "My Message"
		Restangular.all('citation/evaluation/find/').customPOST(strategy, '', {
			author_name: author_name,
			author_id: author_id
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