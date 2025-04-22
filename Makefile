lltag:
	lltag ./catalog/Releases/ -R  -p --id3v2 --yes

tag:
	python3 ./scripts/tag_audio_files.py ./content

preview:
	faircamp --catalog-dir ./content/ --build-dir ./var/build --cache-dir ./var/cache --preview

build:
	faircamp --catalog-dir ./content/ --build-dir ./var/build --cache-dir ./var/cache

inject-admin:
	cp -R ./admin ./var/build/