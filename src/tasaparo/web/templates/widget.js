var kaleidos_div = document.getElementById("kaleidos-tasaparo");

var rate_div = document.createElement('div');
rate_div.className = "lresults";
kaleidos_div.appendChild(rate_div);

var rate_value = document.createElement('div');
rate_value.className = "result r" + {{ level }};
rate_value.textContent = {{ rate }}
rate_div.appendChild(rate_value);

var params = document.createElement('div');
params.className = "txt";
//TODO: hacer que los parámetros se separen por <br>
params.textContent = "{{ sex }} {{ age }} {{ province }} {{ education }}";
rate_div.appendChild(params);

document.write('<link rel="stylesheet" href="http://127.0.0.1:8000/static/css/widget.css" type="text/css" media="handheld, all" />');
