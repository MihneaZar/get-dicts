# Menu Version

## Description
Menu for choosing online dictionaries and opening them with a search query.

## Requirements 
- The [ConsoleListInterface](https://github.com/MihneaZar/ConsoleListInterface) for the MenuInterface class;
- The [PyYAML](https://pypi.org/project/PyYAML/) library for the main menu.


## Dictionaries Menu
In the menu, the following options will be listed:
- 'Search': search a word or phrase on the selected online dictionaries, with the selected chrome options;
- 'Save selection': save the current selection of dictionaries and chrome options to be auto-selected next time the program runs:
- Dictionary links and chrome arguments: the list of dictionaries and chrome command-line arguments, which can be selected or deselected to be active in the searches;
- 'Stop/Keep running after search': by default it is 'Stop' and the program will end after the first non-empty search; by switching it to 'Keep', the program will keep running after every search;
- 'Exit': quit application.


## Adding Dictionaries and Chrome Options
In the 'options.json' file, additional dictionary URLs and chrome command-line arguments can be added. <br>
For dict URLs, a list of dictionary links needs to be provided, with the '{query}' string in the place where the search query should be. <br>
For chrome args, a string with the chrome argument should be added (the entire list of arguments is [here](https://peter.sh/experiments/chromium-command-line-switches/). <br>
A few examples are already present, for a few English dictionaries, a few Romanian ones, and the [Reverso](https://context.reverso.net/traducere/engleza-romana/) English-Romanian translator, along with the '-incognito' and '/new_window' chrome options.

A few notes:
- the order of the entries in the 'options.json' determines both their order in the menu, but also the order in which the links are opened;
- as is shown in the '_comments', entries can be removed from the menu by adding an '_' to the beginning of their name, without having to actually delete them;
- multiple chrome options can be added in the same entry simply by adding them with spaces in between.

-------------------------------------------------------------------------

*Copyright (c) 2026 Mihnea Bogdan Zarojanu*
