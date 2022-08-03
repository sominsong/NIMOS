# dockerfile

FROM mongo

WORKDIR /usr/src
RUN mkdir configs
WORKDIR /usr/src/configs

COPY init/* init/

RUN chmod +x init/setup.sh

CMD ["/usr/src/configs/init/setup.sh"]