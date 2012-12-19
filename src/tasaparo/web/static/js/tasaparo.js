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

        onMainFormSubmit: function(event) {
            event.preventDefault();
            var target = $(event.currentTarget);

            $.post(target.attr('action'), target.serialize(),
                                this.onSubmitSuccess, 'json');
        },

        onSubmitSuccess: function(data) {
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

        onMainFormSubmit: function(event) {
            event.preventDefault();
            var target = $(event.currentTarget);
            this.submit(target);
        },

        submit: function(target) {
            $.get(target.attr('action'), target.serialize(),
                                this.submitSuccess, 'json');
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

        initialize: function() {
            _.bindAll(this);

            this.form = this.$("form#calculate");
            this.submit(form);
            this.r = Raphael("map", 600, 500);
            this.map = app.drawMap(this.r);
        },

        submitSuccess: function(data) {
            if (!data.success) return;
        }
    });
}).call(this);
