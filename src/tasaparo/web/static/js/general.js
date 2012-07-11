var TtpRouter = Backbone.Router.extend({
    routes: {
        "" : "home",
        "map/" : "map",
        "compare/" : "compare",
        "profile/" : "profile",
    },

    home: function(){
        console.log("home");
    },

    map: function(){
        console.log("map");
    },

    compare: function(){
        console.log("compare");
    },

    profile: function(){
        console.log("profile");
    }
});

$(document).ready(function(){    
    $('.default').dropkick();
    
    var appTtpRouter = new TtpRouter();
    Backbone.history.start({pushState: true});
});


