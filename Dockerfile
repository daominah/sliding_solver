FROM daominah/python37

RUN apt-get -yq install ffmpeg libsm6 libxext6
COPY ./requirements.txt /requirements.txt
RUN ${BIN_PYTHON} -m pip install -r /requirements.txt

ENV APP_DIR=/python/src/app
WORKDIR ${APP_DIR}
COPY . ${APP_DIR}
RUN ${BIN_PYTHON} main_test.py

EXPOSE 15715

CMD ["bash", "-c", "${BIN_PYTHON} ${APP_DIR}/main.py"]
