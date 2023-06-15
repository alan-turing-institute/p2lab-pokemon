from python

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install nodejs npm -y

ENV ROOT_DIR=/home
ENV P2_PATH=$ROOT_DIR/P2-Lab

RUN git clone https://github.com/alan-turing-institute/P2-Lab $P2_PATH
RUN git clone https://github.com/smogon/pokemon-showdown $P2_PATH/pokemon-showdown
RUN git clone https://github.com/AoifeHughes/poke-env $P2_PATH/poke_env
RUN git clone https://github.com/phinate/showdown $P2_PATH/showdown

RUN python3 -m venv $P2_PATH/venv-pokemon
RUN pip install --upgrade pip setuptools wheel

RUN pip install -e $P2_PATH
RUN pip install -e $P2_PATH/poke_env

RUN npm install -g $P2_PATH/pokemon-showdown

WORKDIR $P2_PATH/pokemon-showdown
ENTRYPOINT node pokemon-showdown start --no-security && python $P2_PATH/run.py
