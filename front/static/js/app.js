var app = angular.module('app', [], function () {});
function propertyFilter(){
    function parseString(input){
        return input.split(".");
    }
 
    function getValue(element, propertyArray){
        var value = element;
        for(var i = 0;i<propertyArray.length;i++)
        	value = value[propertyArray[i]]; 
        return value;
    }
 
    return function (array, propertyString, target){
    	if(!array)
    		return [];
        var properties = parseString(propertyString);
        var finalArray = [];
        for(var i = 0;i<array.length;i++){
        	if(getValue(array[i], properties) == target)
        		finalArray.push(array[i]);
        }
        return finalArray;
    }
}
app.filter('property', propertyFilter);