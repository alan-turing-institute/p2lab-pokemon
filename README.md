<p align="center">
  <img width="30%" alt="p2lab logo" src=assets/logo.png><br>
  <br>
  <a href="https://github.com/alan-turing-institute/p2lab-pokemon/actions">
    <img alt="GitHub Workflow Status" src="https://github.com/alan-turing-institute/p2lab-pokemon/workflows/CI/badge.svg">
  </a>
  <a href="https://codecov.io/gh/alan-turing-institute/p2lab-pokemon" >
    <img src="https://codecov.io/gh/alan-turing-institute/p2lab-pokemon/branch/main/graph/badge.svg?token=2U0YQV7PO6"/>
  </a>
</p>

An interface for optimising Pokémon teams using genetic algorithms!

## Installation

- Clone required repos:

```bash
git clone git@github.com:alan-turing-institute/p2lab-pokemon.git
cd p2lab-pokemon
git submodule update --init --recursive
git clone git@github.com:smogon/pokemon-showdown.git
```

- Install p2lab and poke-env:

```bash
cd poke-env
pip install -e .
cd ..
pip install -e .
```

- Have node installed and install showdown
  - See: https://nodejs.dev/en/learn/how-to-install-nodejs/

```bash
cd pokemon-showdown
npm install  # -g flag sometimes solved problems on our machines
cd ..
```

## Running

To run locally start the pokemon showdown server:

```bash
node pokemon-showdown start --no-security
```

In another terminal, from this project's root directory run:

```bash
p2lab <args>
```

### Additional arguments for p2lab

```bash
usage: p2lab [-h] [--generations GENERATIONS]
             [--team-size TEAM_SIZE] [--teams TEAMS]
             [--seed SEED] [--unique UNIQUE]

options:
  -h, --help            show this help message and
                        exit
  --generations GENERATIONS
                        Number of generations to
                        iterate over
  --team-size TEAM_SIZE
                        Number of pokemon per team
                        (max 6)
  --teams TEAMS         Number of teams i.e.,
                        individuals per generation
  --seed SEED           Random seed to use
  --unique UNIQUE       Determines if a team can have
                        duplicate pokemon species
```

### Docker:

Alternatively, using docker: `docker build -t p2:latest docker/`
`docker run -it -v <path-to-config>.yaml:/home/p2lab-pokemon/config.yaml p2`

The docker image is built to start a server and run `p2lab` with the config
mounted at the root of the repo.

## Components used

### Pokemon showdown engine:

[smogon/pokemon-showdown](https://github.com/smogon/pokemon-showdown)

- Has instructions on setting up our own server (needed to run battles!)
- Also features command-line utilities for generating/validating new teams

### Poke-env

- Wicked fast at simulating battles via pokemon showdown engine
- https://poke-env.readthedocs.io/en/stable/getting_started.html
