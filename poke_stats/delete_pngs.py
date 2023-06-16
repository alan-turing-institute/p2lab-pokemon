from __future__ import annotations

import os
import pickle

# Directory path where the files are located
directory = "/Users/lfrance/OneDrive - The Alan Turing Institute/002_Projects/Pokemon/poke-images/pokesprite/pokemon-gen8/regular"

pickle_file = "poke_base_stats.pkl"

with open(pickle_file, "rb") as file:
    pokemon_dict = pickle.load(file)
# Get a list of all filenames in the directory
filenames = os.listdir(directory)

print(pokemon_dict.keys())

pokemon_names = list(pokemon_dict.keys())
for filename in filenames:
    file_path = os.path.join(directory, filename)

    # Extract the Pokémon name from the filename
    pokemon_name = filename[:-4]  # Remove the ".png" extension

    # Check if the Pokémon name is not present in the dictionary
    if pokemon_name not in pokemon_names:
        # Delete the file
        os.remove(file_path)
        print(f"Deleted file: {filename}")
