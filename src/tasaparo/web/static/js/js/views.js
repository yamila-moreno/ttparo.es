/*var Views = {};
Views.Home = Backbone.View.extend({
    events: {
        "submit #calculate":   "submit"
    },    
    el: '#home-view',
    submit: function(e){
        e.preventDefault();
        var target = $(e.target);
        
        $.ajax({
          data: target.serialize(),
          url: target.attr('action'),
          dataType:'json',
          success: function(data) {
            if(data.success) {
                window.location.href = data.rate_query.absolute_url;
            }
          }
        });
    }
});
*/


