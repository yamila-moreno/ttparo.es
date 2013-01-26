all: mainjs tasaparojs compileless

dependences:
	npm install uglify-js less jshint


compileless:
	./node_modules/less/bin/lessc --yui-compress tasaparo/web/static/css/styles.less tasaparo/web/static/css/styles.css

tasaparojs:
	./node_modules/uglify-js/bin/uglifyjs  tasaparo/web/static/js/tasaparo.js \
							tasaparo/web/static/js/mapdata.js \
							tasaparo/web/static/js/app.js \
							-c -o  tasaparo/web/static/js/tasaparo.min.js

