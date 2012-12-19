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
            "submit form#calculate": "onMainFormSubmit"
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
            console.log(data);
            if (data.success) {
                window.location.href = data.rate_query.absolute_url;
            }
        },

        onMainFormSubmit: function(event) {
            event.preventDefault();
            var target = $(event.currentTarget);
            this.submit(target);
        }
    });

    Tasaparo.CompateView = Tasaparo.HomeView.extend({
        el: "#compare-view",

        setup: function() {
            this.template = _.template($("#compare-item").html());

            var form = this.$("form#calculate");
            this.submit(form);
        },

        submitSuccess: function(data) {
            if (!data.success) return;

            var compareDom = this.$("#compare").empty();
            var timeout = 0;
            var template = this.template

            _.each(data.rates, function(item) {
                _.delay(function() {
                    var dom = $(template(item));
                    compareDom.append(dom)
                    dom.fadeIn();
                }, timeout)
                timeout += 500;
            }, this);
        }
    });

    Tasaparo.MapView = Tasaparo.CompateView.extend({
        el: "#map-view",

        setup: function() {
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
