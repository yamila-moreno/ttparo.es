(function() {
    var kaleidosDiv = document.getElementById("kaleidos-tasaparo");

    var moreInfoLink = document.createElement('a');
    moreInfoLink.className =
    moreInfoLink.href = "{{ host }}/{{ absolute_url }}";
    moreInfoLink.target = "_new";
    kaleidosDiv.appendChild(moreInfoLink);

    var rateDiv = document.createElement('div');
    rateDiv.className = "lresults";
    moreInfoLink.appendChild(rateDiv);

    var rateValue = document.createElement('div');
    rateValue.className = "result r" + {{ level }};
    rateValue.textContent = {{ rate }}+"%";
    rateDiv.appendChild(rateValue);

    //var params = document.createElement('div');
    //params.className = "txt";
    //params.innerHTML = "{{ sex }}<br />{{ age }}<br />{{ province }}<br />{{ education }}";
    //rateDiv.appendChild(params);

    var moreInfoText = document.createElement('div');
    moreInfoText.className = "txt";
    moreInfoText.innerHTML = "+ INFO";
    rateDiv.appendChild(moreInfoText);

    var stylesheet = document.createElement('link');
    stylesheet.href = "{{ host }}/static/css/widget.css";
    stylesheet.rel = "stylesheet";
    stylesheet.type = "text/css";
    //stylesheet.media = "handheld, all";
    kaleidosDiv.appendChild(stylesheet);

}).call(this);
