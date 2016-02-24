function api(RestangularProvider) {
	// Base URL
	RestangularProvider.setBaseUrl('https://141.83.150.131/api/');
	
	RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response) {
		if (operation == "getList") {
			//response.totalCount = data.total_item_count;
			if (data.items) {
				data = data.items;				
			}
		}
		return data;
	});
}

api.$inject = ['RestangularProvider'];
	
module.exports = api;