FROM "debian:12-slim"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gdebi-core \
        git \
        make
    
COPY ./.devcontainer/pkg /tmp/

RUN  gdebi -n /tmp/faircamp_1.3.0-1+deb12_amd64.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives
