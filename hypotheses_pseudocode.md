# Hypothesis Testing Pseudocode

## 1v1 Pokemon Battles

### Experiment Setup:

- Team size: 1
- Total Pokemon: 151
- Battle Mode: ???
- Number of Battles per pairing: ??? [25,50,100, etc]
- Generations: `0`
- Mutation rate: `0`
- Breeding: `Off`

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


