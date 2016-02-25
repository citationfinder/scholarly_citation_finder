function ListTasks() {
    return {
        restrict: 'E',
        controller: require('../controller/directive/ListTasksController'),
        template: require('../view/directive/list-tasks.html'),
		scope: {
			tasktype: '@',
			taskstatuscallback: '&'
		},
		link: function(scope, element, attrs) {
			scope.taskstatuscallback = scope.taskstatuscallback();
		}
    };
}

module.exports = ListTasks;