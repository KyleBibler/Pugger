
var app = angular.module('pugger', []);

app.directive('loginModal', function($scope) {
   return {
       restrict: 'E',
       templateUrl: '../static/templates/registerPanel.html',
       controller: function() {
           this.register = $scope.register;

           this.setRegister = function(regSet) {
               this.register = regSet;
           };

           this.checkRegister = function (regCheck) {
               return this.register == regCheck;
           };
       },
       controllerAs: 'loginCtrl'
   }
});

app.directive('navBar', function () {
    return {
        restrict: 'E',
        templateUrl: '../static/templates/navbar.html',
        controller: function () {
            this.nav = 1;

            this.setNav = function (navSet) {
                this.nav = navSet;
            };

            this.checkNav = function (navCheck) {
                return this.nav === navCheck;
            };

            this.setPanel = function(panelName) {
                this.register = panelName;
            }

        },
        controllerAs: 'navCtrl'
    };
});



app.controller('EventFilter', function($scope) {
    $scope.sportsFiltered = []
    $scope.timeRange = [0, 24]
    $scope.dateRange = [0, -1]
    $scope.sportList = ['Baseball', 'Basketball', 'Soccer', 'Football', 'Disc golf', 'Ultimate frisbee', 'Golf', 'Other']


    $scope.isSportFiltered = function(sport) {
       return ($scope.sportsFiltered.indexOf(sport) != -1);
    }

    $scope.addSportFilter = function(sport) {
      $scope.sportsFiltered.push(sport);
    };

    $scope.removeSportFilter = function(sport) {
      var index = $scope.sportsFiltered.indexOf(sport);
      if(index != -1) {
          $scope.sportsFiltered.splice(index, 1);
      }
    };

    $scope.showOnly = function(sport) {
        $scope.sportsFiltered = $scope.sportList.slice(0);
        $scope.removeSportFilter(sport);
    };

    $scope.removeAllFilters = function() {
      $scope.sportsFiltered = [];
    };

    $scope.toggleFilter = function (sport) {
          if (!$scope.isSportFiltered(sport)) {
              if($scope.sportsFiltered.length == 0) {
                  $scope.showOnly(sport);
              } else if ($scope.sportsFiltered.length+1 != $scope.sportList.length) {
                  $scope.addSportFilter(sport);
              }
          } else {
              $scope.removeSportFilter(sport);
          }
    };
});

app.directive('filterPanel', function() {
    return {
        restrict: 'E',
        templateUrl: '../static/templates/filterBar.html'
    }
});

app.controller('EventController', ['$http', '$scope', function ($http, $scope) {
    $scope.events = [];

    $scope.register = 'login';
    $http.get('/events/event-list.json').success(function(data){
        $scope.events = data.events;
    });


}]);

app.directive('eventPanel', function () {
    return {
        restrict: 'E',
        templateUrl: '../static/templates/eventPanel.html',
        controller: function () {
            this.tab = 1;
            this.shown = true;

            this.isShown = function () {
                return this.shown;
            };

            this.formatName = function(name) {
                if(name.length > 25) {
                    return name.substring(0, 20) + "...";
                }
                else
                    return name;
            }

            this.setTab = function (setTab) {
                this.tab = setTab;
            };

            this.setShown = function (setHide) {
                this.shown = setHide;
            };

            this.isSelected = function (checkTab) {
                return this.tab === checkTab
            };

            this.formatTime = function (time) {
                var times = time.split(":"),
                    meridiem = "A.M.";
                times[0] = parseInt(times[0]);

                if (times[0] >= 12) {
                    meridiem = "P.M.";
                    if (times[0] > 12)
                        times[0] = times[0] - 12;
                } else if (times[0] == 0) {
                    times[0] = 12;
                }
                return times[0] + ":" + times[1] + " " + meridiem;
            }
        },
        controllerAs: 'panel'
    }
});

app.directive('eventDescription', function() {
    return {
        restrict: 'E',
        templateUrl: '../static/templates/eventDescription.html'
    }
});


