function api(RestangularProvider) {
	// Used for local development only
	if (window.location.host === 'localhost:4000') {
		RestangularProvider.setBaseUrl('http://localhost:8000/api/');
		//RestangularProvider.setDefaultHttpFields({
		//	'withCredentials': true
		//});
		//RestangularProvider.setDefaultHeaders({
		//	'Content-Type': 'application/json',
		//	'X-Requested-With': 'XMLHttpRequest'
		//});
	} else {
		// Base URL
		RestangularProvider.setBaseUrl('/api/');
	}
	
	RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response) {
		if (operation == 'getList') {
			//response.totalCount = data.total_item_count;
			if (data.results) {
				data = data.results;				
			}
		}
		else if (operation == 'get') {
			if (data.item) {
				data = data.item;
			}
		}
		return data;
	});
}

api.$inject = ['RestangularProvider'];
	
module.exports = api;