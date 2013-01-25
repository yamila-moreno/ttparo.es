all: mainjs tasaparojs compileless

dependences:
	npm install uglify-js less jshint


compileless:
	./node_modules/less/bin/lessc --yui-compress tasaparo/web/static/css/styles.less tasaparo/web/static/css/styles.css

mainjs:
	./node_modules/uglify-js/bin/uglifyjs \
					      tasaparo/web/static/js/libs/json2.js \
					      tasaparo/web/static/js/libs/jquery-1.8.3.js \
					      tasaparo/web/static/js/libs/raphael.js \
					      tasaparo/web/static/js/libs/tooltip.js \
					      tasaparo/web/static/js/libs/elycharts.js \
					      tasaparo/web/static/js/libs/underscore.js \
					      tasaparo/web/static/js/libs/backbone.js \
					      	-o tasaparo/web/static/js/main.min.js

tasaparojs:
	./node_modules/uglify-js/bin/uglifyjs  tasaparo/web/static/js/tasaparo.js \
							tasaparo/web/static/js/mapdata.js \
							tasaparo/web/static/js/app.js \
							-c -o  tasaparo/web/static/js/tasaparo.min.js

