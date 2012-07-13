var aux = {};
var form = {};

var TtpRouter = Backbone.Router.extend({
    routes: {
        "" : "home",
        "map/" : "map",
        "compare/" : "compare",
        "profile/" : "profile",
        "*actions": "home_with_hash"
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

    home_with_hash: function(){
        $("#inner-content").html("<div id='home-view'></div>");
        var homeview = new HomeWithHashView();
        homeview.render();

        var inforesult = new InfoResult();
        inforesult.render();

        var lastprofiles = new LastProfiles();
        lastprofiles.render();
    },

    map: function(){
        if(aux.rate === undefined){
            this.navigate("", true);
            return true;
        }
        var mapview = new MapView();
        mapview.render();
    },

    compare: function(){
        if(aux.rate === undefined){
            this.navigate("", true);
            return true;
        }

        var compareview = new CompareView();
        compareview.render();
    },

    profile: function(){
        if(aux.rate === undefined){
            this.navigate("", true);
            return true;
        }
        var profileview = new ProfileView();
        profileview.render();
    }
});

var CompareView = Backbone.View.extend({
    template: _.template($("#compare-result").html()),
    render: function() {
        var tabs = new TabsView(3);
        tabs.render();

        $("#inner-content").append("<div id='compare-view'></div>");
        $("#compare-view").html(this.template());

        var recalcualteview = new RecalculateView();
        recalcualteview.render();

        var inforesult = new InfoResult();
        inforesult.render();

        initmap();
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
    template_item: _.template($("#compare-item").html()),

    render: function() {
        $("#left").append(this.template());
        $("#recalculate").bind("submit", $.proxy( this.submit, this ));
        return this;
    },
    submit: function(e){
        e.preventDefault();
        form = $("#recalculate").serializeObject();
        var self = this;

        $.ajax({
            data: $('#recalculate').serialize(),
            url: $('#recalculate').attr('action'),
            dataType:'json',
            success: function(data) {
                if(data.success) {
                    var comp = $("#compare");

                    $("#compare").html('');

                    var rates_long = data.rates.length;
                    for(var i=0; i < rates_long; i++){

                        var mydict;
                        mydict =
                            {'percent': data.rates[i].rate,
                            'sex': data.rates[i].sex,
                            'level': data.rates[i].level,
                        }

                        comp.append(self.template_item(mydict));

                        setTimeout(function(){
                            var bls = $("#compare-view").find('.bl');

                            for(var z=0; z<bls.length; z++){
                                (function (bl, time) {
                                    setTimeout(function(){
                                        $(bl).fadeIn();
                                    },time);
                                })(bls[z], z*500);
                            }
                        },200);
                    }
                }
            }
        });
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
          url: $('#last').attr('latest_queries'),
          dataType:'json',
          success: function(data) {
            var last = $("#last");
            for(var i=0; i < 4; i++){
                var mydict;
                mydict =
                    {'time': data.latest_queries[i].cycle,
                    'level': data.latest_queries[i].level,
                    'percent': data.latest_queries[i].rate,
                    'sex': data.latest_queries[i].sex,
                    'years': data.latest_queries[i].age,
                    'province': data.latest_queries[i].province,
                    'studies': data.latest_queries[i].education,
                }

                last.append(self.template_item(mydict));
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
        if(aux.rate === undefined){
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
                data = data.rate_query;
                aux = data;
                $("#resulparo").fadeOut(function(){
                    appTtpRouter.navigate(data.absolute_url, false);
                    data.url = window.location.href;
                    $("#result").html(self.template2(data));
                    $("#resulparo").fadeIn();
                });
            }
          }
        });
    }
});

var HomeWithHashView = HomeView.extend({
    render: function(){
        var self = this;
        $(this.el).html(this.template3());
        $(this.el).append(this.template1());
        $("#calculate").bind("submit", $.proxy( this.submit, this ));
        $.ajax({
          data: $('#calculate').serialize(),
          url: $('#calculate').attr('action'),
          dataType:'json',
          success: function(data) {
              if(data.success) {
                data = data.rate_query;
                aux = data;
                $("#resulparo").fadeOut(function(){
                    data.url = window.location.href;
                    $("#result").html(self.template2(data));
                    $("#resulparo").fadeIn();
                });
            }
          }
        });
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
                data = data.rate_query;
                aux = data;
                $("#resulparo").fadeOut(function(){
                    $("#compartir a").attr('data-url', data.absolute_url);
                    $("#compartir a").attr('data-text', 'Mi tasa de paro es ' & data.absolute_url & '%');
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
var appTtpRouter = 0;
var iframe = '<iframe allowtransparency="true" frameborder="0" scrolling="no" data-url="<%- url %>" src="https://platform.twitter.com/widgets/tweet_button.html" style="width:130px; height:20px;"></iframe>';
$(document).ready(function(){
    appTtpRouter = new TtpRouter();
    Backbone.history.start({pushState: true});

    $("body").on("click", ".link", function(e){
        e.preventDefault();
        appTtpRouter.navigate($(this).attr('href'), true);
    })
});


