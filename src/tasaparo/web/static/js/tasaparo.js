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

        initialize: function() {
            _.bindAll(this);
        },

        submit: function(target, url) {
            url = url || target.attr('action');
            $.get(url, target.serialize(),
                                this.submitSuccess, 'json');
        },

        onMainFormSubmit: function(event) {
            event.preventDefault();
            var target = $(event.currentTarget);
            this.submit(target);
        },

        submitSuccess: function(data) {
            console.log(data);
            if (data.success) {
                window.location.href = data.rate_query.absolute_url;
            }
        }
    });

    Tasaparo.CompateView = Tasaparo.HomeView.extend({
        el: "#compare-view",

        initialize: function() {
            _.bindAll(this);
            this.template = _.template($("#compare-item").html());
        },

        submitSuccess: function(data) {
            if (!data.success) return;

            var compareDom = this.$("#compare").empty();
            var ratesLength = data.rates.length;

            _.each(data.rates, function(item) {
                console.log(item);
            }, this);
        }
    });

    Tasaparo.MapView = Tasaparo.CompateView.extend({
        el: "#map-view",

        events: {
            "submit form#calculate": "onMainFormSubmit"
        },

        initialize: function() {
            _.bindAll(this);

            this.r = Raphael("map", 600, 500);
            this.map = app.drawMap(this.r);

            var form = this.$("form#calculate");
            this.submit(form);
        },

        submit: function(target) {
            $.get(this.$el.data('url'), target.serialize(),
                                this.submitSuccess, 'json');
        },

        onMainFormSubmit: function(event) {
            event.preventDefault();
            var target = $(event.currentTarget);
            this.submit(target);
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
}).call(this);
