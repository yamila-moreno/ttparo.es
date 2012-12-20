(function() {
    var kaleidosDiv = document.getElementById("kaleidos-tasaparo");

    var moreInfoLink = document.createElement('a');
    moreInfoLink.className =
    moreInfoLink.href = "http://127.0.0.1:8000{{ absolute_url }}";
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
    stylesheet.href = "http://127.0.0.1:8000/static/css/widget.css";
    stylesheet.rel = "stylesheet";
    stylesheet.type = "text/css";
    //stylesheet.media = "handheld, all";
    kaleidosDiv.appendChild(stylesheet);

}).call(this);


//<div id="kaleidos-tasaparo"> kaleidosDiv
    // <a href>+ info</a>
   //<div class="lresults">    rateDiv
        //<div class="result r3">7%</div> rateValue
       //<div class="txt">género indiferente<br>de 55 A 59 años<br>Málaga<br>Universidad (Licenciatura o Diplomatura)</div> params
  //</div>
  //<link href="http://127.0.0.1:8000/static/css/widget.css" rel="stylesheet" type="text/css" media="handheld, all">
//</div>
