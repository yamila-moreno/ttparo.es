(function() {
    var kaleidosDiv = document.getElementById("kaleidos-tasaparo");

    var moreInfoLink = document.createElement('a');
    moreInfoLink.href = "{{ url }}{{ absolute_url }}";
    moreInfoLink.target = "_new";
    kaleidosDiv.appendChild(moreInfoLink);

    var logo = document.createElement('img');
    logo.src = "{{ url }}/static/images/logo_widget.png";
    moreInfoLink.appendChild(logo);

    var rateValue = document.createElement('div');
    rateValue.className = "result r" + {{ level }};
    rateValue.textContent = {{ rate }}+"%";
    moreInfoLink.appendChild(rateValue);

    var moreInfoText = document.createElement('div');
    moreInfoText.className = "txt";
    moreInfoText.innerHTML = "+ INFO";
    moreInfoLink.appendChild(moreInfoText);

    var stylesheet = document.createElement('link');
    stylesheet.href = "{{ url }}/static/css/widget.css";
    stylesheet.rel = "stylesheet";
    stylesheet.type = "text/css";
    kaleidosDiv.appendChild(stylesheet);

}).call(this);
