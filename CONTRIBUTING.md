# Setting up a python development environment

After cloning this repository, navigate into it and run the following commands:

```bash
python3 -m venv venv-pokemon
source ./venv-pokemon/bin/activate
pip install --upgrade pip setuptools wheel
pip install -e .
```

These commands do the following, in order:

- Create a new python environment called `venv-pokemon` (you can call it
  whatever you want, but this is what I'll use in this README)
- Activate the environment, which means that any python commands you run will
  use the python version in this environment (rather than the system python
  version)
  - Note that you'll need to run `source ./venv-pokemon/bin/activate` every time
    you want to use this environment in a new terminal -- you can check if
    you're using the environment by running `which python` and checking that it
    points to `.../venv-pokemon/bin/activate`, where `...` will be wherever you
    cloned this repo
- Upgrade `pip`, `setuptools`, and `wheel` to the latest versions
- Install the module in editable mode (i.e. you can make changes to the code for
  `p2lab` and they'll be reflected in any code that uses `p2lab` without having
  to reinstall the whole module)

The module is now installed in a new python environment called `venv-pokemon`.
This means that you can import the module `p2lab` in any python file or jupyter
notebook you want, provided that you activate the environment first. If you want
to use this environment in a jupyter notebook, you can do the following:

```bash
pip install ipykernel
python -m ipykernel install --user --name=venv-pokemon
```

This will install a new kernel called `venv-pokemon` that you can select in the
jupyter notebook interface (Kernel -> Change kernel -> venv-pokemon).

# Post setup

The next step is to take advantage of `pre-commit`, which will automatically
format your code and run some basic checks before you commit:

```bash
pip install pre-commit  # or brew install pre-commit on macOS
pre-commit install  # Will install a pre-commit hook into the git repo
```

You can also/alternatively run `pre-commit run --all-files` to run the checks
yourself (works even if you forget to run `pre-commit install`, I do this fairly
often...)

# How to write and commit python code to p2lab

This section is to show you how to add new functionality to the `p2lab` module,
which we'll use to steer the genetic algorithm pipeline in python.

Say you want to make a new function to check the validity of a pokemon name, for
instance. The first thing you should do is create a new branch:

```bash
git checkout -b pokemon-name-check
```

Then, if there's not already a `.py` file in `src/p2lab` that covers the
category of thing you want to do, you'll need to create a new file in
`src/p2lab` -- say we call it `pokemon.py`. This file could contain a function
called `is_valid_pokemon_name` that takes a string as input and returns `True`
if the string is a valid pokemon name, and `False` otherwise. For instance,
`is_valid_pokemon_name("pikachu")` should return `True`, but
`is_valid_pokemon_name("pikachuuuu")` should return `False`.

This will appear in the module as `p2lab.pokemon.is_valid_pokemon_name`. You can
then import it in any new jupyter notebook or python file as follows:

```python
from p2lab.pokemon import is_valid_pokemon_name

is_valid_pokemon_name("pikachu")  # True
```

Once you're done writing your code, you can commit it to your branch:

```bash
git add src/p2lab/pokemon.py
git commit -m "Add pokemon name checker"
```

If the pre-commit hook is installed, it will automatically format your code and
run some basic checks when you commit. If any check fails (you'll probably see
some red somewhere), the commit will be aborted. If the file was being
formatted, you'll need to add it again and commit again, i.e. just add+commit
twice in a row:

```bash
git add src/p2lab/pokemon.py
git commit -m "Add pokemon name checker"  # This could fail due to formatting
git add src/p2lab/pokemon.py
git commit -m "Add pokemon name checker" # This may succeed now
```

If it still fails, you'll need to fix any errors manually. Once the commit
succeeds, you can push your branch to github:

```bash
git push origin pokemon-name-check
```

Then, you can go to the github page for this repo and open a pull request so we
can merge your awesome code 🤗

# Testing

I don't have any thought-through plans for unit tests, but if things go well,
the repo is set up to use `pytest` for testing. This would require you to
install the `.[test]` extras when you install the module, which you can do in a
bash shell with:

```bash
pip install -e .[test]
```

or on zsh (probably the case if you're on macOS):

```bash
pip install -e ".[test]"
```

After that, to run the tests, you can do:

```bash
pytest
```

from the root of the repo. This will run all the tests in the `tests` directory.
If you want to run a specific test, you can do:

```bash
pytest tests/test_pokemon.py
```

which will run all the tests in `tests/test_pokemon.py`. Alternatively, you can
search for a specific test by name:

```bash
pytest -k "test_pokemon_name"
```

which will run all the tests that have "test_pokemon_name" in their name.
