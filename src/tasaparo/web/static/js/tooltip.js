(function($){  
 $.fn.tooltip = function(params) {  
    var defaults = {
        'appendTo': 'body',
        'className': 'tooltip',
        'relative': false,
        'width': 200,
        'html':  function(elm){
            return "<div><p>"+$(elm).attr('title')+"</p></div>";
        },
        'position': 'bottom center',
        'margin_top': 0,
        'margin_bottom': 0,
        'margin_left': 0,
        'onBeforeHide': function(){},
        'onBeforeShow': function(){},
        'onCreate': function(){},
        'onHide': function(){},
        'onShow': function(){},
        'open_event': 'mouseover',
        'close_event': 'mouseout',
        'open_effect': false,
        'close_effect': false,
        'duration_effect': 'slow',
        'css':{
            'position': 'absolute',
            'width': 200 
        },
        'max_left': 'none',
        'max_top': 'none',
        'min_left': 'none',
        'min_top': 'none'    
    };
        
    var options = $.extend(defaults, params);
    
    return this.each(function(){
        var self = this;
                
        if(options.open_event){
            $(self)[options.open_event](function(){
                self.open();
            });
        }
        
        if(options.close_event){
            $(self)[options.close_event](function(){
                self.close();
            });
        }
        
        self.close = function(){
            options.onBeforeHide();
            if(options.close_effect){
                $(self.tooltip)[options.close_effect](options.duration_effect, function(){
                    options.onHide();        
                 });
            }else{
                $(self.tooltip).hide();
                options.onHide();  
            }
        };
        
        self.open = function(){
            options.onBeforeShow();
            if(self.tooltip==undefined){
                self.tooltip = $(document.createElement('div'))
                .attr('class', options.className);
                $(self.tooltip).html(options.html(self));
                $(self.tooltip).appendTo(options.appendTo);
                $(self.tooltip).css(options.css);
                $(self.tooltip).css(self.getPosition());
                options.onCreate(self);
            }
            
            if(options.open_effect){
                $(self.tooltip)[options.open_effect](options.duration_effect, function(){
                    options.onShow();
                 });
            }else{
                $(self.tooltip).show();
                options.onShow();
            }      
        };

        self.getPosition = function(){
            var css = {};
            var position = options.position.split(' ');
            
            if(position[0]=='top'){
                css.top = $(self).offset().top-$(self.tooltip).outerHeight();
            }else{
                 if(position[0]=='center'){
                     css.top = $(self).offset().top-($(self.tooltip).outerHeight()/2);
                 }else{
                     css.top = $(self).offset().top+$(self).outerHeight();
                 }
            }    
            
            if(position[1]=='left'){
                css.left = $(self).offset().left-$(self.tooltip).outerWidth();    
            }else{
                 if(position[1]=='center'){
                     css.left = $(self).offset().left-(($(self.tooltip).outerWidth()-$(self).outerWidth())/2);
                 }else{
                     css.left = $(self).offset().left+$(self).outerWidth();
                 }
            }                
            
            css.top += options.margin_top;
            css.left += options.margin_left;

            if(options.margin_bottom){
                css.top -= options.margin_bottom;
            }
  
            if(options.max_top!='none'){
                if(css.top>options.max_top)css.top = options.max_top;
                else{
                    if(css.top<options.min_top)css.top = options.min_top;
                }
            }

            if(options.min_left!='none'){
                if(css.left>options.max_left)css.left = options.max_left;
                else{
                    
                    if(css.left<options.min_left)css.left = options.min_left;
                }
            }
            
            css.display = 'none';
            css.visibility = 'visible';
            
            return css;
        };
    });
 };  
})(jQuery);
