lltag:
	lltag ./catalog/Releases/ -R  -p --id3v2 --yes

tag:
	python3 ./src/scripts/tag_audio_files.py ./content

preview:
	faircamp --catalog-dir ./content/ --build-dir ./var/build --cache-dir ./var/cache --preview

build:
	faircamp --catalog-dir ./content/ --build-dir ./var/build --cache-dir ./var/cache

catalog:
	python3 ./src/scripts/json_to_eno.py ./content/catalog.json > ./content/catalog.eno

inject-admin:
	cp -R ./src/admin ./var/build/