all: mainjs tasaparojs

dependences:
	npm install uglify-js less jshint


mainjs:
	./node_modules/uglify-js/bin/uglifyjs \
					      tasaparo/web/static/js/libs/json2.js \
					      tasaparo/web/static/js/libs/jquery-1.8.3.min.js \
					      tasaparo/web/static/js/libs/raphael-min.js \
					      tasaparo/web/static/js/libs/tooltip.js \
					      tasaparo/web/static/js/libs/elycharts.min.js \
					      tasaparo/web/static/js/libs/underscore-min.js \
					      tasaparo/web/static/js/libs/backbone-min.js \
					      	-o tasaparo/web/static/js/main.min.js
tasaparojs:
	./node_modules/uglify-js/bin/uglifyjs  tasaparo/web/static/js/tasaparo.js \
						-c -o  tasaparo/web/static/js/tasaparo.min.js
