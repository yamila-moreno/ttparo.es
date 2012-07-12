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

    $(".result").tooltip({ 
        'position': 'top center',
        'margin_bottom': 10,
        'html': function(self){
            return "<p>Rellena el formulario para obtener tu tasa de paro</p><div class='arrow'></div></div>";
         }                    
    });

    $("#calculate").on("submit", function(e){
        e.preventDefault();

        $.ajax({
          data: $(this).serialize(),    
          url: $(this).attr('action'),
          success: function(data) {
            data = {'result': 17, 'level': 'r1', 'leveltxt': 'nivel alto'};

            $("#resulparo").fadeOut(function(){
                var template = _.template($("#result-template").html());
                $("#result").html(template(data));
                $("#resulparo").fadeIn();
            });

          }
        });
    });
});


