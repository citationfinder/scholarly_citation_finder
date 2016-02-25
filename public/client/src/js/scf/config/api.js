function api(RestangularProvider) {
	// Base URL
	RestangularProvider.setBaseUrl('/api/');
	
	RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response) {
		if (operation == "getList") {
			//response.totalCount = data.total_item_count;
			if (data.results) {
				data = data.results;				
			}
		}
		return data;
	});
}

api.$inject = ['RestangularProvider'];
	
module.exports = api;