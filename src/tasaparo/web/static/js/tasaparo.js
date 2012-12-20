$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

(function() {
    var Tasaparo = this.Tasaparo = {};
    var app = this.app = {};

    Tasaparo.HomeView = Backbone.View.extend({
        el: "#home-view",

        events: {
            "submit form#calculate": "onMainFormSubmit",
            "click .lresults": "showResult"
        },

        setup: function() {},

        initialize: function() {
            _.bindAll(this);
            this.setup();
        },

        submit: function(target) {
            $.get(target.attr('action'), target.serialize(),
                                this.submitSuccess, 'json');
        },

        submitSuccess: function(data) {
            if (data.success) {
                window.location.href = data.rate_query.absolute_url;
            }
        },

        onMainFormSubmit: function(event) {
            event.preventDefault();
            var target = $(event.currentTarget);
            this.submit(target);
        },

        showResult: function(event){
            var target = $(event.currentTarget);
            window.location.href = target.attr('rel');
        }

    });

    Tasaparo.CompareView = Tasaparo.HomeView.extend({
        el: "#compare-view",

        events: {
            "click #by-sex": "compareBySex",
            "click #by-age": "compareByAge",
            "click #by-education": "compareByEducation",
        },

        setup: function() {
            this.submit(this.$("#by-sex"));
        },

        compareBySex: function(event){

            this.$("#by-sex").addClass('sel');
            this.$("#by-age").removeClass('sel');
            this.$("#by-education").removeClass('sel');

            // recolocar los combos
            var target = $(event.currentTarget);
            this.submit(target);
        },

        compareByAge: function(event){

            this.$("#by-sex").removeClass('sel');
            this.$("#by-age").addClass('sel');
            this.$("#by-education").removeClass('sel');

            // recolocar los combos
            var target = $(event.currentTarget);
            this.submit(target);
        },

        compareByEducation: function(event){

            this.$("#by-sex").removeClass('sel');
            this.$("#by-age").removeClass('sel');
            this.$("#by-education").addClass('sel');

            // recolocar los combos
            var target = $(event.currentTarget);
            this.submit(target);
        },

        submit: function(target) {
            this.template = _.template($("#compare-item").html());
            var form = this.$("form#calculate");

            $.get(this.$el.data('url'), target.serialize(),
                                this.submitSuccess, 'json');
        },

        submitSuccess: function(data) {
            if (!data.success) return;

            var compareDom = this.$("#compare").empty();
            var timeout = 0;
            var template = this.template;

            _.each(data.rates, function(item) {
                _.delay(function() {
                    var dom = $(template(item));
                    compareDom.append(dom)
                    dom.fadeIn();
                }, timeout)
                timeout += 500;
            }, this);
        },


    });

    Tasaparo.MapView = Tasaparo.CompareView.extend({
        el: "#map-view",

        setup: function() {

            $("#id_province").attr('disabled','disabled');
            $("#id_sex").removeAttr('disabled');
            $("#id_age").removeAttr('disabled');
            $("#id_education").removeAttr('disabled');

            this.r = Raphael("map", 600, 500);
            this.map = app.drawMap(this.r);

            var form = this.$("form#calculate");
            this.submit(form);
        },

        onMainFormSubmit: function(event) {
            event.preventDefault();
            var target = $(event.currentTarget);
            this.submit(target);
        },

        submit: function(target) {
            $.get(this.$el.data('url'), target.serialize(),
                                this.submitSuccess, 'json');
        },

        submitSuccess: function(data) {
            if (!data.success) return;

            _.each(data.rates, function(rate) {
                var attrs = app.levelAttrs[rate.level];
                var provinceData = this.map[rate.province_id];
                _.each(provinceData, function(item) {
                    item.attr(attrs);
                }, this);
            }, this);
        }
    });

    Tasaparo.WidgetView = Tasaparo.HomeView.extend({
        el: "#widget-view",

        setup: function() {
            this.$("#calculate input").attr('value','Widget!');
        },

        submit: function(target) {
            $.get(this.$el.data('url'), target.serialize(),
                                this.submitSuccess, 'json');
        },

        submitSuccess: function(data) {
            if (!data.success) return;
            this.$("#widget-wrapper").show();
            this.$("#widget-html").text(data.widget_html).select();
        }

    });

    Tasaparo.ProfileView = Tasaparo.HomeView.extend({
        el: "#profile-view",

        setupChart: function(values) {
            this.$("#chart").chart({
                type : "line",
                labels : ["2005", "", "", "", "2006", "", "", "", "2007", "", "", "", "2008", "", "", "", "2009", "", "", "", "2010", "", "", "", "2011", "", "", "", "2012"],
                values: values,
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

        setup: function() {
            var form = this.$("form#calculate");
            this.submit(form);
        },

        submitSuccess: function(data) {
            if (!data.success) return;

            var data_submit = {serie1:  _.map(data.profile_rates, function(item) {
                return item.rate
            })};

            var self = this;

            this.$("#chart").fadeOut(function() {
                $(this).remove();
                self.$("#right").html("<div id='chart'></div>");
                self.setupChart(data_submit);
            });
        }
    });
}).call(this);
