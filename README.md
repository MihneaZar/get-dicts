# Menu Version

## Description
Menu for choosing online dictionaries and opening them with a search query.

## Requirements 
- The [ConsoleListInterface](https://github.com/MihneaZar/ConsoleListInterface) for the MenuInterface class;
- The [PyYAML](https://pypi.org/project/PyYAML/) library for the main menu structure.


## Dictionaries Menu
In the menu, the following options will be listed:
- 'Search': search a word or phrase on the selected online dictionaries, with the selected chrome options;
- 'Save selection': save the current selection of dictionaries and chrome options to be auto-selected next time the program runs;
- Dictionary links and chrome arguments: the list of dictionaries and chrome command-line arguments, which can be selected or deselected to be active in the searches;
- 'Stop/Keep running after search': by default it is 'Stop' and the program will end after the first non-empty search; by switching it to 'Keep', the program will keep running after any search;
- 'Exit': quit application.


## Adding Dictionaries and Chrome Options
In the 'options.json' file, additional dictionary URLs and chrome command-line arguments can be added. <br>
For dict URLs, a list of dictionary links needs to be provided, with the '{query}' string in the place where the search query should be. <br>
For chrome arguments, a string with the chrome argument should be added (the entire list of arguments is [here](https://peter.sh/experiments/chromium-command-line-switches/)). <br>
A few examples are already present, with an entry for three English dictionaries, an entry for two Romanian ones, an entry for the [Reverso](https://context.reverso.net/traducere/engleza-romana/) English-Romanian translator, and one entry each for the '-incognito' and the '/new_window' chrome options.<br>

A few notes:
- the order of the entries in the 'options.json' determines both their order in the menu, but also the order in which the links are opened;
- as is shown in the '\_comments', entries can be removed from the menu by adding an '\_' at the beginning of their name, without having to actually delete them;
- multiple chrome options can be added in the same entry simply by adding them with spaces in between.

## Direct Search from Command-Line
Adding '--search' or '-s' as a command-line argument will directly prompt the search query, open dictionaries according to currently-saved selection, then quit. <br>
On top of that, the arguments '--clear' or '-c' will clear the screen and prompt the direct search query at the same position as the menu option does. 

-------------------------------------------------------------------------

*Copyright (c) 2026 Mihnea Bogdan Zarojanu*
