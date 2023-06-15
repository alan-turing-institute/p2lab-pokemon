# P2-Lab

An interface for optimising pokemon teams using genetic algorithms!

## Installation

steps:

- clone the repo
- install the module in a virtual environment with `pip install -e .`
- initialise submodules with `git submodule update --init --recursive`
- cd into `poke-env` and run `pip install -e .`
- cd back to the root directory and clone the `pokemon-showdown` repo with
  `git clone https://github.com/smogon/pokemon-showdown`
- install with `npm install pokemon-showdown` in the `pokemon-showdown`
  directory
- start a local server with `node pokemon-showdown start --no-security` in the
  `pokemon-showdown` directory
- cd back to the root directory and run `python run.py` to run the demo!

or via Docker:

`docker build -t p2:latest .` `docker run -it p2:latest`
`docker exec -it your_container_id /bin/bash`

then go to the P2 root and run the script. Run docker build with `--no-cache` to
rebuild with newer versions of the repos.

## Components

### Pokemon showdown engine:

[smogon/pokemon-showdown](https://github.com/smogon/pokemon-showdown)

- Has instructions on setting up our own server (needed to run battles!)
- Also features command-line utilities for generating/validating new teams

### Pokemon battle bot by pmargilia (not used yet)

[pmargilia/showdown](https://github.com/pmariglia/showdown)

- Can interface into a server
- Can both launch and accept battle challenges --> we can make the bots battle!
- Already calculates wins/losses in its code (but we need to figure out the best
  way to get that info)
- Can be run locally or in a docker container

### Poke-env

- Wicked fast at simulating battles via pokemon showdown engine
- A potential replacement for the battle bot by pmargilia
- https://poke-env.readthedocs.io/en/stable/getting_started.html

### Genetic algorithm library: TBD

### This library, `p2lab`:

- Aiming to be a python module to steer a bunch of bots into battling, collect
  the results, then run a genetic algorithm step!
