# -*- coding: utf-8 -*-
# Copyright (C) 2018  Louis Sugy
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import mutagen

# Local imports
from common_utils import get_music_files_in_dir

# Debug levels:
#    0: no debug message
#    1: file can't be parsed
#    2: file doesn't have genre
DEBUG = 0


def main():
    """Interact with the user to harmonize the genre tag of the music
    tracks in a given directory.
    """

    # Prompt the path in which music tracks will be browsed
    dirpath = input("Directory path: ")

    # Prompt the keywords which should appear in the genre
    keywords_input = input("Comma-separated list of keywords: ")
    keywords = [keyword.strip().lower()
                for keyword in keywords_input.split(",")]

    # Browse files
    print("Browsing files...")
    music_files = get_music_files_in_dir(dirpath)

    # Associate files to a genre
    genres_files = get_genres_files(music_files, keywords)

    # Get the distinct genres
    unique_genres = sorted(get_unique_genres(genres_files))
    if len(unique_genres) == 0:
        print("No matching genre has been found")
        return

    # Display the genres to the user
    print("--- Found genres ---")
    for i in range(len(unique_genres)):
        print("%d: %s" % (i + 1, unique_genres[i]))
    print("---")

    while True:
        # Prompt genres to harmonize
        genres_input = input(
            "Comma-separated list of the numeros of the genres to harmonize:\n")
        try:
            genres_choice = [int(genre) - 1 for genre in genres_input.split(",")]
            for numero in genres_choice:
                if numero < 0 or numero >= len(unique_genres):
                    raise ValueError
        except ValueError:
            print("Error: invalid choice.")
            return
        if len(genres_choice) == 0:
            print("No genre chosen")
            return

        # Prompt new genre name
        new_name = input("New genre name: ").strip()

        # Replace chosen genres by chosen name
        print("Renaming chosen genres...")
        replaced_genres = set(unique_genres[i] for i in genres_choice)
        replace_genres(genres_files, replaced_genres, new_name)

        userchoice = input("Do another operation on this selection? (Y/n): ")
        if userchoice == "n":
            return


def get_genres_files(music_files, keywords):
    """Associate each filepath to a genre read in metatags, if the genre
    contains one of the keywords, or if no keyword is given."""
    genres_files = {}
    for filepath in music_files:
        # Try to read the file's metatags
        try:
            mhandler = mutagen.File(filepath)
        except mutagen.MutagenError:
            if DEBUG:
                print("File %s could not be parsed by Mutagen" % filepath)
            continue

        if 'genre' not in mhandler:
            if DEBUG >= 2:
                print("File %s has no genre" % filepath)
            continue

        for genre in mhandler['genre']:
            if not genre:
                continue

            # If genre already seen, we directly add the filepath
            if genre in genres_files:
                genres_files[genre].append(filepath)
            else:
                # Test that the genre matches the keywords, or if there are
                # no keywords specified
                genre_lower = genre.lower()
                genre_matches = (len(keywords) == 0)
                for keyword in keywords:
                    if keyword in genre_lower:
                        genre_matches = True
                        break

                if genre_matches:
                    genres_files[genre] = [filepath]

    return genres_files


def get_unique_genres(genres_files):
    """Return a set of all the distinct genres in the dictionary which
    associates files paths to their genres.
    """
    return set(genres_files.keys())


def replace_genres(genres_files, replaced_genres, new_name):
    """Renames the given genres by the given name in the files passed via
    a dictonary genre: files.
    """
    for genre in replaced_genres:
        for filepath in genres_files[genre]:
            try:
                mhandler = mutagen.File(filepath)
                genres = mhandler['genre']
            except mutagen.MutagenError:
                print("Error parsing file %s" % filepath)
                continue
            except KeyError:
                print("File %s has no genre" % filepath)
                continue

            for i in range(len(genres)):
                if genres[i] in replaced_genres:
                    genres[i] = new_name
            genres = list(set(genres))

            try:
                mhandler['genre'] = genres
                mhandler.save()
            except mutagen.MutagenError:
                print("Could not write file %s" % filepath)
                continue


if __name__ == "__main__":
    while True:
        main()
        userchoice = input("Make another selection? (Y/n): ")
        if userchoice == "n":
            break
