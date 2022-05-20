yarn build
cat build/static/js/2.*.js build/static/js/main.*.js build/static/js/runtime*.js > ../embed_website/full-bundle.js
