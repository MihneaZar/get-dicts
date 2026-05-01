## Description
Script that opens online dictionaries based on given arguments. <br>
Especially useful when saved as a console command or with a hotkey (using [AutoHotkey](https://www.autohotkey.com/) or a similar tool).

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
- a      (--s[ave]): save current search options.

Last used options will be reused if none are provided.
