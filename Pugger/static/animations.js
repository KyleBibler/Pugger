/**
 * Created by Kyle on 7/11/2014.
 */

function showPanel(parentId, elementId) {
    var element = document.getElementById(elementId)
    var parent = document.getElementById(parentId)
    parent.css({
        height: function (){ return element.height() + 10 } + "px"
        });
    element.css({
       display: 'block'
    });
    element.toggleClass('transparent', 500)
}

function incHeight(elementId, hiddenId) {
    var element = $(elementId);
    var hidden = $(hiddenId);
    element.animate({
        height: "+=" + (element.height() + 10)
    }, 200);
    hidden.toggleClass('hidden');
}

var toggleFilter = function() {
    //e.preventDefault();
    $("#wrapper").toggleClass("toggled");
};

//$(document).ready(function() {
//    $("#filter-toggle").click(function(e) {
//
//    });
//});

