function HarvesterController($scope, Restangular) {
	
	$scope.oaipmhProvider = []
	
	$scope.getOaipmhProvider = function() {
		Restangular.all('rest/default/harvester/oaipmhprovider/').getList().then(function(items) {
			console.log(items);
			$scope.oaipmhProvider = items;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
	
	$scope.submitTask = function(name, limit, from, until) {
		Restangular.all('harvester/oaipmh/').customGET(name, {
			limit: limit,
			from: from,
			until: until
		}).then(function(data) {
			console.log(data);
			//$scope.getTasks();
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	}
	
	
	$scope.getOaipmhProvider();
}

HarvesterController.$inject = ['$scope', 'Restangular'];

module.exports = HarvesterController;