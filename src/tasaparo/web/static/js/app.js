(function() {
    var app = this.app;

    app.initialize = function() {
        if ($("#home-view").length > 0) {
            app.currentView = new Tasaparo.HomeView();
        } else if ($("#compare-view").length > 0) {
            app.currentView = new Tasaparo.CompareView();
        } else if ($("#map-view").length > 0) {
            app.currentView = new Tasaparo.MapView();
        } else if($("#profile-view").length > 0) {
            app.currentView = new Tasaparo.ProfileView();
        } else if($("#widget-view").length > 0) {
            app.currentView = new Tasaparo.WidgetView();
        }
    };
}).call(this);

app.initialize.call(this);
