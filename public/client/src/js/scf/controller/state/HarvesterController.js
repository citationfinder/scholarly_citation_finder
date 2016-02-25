function HarvesterController($scope, Restangular) {
	
	$scope.oaipmhProvider = []
	
	$scope.getOaipmhProvider = function() {
		Restangular.all('rest/default/oaipmhprovider/').getList().then(function(items) {
			console.log(items);
			$scope.oaipmhProvider = items;
		}, function(data) {
			console.warn(data);
			$scope.addAlert(data.data);
		});
	};
	
	
	$scope.getOaipmhProvider();
}

HarvesterController.$inject = ['$scope', 'Restangular'];

module.exports = HarvesterController;