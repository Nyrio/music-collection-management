# Music collection management tools

This repository provides tools to manage your music collection, because editing metatags by hand is a long and boring work, but for those like me who are very organized, it has to be done.

It's *work in progress*: I'll hopefully add more tools over time.

## Installation

### Manual installation

To use these tools you need to [install Python](https://www.python.org/downloads/). Then clone or download this repository, and install the dependencies with the python package manager `pip` by running in the root folder of the project:

```bash
pip install -r requirements.txt
```

Then execute the tool of your choice :)


### Windows standalone

*TODO*


## Tools

Tools are found in the `src` directory.

### Harmonize genres

`harmonize_genre.py` runs an interactive command-line interface where the user is asked a directory and keywords, and can rename a list of genres in the resulting selection.

Example:
```
Directory path: C:\Users\Louis Sugy\Music
Comma-separated list of keywords: pop
Browsing files...
--- Found genres ---
1: Britpop
2: French Pop, Chanson, Singer/Songwriter
3: Pop
4: Pop, Variete Francaise
5: Pop-Folk
6: Pop-Punk
7: Pop-Rock
8: Synth Pop / Electro Hip Hop
9: pop
---
Comma-separated list of the numeros of the genres to harmonize:
2,4
New genre name: French Pop
Renaming chosen genres...
Do another operation on this selection? (Y/n): y
Comma-separated list of the numeros of the genres to harmonize:
3,9
New genre name: Pop
Renaming chosen genres...
```