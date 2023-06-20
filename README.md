<p align="center">
  <img width="30%" alt="relaxed logo" src=assets/logo.png><br>
  <br>
  <a href="https://github.com/alan-turing-institute/p2lab-pokemon/actions">
    <img alt="GitHub Workflow Status" src="https://github.com/alan-turing-institute/p2lab-pokemon/workflows/CI/badge.svg">
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

- Have node installed
  - See: https://nodejs.dev/en/learn/how-to-install-nodejs/

## Running

To run locally start the pokemon showdown server:

```bash
cd pokemon-showdown
node pokemon-showdown start --no-security
```

In another terminal, from this project's root directory run:

```bash
p2lab <args>
```

### Additional arguments for p2lab

```bash
usage: p2lab [-h] [--generations GENERATIONS] [--teamsize TEAMSIZE] [--numteams NUMTEAMS] [--seed SEED] [--unique UNIQUE]

options:
  -h, --help            show this help message and exit
  --generations GENERATIONS
                        Number of generations to iterate over
  --teamsize TEAMSIZE   Number of pokemon per team (max 6)
  --numteams NUMTEAMS   Number of teams i.e., individuals per generation
  --seed SEED           Random seed to use
  --unique UNIQUE       Determines if a team can have duplicate pokemon species
```

### Docker:

Alternatively, using docker: `docker build -t p2:latest .`
`docker run -it p2:latest` `docker exec -it your_container_id /bin/bash`

Run docker build with `--no-cache` to rebuild with newer versions of the repos.

## Components used

### Pokemon showdown engine:

[smogon/pokemon-showdown](https://github.com/smogon/pokemon-showdown)

- Has instructions on setting up our own server (needed to run battles!)
- Also features command-line utilities for generating/validating new teams

### Poke-env

- Wicked fast at simulating battles via pokemon showdown engine
- https://poke-env.readthedocs.io/en/stable/getting_started.html
