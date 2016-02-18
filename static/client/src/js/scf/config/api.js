function api(RestangularProvider) {
	// Base URL
	RestangularProvider.setBaseUrl('/api/');
	
	RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response) {
		if (operation == "getList") {
			//response.totalCount = data.total_item_count;
			data = data.items;
		}
		return data;
	});
}

api.$inject = ['RestangularProvider'];
	
module.exports = api;