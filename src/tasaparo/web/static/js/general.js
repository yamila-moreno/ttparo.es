var TtpRouter = Backbone.Router.extend({
    routes: {
        "" : "home",
        "map/" : "map",
        "compare/" : "compare",
        "profile/" : "profile",
    },

    home: function(){            
        $("#inner-content").html("<div id='home-view'></div>");
        var homeview = new HomeView();
        homeview.render();

        var inforesult = new InfoResult();
        inforesult.render();

        var lastprofiles = new LastProfiles();
        lastprofiles.render();
    },

    map: function(){
        console.log("map");
    },

    compare: function(){
        console.log("compare");
    },

    profile: function(){
        var profileview = new ProfileView();
        profileview.render();
    }
});

var RecalculateView = Backbone.View.extend({
    template: _.template($("#recalculate").html()),
    render: function() {
        $("#left").append(this.template());
        return this;
    }
});

var InfoResult = Backbone.View.extend({
    template: _.template($("#info-result").html()),
    render: function() {
        $("#inner-content").append(this.template());
        $('.default').dropkick();

        return this;
    }
});

var ProfileView = Backbone.View.extend({
    template: _.template($("#result-profile").html()),
    el: '#profile-view',
    values: {
      serie1 : [19, 35, 9, 18, 19, 35, 9, 18],
      serie2 : [17, 57, 4, 85, 17, 57, 4, 85],
      serie3 : [27, 67, 7, 35, 27, 67, 7, 35],
    },
    initchart: function(){
        $("#chart").chart({
         type : "line",
         labels : ["2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012"],
         values : this.values,
         margins : [10, 15, 20, 50],
        series: {
              serie1 : {
               color : "red"
              },
              serie2 : {
               color : "blue"
              }
        },
         defaultAxis : {
          labels : true
         },
         features : {
          grid : {
           draw : true,
           forceBorder : true
          }
         }
        });
    },
    render: function() {
        $("#inner-content").html("<div id='profile-view'></div>");
        $("#profile-view").html(this.template());

        this.initchart();

        var recalcualteview = new RecalculateView();
        recalcualteview.render();

        $("#calculate").bind("submit", $.proxy( this.submit, this ));

        var inforesult = new InfoResult();
        inforesult.render();

        return this;
    },
    submit: function(e){
        e.preventDefault();
        var self = this;

        $.ajax({
          data: $(this).serialize(),    
          url: $(this).attr('action'),
          success: function(data) {
            //delete
             data =  {
              serie1 : [19, 35, 29, 18, 19, 35, 9, 18],
              serie2 : [37, 57, 4, 15, 17, 17, 34, 85],
              serie3 : [7, 67, 7, 35, 57, 67, 7, 35],
            };

            self.values = data;

            $("#chart").fadeOut(function(){
                $(this).remove();
                $("#right").html("<div id='chart'></div>");
                self.initchart();
            });

          }
        });
    }
});

var LastProfiles = Backbone.View.extend({
    template: _.template($("#last-profiles").html()),
    template_item: _.template($("#last-profiles-item").html()),

    render: function() {
        $("#inner-content").append(this.template());
        var self = this;

        $.ajax({
          url: '',
          success: function(data) {
            data = {'items': [
                {'time': '10 minutos',
                'level': '1',
                'percent': 10,
                'sex': 'Mujer',
                'years': '43',
                'province': 'Santa Cruz de Tenerife',
                'studies': 'Estudios Universitarios Superiores'
                },
                {'time': '20 minutos',
                'level': '2',
                'percent': 20,
                'sex': 'Mujer',
                'years': '43',
                'province': 'Madrid',
                'studies': 'Estudios Universitarios Superiores'
                },
                {'time': '30 minutos',
                'level': '3',
                'percent': 34,
                'sex': 'Hombre',
                'years': '43',
                'province': 'Barcelona',
                'studies': 'FP2'
                },
                {'time': '50 minutos',
                'level': '1',
                'percent': 53,
                'sex': 'Mujer',
                'years': '43',
                'province': 'Málaga',
                'studies': 'Estudios Universitarios Superiores'
                }
            ]};

            var last = $("#last");

            for(var i=0; i < 4; i++){
                last.append(self.template_item(data.items[i]));
            }

            $(".result").tooltip({ 
                'position': 'top center',
                'margin_bottom': 10,
                'html': function(self){
                    return "<p>Rellena el formulario para obtener tu tasa de paro</p><div class='arrow'></div></div>";
                 }                    
            });

          }
        });

        return this;
    }
});

var HomeView = Backbone.View.extend({
    template1: _.template($("#result-empty-template").html()),      
    template2: _.template($("#result-template").html()), 
    data: false,    
    el: '#home-view',
    render: function() {
        $(this.el).html(this.template1());

        $('.default').dropkick();
        $("#calculate").bind("submit", this.submit);

        return this;
    },
    submit: function(e){
        e.preventDefault();

        $.ajax({
          data: $(this).serialize(),    
          url: $(this).attr('action'),
          success: function(data) {
            data = {'result': 17, 'level': 'r2', 'leveltxt': 'nivel alto'};

            $("#resulparo").fadeOut(function(){
                var template = _.template($("#result-template").html());
                $("#result").html(template(data));
                $("#resulparo").fadeIn();
            });

          }
        });
    }
});

$(document).ready(function(){    
    var appTtpRouter = new TtpRouter();
    Backbone.history.start({pushState: true});

    $("body").on("click", "a", function(e){
        e.preventDefault();
        appTtpRouter.navigate($(this).attr('href'), true);
    })
});


