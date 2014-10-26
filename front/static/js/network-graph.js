app.directive('networkGraph', function(){
	return {
		templateUrl: 'assets/views/network-graph.html',
		restrict: 'E',
		scope: {

		},
		link: function(scope, element, attrs){},
		controller: ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
			$scope.cycle_order_by = [
				{label: 'Ratio', predicate: 'ratio'},
				{label: 'Path length', predicate: 'path.length'},
				{label: 'Volume', predicate: 'volume'},
				{label: 'BTC Amount Win', predicate: 'btc_amount'}
			];
			$scope.order = {
				value: $scope.cycle_order_by[0],
				reverse: true
			};
			$scope.update_book_orders = function(graph_dict){
				$http.get('/api/OrderBook/all').success(function(data){
					_.forEach($scope.edges, function(edge){
						edge.orders = [];
					});
					_.forEach(data, function(order){
						var currency1 = (!order.fields.is_bid)?order.fields.currency1:order.fields.currency2;
						var currency2 = (!order.fields.is_bid)?order.fields.currency2:order.fields.currency1;
						var node = graph_dict[currency1];
						var edge = node.edges[currency2];
						edge.orders.push({
							price: order.fields.price,
							amount: order.fields.amount
						});
					});
					$scope.update_cycle_data($scope.found_cycles, $scope.graph_dict);
					console.log($scope.found_cycles);
					console.log($scope.edges);
				});
			}
			$scope.update_cycle_data = function(cycles, graph_dict){
				for(var cycle_id in cycles){
					var cycle = cycles[cycle_id];
					cycle.ratio = 1;
					cycle.amounts = 1000000;
					var bootle_necks = [];
					for(var i = 0; i < cycle.path.length; i++)
						bootle_necks[i] = 0;
					for(var i = 0; i < cycle.path.length - 1; i++){
						var node = graph_dict[cycle.path[i]];
						var edge = node.edges[cycle.path[i+1]];
						cycle.ratio *= edge.ratio;
						cycle.ratio *= 0.998;
						if(cycle.amount*edge.orders[0].price < edge.orders[0].amount){
							cycle.amount = cycle.amount*edge.orders[0].price;
						}else{
							cycle.amount = edge.orders[0].amount;
							bootle_necks[i]++;
						}
					}
					console.log(bootle_necks);
					cycle.btc_amount = (cycle.path[0] == 'BTC')?cycle.amount:(cycle.amount * graph_dict[cycle.path[0]].edges['BTC'].ratio);
				}//1000 USD, 1.5 USD/GHS -> 
			}
			$scope.find_cycle = function(node, mark, path, start_id){
				node.mark = mark;
				_.forEach(node.edges, function(edge){
					var target_node = $scope.graph_dict[edge.target];
					if(target_node.mark == mark){ //been there
						if(target_node.id == start_id){
							var cycle_path = path + "-" + target_node.id;
							$scope.found_cycles.push({path: cycle_path.split('-'), ratio: 1});
						}
					}
					else
						$scope.find_cycle(target_node, mark, path + "-" + target_node.id, start_id)
				})
			}
			$scope.find_all_cycles = function(graph_dict){
				$scope.found_cycles = [];
				var mark = 0;
				for(var node_id in graph_dict)
					$scope.find_cycle(graph_dict[node_id], mark++, node_id, node_id);
				$scope.found_cycles = _.filter($scope.found_cycles, function(cycle){ return cycle.path.length > 3;});
			}

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
			$scope.graph_dict = {};
			_.forEach($scope.nodes, function(node){
				$scope.graph_dict[node.id] = node;
				node.edges = {};
			});
			$http.get('/api/Tick/').success(function(data){
				$scope.tickers = data;
				for(var i = 0; i < $scope.tickers.length; i++){
					var tick = $scope.tickers[i];
					$scope.edges.push({
						"id": tick.fields.currency1 + "-" + tick.fields.currency2,
						"source": tick.fields.currency1,
						"target": tick.fields.currency2,
						"ratio": 1/Number(tick.fields.ask)
					});
					$scope.edges.push({
						"id": tick.fields.currency2 + "-" + tick.fields.currency1,
						"source": tick.fields.currency2,
						"target": tick.fields.currency1,
						"ratio": Number(tick.fields.ask)
					});
				}
				_.forEach($scope.edges, function(edge){
					var currency1 = $scope.graph_dict[edge.source];
					currency1.edges[edge.target] = edge;
				});
				$scope.find_all_cycles($scope.graph_dict);
				$scope.update_book_orders($scope.graph_dict);
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
