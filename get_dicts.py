import subprocess
import sys
import os

HOMEPATH = os.path.dirname(os.path.realpath(__file__))
sys.stderr = open(f'{HOMEPATH}/errors.txt', "a")

try:
    SAVED_OPTIONS = open(f'{HOMEPATH}/.opts').read()
except:
    SAVED_OPTIONS = 'e'

HELP = """Command-line arguments:
'-h' or  '--help': print this help page.
'-d' or '--debug': print debug info without opening links or saving options.
"""

EXPLAIN = """Search in english/romanian dictionaries.
Syntax: '{search query} [-options] [--option_name[ --option_name]]'.
Search query can have spaces.

The options are: 
e   (--e[nglish]): search in english dictionaries (default).
r  (--r[omanian]): search in romanian dictionaries.
t (--t[ranslate]): translate (reverso -> will choose language based on query words).
i (--i[ncognito]): search in incognito.
s      (--s[ave]): save current search options.

Last saved options (or '-e') will be reused if none are provided."""

ENGLISH = [
    "https://www.thesaurus.com/browse/{query}",
    "https://www.merriam-webster.com/thesaurus/{query}",
    "https://www.wordhippo.com/what-is/another-word-for/{query}.html"
]
ROMANIAN = [
    "https://dexonline.ro/definitie/{query}", 
    "https://www.dictionardesinonime.ro/?c={query}"
]
REVERSO = "https://context.reverso.net/traducere/engleza-romana/{query}"

OPTIONS = ["english", "romanian", "translate", "incognito"]

def main():
    os.system('title Dictionaries')

    debug = ('-d' in sys.argv or '--debug' in sys.argv)
    help  = ('-h' in sys.argv or '--help' in sys.argv)

    if help: 
        print(HELP)
        print(EXPLAIN)
        return

    if not debug and 2 <= len(sys.argv):
        search = " ".join(sys.argv[1:])
    else:
        print(EXPLAIN)
        saved_options = ", ".join([f'--{option}' for option in OPTIONS if option[0] in SAVED_OPTIONS])
        search = input(f"\nSaved options: {saved_options}\nSearch for:\n")

    # resolving full-name --option_name
    full_name_options = ''
    while '--' in search:
        end_pos = search.find('--') + 2
        while (end_pos < len(search) and search[end_pos] != ' '):
            end_pos += 1
        option = search[search.find('--') + 2:end_pos]
        search = search[:search.find('--')] + search[search.find('--') + 2 + len(option):]
        full_name_options += option[0] if option else ''

    # resolving short-name -options (e|r|t|i|k)
    short_options = ''
    while ' -' in search:
        end_pos = search.find(' -') + 2
        while (end_pos < len(search) and search[end_pos] != ' '):
            end_pos += 1
        option = search[search.find(' -') + 2:end_pos]
        search = search[:search.find(' -')] + search[search.find(' -') + 2 + len(option):]
        short_options += option

    if search and search[0] == '-':
        end_pos = 1
        while (end_pos < len(search) and search[end_pos] != ' '):
            end_pos += 1
        option = search[1 : end_pos]
        search = search[1 + len(option):]
        short_options += option

    options = short_options + full_name_options
    if not options:
        options = SAVED_OPTIONS
    if 'e' not in options and 'r' not in options and 't' not in options:
        options += 'e'

    # debug
    if debug:
        print(f"Args:        {sys.argv}")
        print(f"Search:      {search}")
        print(f"Short-name:  {short_options}")
        print(f"Full-name:   {full_name_options}")
        print(f"All options: {options}")
        return

    dicts  = []
    dicts += ENGLISH   if 'e' in options else []
    dicts += ROMANIAN  if 'r' in options else []
    dicts += [REVERSO] if 't' in options else []

    chrome_arg = '-incognito' if 'i' in options else ''
    if search and not search.isspace():
        dicts = " ".join([f'"{link.replace("{query}", search)}"' for link in dicts])
        subprocess.Popen(f'start chrome {chrome_arg} /new-window {dicts}', shell=True)
        print()
    else:
        print("\nEmpty search query, skipping links.")

    if 's' in options:
        print("Saved search options.")
        open(f'{HOMEPATH}/.opts', 'w').write("".join([option[0] for option in OPTIONS if option[0] in options]))

if __name__ == "__main__":
    main()
