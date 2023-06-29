from python

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install nodejs npm -y

ENV ROOT_DIR=/home
ENV P2_PATH=$ROOT_DIR/p2lab-pokemon

RUN git clone https://github.com/alan-turing-institute/p2lab-pokemon $P2_PATH
RUN git clone https://github.com/smogon/pokemon-showdown $P2_PATH/pokemon-showdown
RUN git clone https://github.com/AoifeHughes/poke-env $P2_PATH/poke_env

RUN python3 -m venv $P2_PATH/venv-pokemon
RUN pip install --upgrade pip setuptools wheel

RUN pip install -e $P2_PATH
RUN pip install -e $P2_PATH/poke_env

RUN npm install -g $P2_PATH/pokemon-showdown

COPY ./entrypoint.sh $P2_PATH/pokemon-showdown/entrypoint.sh
RUN chmod +x $P2_PATH/pokemon-showdown/entrypoint.sh

WORKDIR $P2_PATH/pokemon-showdown

ENTRYPOINT $P2_PATH/pokemon-showdown/entrypoint.sh
