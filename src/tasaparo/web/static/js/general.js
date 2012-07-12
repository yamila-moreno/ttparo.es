var aux = {};
var form = {};

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
        if(aux.result === undefined){
            this.navigate("", true);
            return true;
        }
        var mapview = new MapView();
        mapview.render();
    },

    compare: function(){
        console.log("compare");
    },

    profile: function(){
        if(aux.result === undefined){
            this.navigate("", true);
            return true;
        }
        var profileview = new ProfileView();
        profileview.render();
    }
});

var TabsView = Backbone.View.extend({
    template: _.template($("#tabs").html()),
    option: 1,
    initialize: function (option) {
        this.option = option;
    },
    render: function() {
        $("#inner-content").html(this.template(aux));
        $("#tabmenu .t"+this.option).addClass('sel');
        return this;
    }
});

var RecalculateView = Backbone.View.extend({
    template: _.template($("#recalculate").html()),
    render: function() {
        console.log(form);
        $("#left").append(this.template());
        //$('.default').dropkick();
        return this;
    }
});

var InfoResult = Backbone.View.extend({
    template: _.template($("#info-result").html()),
    render: function() {
        $("#inner-content").append(this.template());
        return this;
    }
});

var MapView = Backbone.View.extend({
    template: _.template($("#map-result").html()),
    render: function() {
        var tabs = new TabsView(2);
        tabs.render();

        $("#inner-content").append("<div id='map-view'></div>");
        $("#map-view").html(this.template());

        var recalcualteview = new RecalculateView();
        recalcualteview.render();

        var inforesult = new InfoResult();
        inforesult.render();

        initmap();
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
        var tabs = new TabsView(4);
        tabs.render();

        $("#inner-content").append("<div id='profile-view'></div>");
        $("#profile-view").html(this.template());
        var self = this;

        var recalcualteview = new RecalculateView();
        recalcualteview.render();

        $.ajax({
          data: $("#calculate").serialize(),
          url: '',
          success: function(data) {
            //borrar
            data = self.values;

            self.values = data;
            self.initchart();
         }
        });

        $("#calculate").bind("submit", $.proxy( this.submit, this ));

        var inforesult = new InfoResult();
        inforesult.render();

        return this;
    },
    submit: function(e){
        e.preventDefault();
        var self = this;

        recalculate('');

        $.ajax({
          data: $(this).serialize(),
          url: '',
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
    template3: _.template($("#search-template").html()),
    el: '#home-view',
    render: function() {
        $(this.el).html(this.template3());
        if(aux.result === undefined){
            $(this.el).append(this.template1());
        }else{
            $(this.el).append(this.template2(aux));
            $("#resulparo").fadeIn();
        }

        //$('.default').dropkick();
        $("#calculate").bind("submit", $.proxy( this.submit, this ));

        return this;
    },
    submit: function(e){
        e.preventDefault();
        form = $("#calculate").serializeObject();
        var self = this;

        $.ajax({
          data: $('#calculate').serialize(),
          url: $('#calculate').attr('action'),
          dataType:'json',
          success: function(data) {
              if(data.success) {
                data = {'result': data.rate_query.rate, 'level': data.rate_query.level, 'leveltxt': data.rate_query.levelText};
            aux = data;

                $("#resulparo").fadeOut(function(){
                    $("#result").html(self.template2(data));
                    $("#resulparo").fadeIn();
                });
            }
          }
        });
    }
});

function recalculate(url){
    form = $("#calculate").serializeObject();

    $.ajax({
      data: $("#calculate").serialize(),
      url: url,
      success: function(data) {
        //borrar
        data = {'result': 25, 'level': '3', 'leveltxt': 'nivel alto'};
        aux = data;

        var tabmenu = $("#tabmenu");
        var link = tabmenu.find('.t1 a');
        link.attr('class', 'link c'+data.level);
        tabmenu.find('span').html(data.result+"%");
      }
    });
}

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$(document).ready(function(){
    var appTtpRouter = new TtpRouter();
    Backbone.history.start({pushState: true});

    $("body").on("click", ".link", function(e){
        e.preventDefault();
        appTtpRouter.navigate($(this).attr('href'), true);
    })
});


