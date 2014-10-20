app.controller('networkGraphController', ['$scope', '$http', function ($scope, $http) {
	$http.get('/api/Tick/').success(function(data){
		$scope.tickers = data;
	});
}]);