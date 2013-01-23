(function() {
    var kaleidosDiv = document.getElementById("kaleidos-tasaparo");

    var logoLink = document.createElement('a');
    logoLink.setAttribute("href", "{{ url }}{{ absolute_url }}");
    logoLink.setAttribute("class", "logo-link");
    logoLink.setAttribute("target", "_new");
    kaleidosDiv.appendChild(logoLink);

    var logo = document.createElement('img');
    logo.src = "{{ url }}/static/images/logo_widget.png";
    logoLink.appendChild(logo);

    var rateValue = document.createElement('div');
    rateValue.className = "result r" + {{ level }};
    rateValue.textContent = {{ rate }}+"%";
    rateValue.setAttribute("href", "{{ url }}{{ absolute_url }}");
    kaleidosDiv.appendChild(rateValue);

    var moreInfoText = document.createElement('div');
    moreInfoText.className = "txt";
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
    
    $('#kaleidos-tasaparo').click( function() {
        var link = "{{ url }}{{ absolute_url }}";
        window.open(link);
    });

}).call(this);
