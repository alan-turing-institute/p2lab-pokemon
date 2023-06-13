# P2-Lab

An interface for optimising pokemon teams using genetic algorithms!

## Components

### Pokemon showdown engine:
[smogon/pokemon-showdown](https://github.com/smogon/pokemon-showdown)

- Has instructions on setting up our own server (needed to run battles!)
- Also features command-line utilities for generating/validating new teams

### Pokemon battle bot by pmargilia:
[pmargilia/showdown](https://github.com/pmariglia/showdown)

- Can interface into a server
- Can both launch and accept battle challenges --> we can make the bots battle!
- Already calculates wins/losses in its code (but we need to figure out the best
  way to get that info)
- Can be run locally or in a docker container

### Poke-env 

- Wicked fast at simulating battles via pokemon showdown engine
- A potential replacement for the battle bot by pmargilia

###  Genetic algorithm library: TBD

### This library, `p2lab`:

- Aiming to be a python module to steer a bunch of bots into battling, collect
  the results, then run a genetic algorithm step!
