# Menu Version

## Description
Menu for choosing online dictionaries and opening them with a search query.

## Requirements 
- The [ConsoleListInterface](https://github.com/MihneaZar/ConsoleListInterface) for the MenuInterface class;
- The [PyYAML](https://pypi.org/project/PyYAML/) library for the main menu.

## Help Page
Command-line arguments:
- '-h' or  '--help': print this help page.
- '-d' or '--debug': print debug info without opening links or saving options.

Search in english/romanian dictionaries. <br>
Syntax: '{search query} [-options] [--option_name[ --option_name]]'.
Search query can have spaces.

The options are:
- e   (--e[nglish]): search in english dictionaries (default).
- r  (--r[omanian]): search in romanian dictionaries.
- t (--t[ranslate]): translate (reverso -> will choose language based on query words).
- i (--i[ncognito]): search in incognito.
- s      (--s[ave]): save current search options.

Last used options will be reused if none are provided.

-------------------------------------------------------------------------

*Copyright (c) 2026 Mihnea Bogdan Zarojanu*
