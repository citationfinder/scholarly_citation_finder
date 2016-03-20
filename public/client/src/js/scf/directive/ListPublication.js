function ListPublication() {
    return {
        restrict: 'E',
        template: require('../view/directive/list-publication.html'),
		scope: {
			item: '='
		}
    };
}

module.exports = ListPublication;