app.directive('networkGraph', function(){
	return {
		templateUrl: 'assets/views/network-graph.html',
		restrict: 'E',
		scope: {

		},
		link: function(scope, element, attrs){},
		controller: ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
			$scope.middle_currencies = ['DGB', 'USDE', 'WDC', 'MEC', 'GHS', 'IXC', 'POT', 'DOGE', 'FTC', 'DRK', 'AUR', 'NMC', 'MYR', 'ANC'];
			$scope.market = ['EUR', 'USD', 'LTC', 'BTC'];
			$scope.fixed_position = {}
			$scope.nodes = [];
			$scope.edges = [];
			for(var i = 0; i < $scope.middle_currencies.length; i++){
				var currency = $scope.middle_currencies[i];
				$scope.nodes.push({"id": currency, "label": currency, "x": i, "y": 2, "size": 2});
			}
			$scope.nodes.push({"id": "EUR", "label": "EUR", "x": 4, "y": 1, "size": 3});
			$scope.nodes.push({"id": "USD", "label": "USD", "x": 7, "y": 1, "size": 3});
			$scope.nodes.push({"id": "LTC", "label": "LTC", "x": 4, "y": 3, "size": 3});
			$scope.nodes.push({"id": "BTC", "label": "BTC", "x": 7, "y": 3, "size": 3});
			$http.get('/api/Tick/').success(function(data){
				$scope.tickers = data;
				for(var i = 0; i < $scope.tickers.length; i++){
					var tick = $scope.tickers[i];
					$scope.edges.push({
						"id": tick.fields.currency1 + "-" + tick.fields.currency2,
						"source": tick.fields.currency1,
						"target": tick.fields.currency2
					});
				}
				$scope.graph_data = {
					"nodes": $scope.nodes,
					"edges": $scope.edges
				};
				$scope.graph = new sigma({
					graph: $scope.graph_data,
					container: 'container',
					settings: {
						defaultNodeColor: '#ec5148',
						labelThreshold: 0
					}
				});
			});				
		}]
	}
});
