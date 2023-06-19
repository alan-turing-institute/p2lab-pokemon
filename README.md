<p align="center">
  <img width="30%" alt="relaxed logo" src=assets/logo.png><br>
  <br>
  <a href="https://github.com/alan-turing-institute/p2lab-pokemon/actions">
    <img alt="GitHub Workflow Status" src="https://github.com/alan-turing-institute/p2lab-pokemon/workflows/CI/badge.svg">
  </a>
</p>

An interface for optimising pokemon teams using genetic algorithms!

## Installation

steps:

- clone the repo
- install the module in a virtual environment with `pip install -e .`
- initialise submodules with `git submodule update --init --recursive`
  - if you're having problems, you can directly clone poke-env with
    `git clone https://github.com/aoifehughes/poke-env.git`
- cd into `poke-env` and run `pip install -e .`
- cd back to the root directory and clone the `pokemon-showdown` repo with
  `git clone https://github.com/smogon/pokemon-showdown`
- if you don't have node, install it with `brew install node` (mac) or
  `sudo apt install nodejs` (linux)
- install with `npm install` in the `pokemon-showdown` directory
- start a local server with `node pokemon-showdown start --no-security` in the
  `pokemon-showdown` directory
- to run a small demo, you should be able to just run `p2lab` from the command
  line!

or via Docker:

`docker build -t p2:latest .` `docker run -it p2:latest`
`docker exec -it your_container_id /bin/bash`

Run docker build with `--no-cache` to rebuild with newer versions of the repos.

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
