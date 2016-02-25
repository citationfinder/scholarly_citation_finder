/**
 * Factory to receive data from the API.
 * 
 * @param {angular.provider} Restangular From restangular
 */
function ApiFactory(Restangular) {
	
	return {
		getTasks: function (type, success, failure) {
			Restangular.all('rest/default/tasks/').getList({type: type}).then(function(items) {
				success(items);
			}, function(data) {
				failure(data);
			});
		} 
	};
}

ApiFactory.$inject = ['Restangular'];

module.exports = ApiFactory;