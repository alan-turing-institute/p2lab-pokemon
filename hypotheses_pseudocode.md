# Hypothesis Testing Pseudocode

## 1v1 Pokemon Battles

### Experiment Setup:

- Team size: 1
- Total Pokemon: 151
- Battle Mode: ???
- Starting number of teams: 151*151
- Number of Battles per pairing: ??? 
- Generations: `0`
- Mutation rate: `0`
- Breeding: `Off`
- Loss Shuffle: `Off`

### Hypotheses: 

Is there a decay function for the number of battles? The win ratio should converge which will give us a good understanding of the number of battles required. 

How does this change based on the battle-mode? Is there a "good enough" mode that doesn't take too long?

Do we find all the S tier pokemon from the fan rankings?
Do we find all the D tier pokemon from the fan rankings?

Plotting in 2d using the sprites. The first dimension is the fitness, second dimension:
- Base stat total = sum (hp, attack, defence, special attack, special defence, special speed)
- HP
- Attack
- Anything else

Nearest k-nearest neighbours clusters using fitness values, what tiers have we found?



## 2v2 Pokemon Battles

### Experiment Setup:

- Team size: 2
- Total Pokemon: 151
- Battle Mode: `Optimised`
- Starting number of teams: ???
- Number of Battles per pairing: `Optimised`
- Generations: ???
- Mutation rate: ???
- Breeding: `Off`
- Loss Shuffle: `On`

### Hypotheses: 

Are there synergestic pairs that have greater wins compared with the top tier solo pokemon?

Are there pairings of Pokemon types that stand out? (fire and water)

What is the base rate of synergy? Can we see clusters of all the [Type1&Type2] pairs or are there some stand out power couples?

2d clusterplot: first dimension is fitness, second dimension:
- Categorical Pairs by type
- Sum of base stats


Can we find a diminishing returns number of battle repeats that converge on an answer?

Can we find a diminishing returns number of generations that converge on an answer?

What happens with a high versus low mutation rate? to how quickly it finds an answer and how variable the result is. 



## 6v6 Pokemon Battles

### Experiment Setup:

- Team size: 6
- Total Pokemon: 151
- Battle Mode: `Optimised`
- Starting number of teams: ???
- Number of Battles per pairing: `Optimised`
- Generations: ???
- Mutation rate: ???
- Breeding: `On`
- Loss Shuffle: `Off`

### Hypotheses: 

Which is the best Pokemon team?

Are the best teams very related to the top Pokemon, or are there plenty of wildcards?

Are the synergestic pairs in the top teams?

What are the spread of types in the top teams?








