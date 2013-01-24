(function() {
    var kaleidosDiv = document.getElementById("kaleidos-tasaparo");

    var logoLink = document.createElement('a');
    logoLink.className = "ttdp-a";
    logoLink.setAttribute("href", "{{ url }}{{ absolute_url }}");
    logoLink.setAttribute("class", "ttdp-logo-link");
    logoLink.setAttribute("target", "_new");
    kaleidosDiv.appendChild(logoLink);

    var logo = document.createElement('img');
    logo.src = "{{ url }}/static/images/logo_widget.png";
    logoLink.appendChild(logo);

    var rateValue = document.createElement('div');
    rateValue.className = "result ttdp-r" + {{ level }};
    rateValue.textContent = {{ rate }}+"%";
    rateValue.setAttribute("href", "{{ url }}{{ absolute_url }}");
    kaleidosDiv.appendChild(rateValue);

    var moreInfoText = document.createElement('div');
    moreInfoText.className = "ttdp-txt";
    kaleidosDiv.appendChild(moreInfoText);
    
    var moreInfoLink = document.createElement('a');
    moreInfoLink.setAttribute("href", "{{ url }}{{ absolute_url }}");
    moreInfoLink.setAttribute("target", "_new");
    moreInfoLink.innerHTML = "+ Info";
    moreInfoText.appendChild(moreInfoLink);

    var stylesheet = document.createElement('link');
    stylesheet.href = "{{ url }}/static/css/widget.css";
    stylesheet.rel = "stylesheet";
    stylesheet.type = "text/css";
    kaleidosDiv.appendChild(stylesheet);
    
    var element =  document.getElementById('kaleidos-tasaparo');
    element.onclick = function(){ 
    var link = "{{ url }}{{ absolute_url }}";
        window.open(link);
     };
}).call(this);
