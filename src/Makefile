all: bower mainjs tasaparojs compileless

dependences:
	npm install uglify-js less jshint


compileless:
	./node_modules/less/bin/lessc --yui-compress tasaparo/web/static/css/styles.less tasaparo/web/static/css/styles.css

bower:
	bower install
	wget http://elycharts.googlecode.com/svn/tags/stable/dist/elycharts.js -O app/components/elycharts.js
	cp app/components/less/dist/less-1.7.1.js tasaparo/web/static/js/libs/less.js

mainjs:
	./node_modules/uglify-js/bin/uglifyjs \
					      app/components/json2/json2.js \
					      app/components/jquery/dist/jquery.js \
						  app/components/raphael/raphael.js \
					      tasaparo/web/static/js/libs/tooltip.js \
					      app/components/elycharts.js \
					      app/components/lodash/dist/lodash.compat.js \
						  app/components/backbone/backbone.js \
					      	-o tasaparo/web/static/js/main.min.js

tasaparojs:
	./node_modules/uglify-js/bin/uglifyjs  tasaparo/web/static/js/tasaparo.js \
							tasaparo/web/static/js/mapdata.js \
							tasaparo/web/static/js/app.js \
							-c -o  tasaparo/web/static/js/tasaparo.min.js

