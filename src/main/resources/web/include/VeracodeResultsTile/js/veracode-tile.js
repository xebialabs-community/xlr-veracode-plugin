/*
 * Copyright 2018 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/* insert your javascript code here.  see xlr-sonar-plugin for an example */

'use strict';
(function() {
  var VeracodeResultsTileViewController = function($scope, VeracodeResultsService, XlrTileHelper) {
    var vm = this;
    vm.tileConfigurationIsPopulated = tileConfigurationIsPopulated;
    var tile;
/*  if ($scope.xlrDashboard) {
      // summary page
      vm.release = $scope.xlrDashboard.release;
      vm.tile = $scope.xlrTile.tile;
      if (vm.tile.properties == null) {
        vm.config = vm.tile.configurationProperties;
      } else {
        // new style since 7.0
        vm.config = vm.tile.properties;
      }
    } else {
      // detail page
      vm.release = $scope.xlrTileDetailsCtrl.release;
      vm.tile = $scope.xlrTileDetailsCtrl.tile;
    }
*/

    vm.release = $scope.xlrDashboard.release;
    vm.tile = $scope.xlrTile.tile;
    if (vm.tile.properties == null) {
      vm.config = vm.tile.configurationProperties;
    } else {
      // new style since 7.0
      vm.config = vm.tile.properties;
    }

    function tileConfigurationIsPopulated() {
        const config = this.tile.properties;
        return true;
    }

    function refresh() {
      load({params: {refresh: true}});
    }

    function load(config) {
      if (vm.tileConfigurationIsPopulated()) {
        vm.loading = true;
        VeracodeResultsService.executeQuery(vm.tile.id, config).then(
          function(response) {
             mapResponseToUi(response);
        }).finally(
          function() {
            vm.loading = false;
          });
      }
    }

    function mapResponseToUi(response) {

        /*
        var staticAnalysis = response.data.data;
        $scope.outputValue1 = staticAnalysis['submitted_date'];
        $scope.outputValue2 = staticAnalysis['published_date'];
        $scope.outputValue3 = staticAnalysis['next_scan_due'];
        */
        vm.staticAnalysis = response.data.data
    }

    vm.tileConfigurationIsPopulated = tileConfigurationIsPopulated;
    vm.refresh = refresh;

  };

  var VeracodeResultsService = function(Backend) {
     function executeQuery(tileId, config) {
       return Backend.get("tiles/" + tileId + "/data", config);
     }
     return   {
       executeQuery : executeQuery
     };
  }

  VeracodeResultsService.$inject = ['Backend'];
  VeracodeResultsTileViewController.$inject = ['$scope', 'xlrelease.veracode.VeracodeResultsService', 'XlrTileHelper'];
  angular.module('xlrelease.veracode.tile', []);
  angular.module('xlrelease.veracode.tile').service('xlrelease.veracode.VeracodeResultsService', VeracodeResultsService);
  angular.module('xlrelease.veracode.tile').controller('veracode.VeracodeResultsTileViewController', VeracodeResultsTileViewController);
})();
