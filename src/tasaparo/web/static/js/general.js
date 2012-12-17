var app = {};
app.views = {};

$(document).on('ready', function(){
    //info tooltips
    //$(".result").tooltip({
        //'position': 'top center',
        //'margin_bottom': 10,
        //'html': function(self){
            //return "";
         //}
    //});

    $(".result").click({
        //TODO on click cargar este query_hash en la home
    });

    //home calculate ajax get & redirect
    $("#calculate").on('submit', function(e){
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
    });

    //map view
    if($("#map-view").length){
        initmap();
    }

    //compare view
    if($("#compare-view").length){
        var template = _.template($("#compare-item").html());
        var recalculate = function(){
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
                            comp.append(template(data.rates[i]));

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

        recalculate();
        $("#recalculate").on('submit', function(e){
            e.preventDefault();
            recalculate();
        });
    }

    //profile view
    if($("#profile-view").length){
        var conf = {

        };

        var initchart = function(values){
            $("#chart").chart({
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
        }

        var recalculate = function(){
            $.ajax({
                data: $('#recalculate').serialize(),
                url: $('#recalculate').attr('action'),
                dataType:'json',
                success: function(data) {
                    profile_serie = [];
                    profile_labels = [];

                    var rates_long = data.profile_rates.length;
                    for(var i=0; i < rates_long; i++){
                        profile_serie.push(data.profile_rates[i].rate);
                    }

                    //delete
                    data_submit =  {
                        serie1 : profile_serie,
                    };

                    $("#chart").fadeOut(function(){
                        $(this).remove();
                        $("#right").html("<div id='chart'></div>");
                        initchart(data_submit);
                    });

                }
            });
        }

        recalculate();
        $("#recalculate").on('submit', function(e){
            e.preventDefault();
            recalculate();
        });
    }
});


