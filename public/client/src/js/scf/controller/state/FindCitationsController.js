function FindCitationsController($scope, Restangular) {
	
	$scope.jobsResult = [
		{id: 231, date: '12:00', status: 'running'},
		{id: 315, date: '12:40', status: 'waiting'},
		{id: 313, date: '11:40', status: 'done'}		
	];
	
	$scope.getJobs = function() {
		// TODO
	};
	
	$scope.getAuthors = function(name) {
		Restangular.all('citation/author/').getList({author_name: name}).then(function(items) {
			console.log(items);
			$scope.authorsResult = items;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
}

FindCitationsController.$inject = ['$scope', 'Restangular'];

module.exports = FindCitationsController;