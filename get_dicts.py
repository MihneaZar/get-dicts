from ConsoleListInterface import MenuInterface
import subprocess
import yaml
import json
import sys
import os

HOMEPATH = os.path.dirname(os.path.realpath(__file__))
DATAPATH = f"{HOMEPATH}/data"
sys.stderr = open(f'{DATAPATH}/errors.txt', "a")


if not os.path.exists(f"{HOMEPATH}/options.json"):
    os.replace(f"{HOMEPATH}/options_setup.json", f"{HOMEPATH}/options.json")

if not os.path.exists(f"{DATAPATH}/selected.json"):
    os.replace(f"{DATAPATH}/selected_setup.json", f"{DATAPATH}/selected.json")


KEEP_RUNNING = "Keep running after search"
QUIT_RUNNING = "Stop running after search"

def main():
    os.system('title Dictionaries')

    menu_structure = yaml.safe_load(open(f"{DATAPATH}/main_menu.yaml"))

    full_options = json.load(open(f"{HOMEPATH}/options.json"))
    options = [option for option in full_options if option and option[0] != '_']
    selected_options = json.load(open(f"{DATAPATH}/selected.json"))

    max_option = max([len(option) for option in options])

    option_dict = {}
    for option in options:
        selected_text = f"{'x':>{max_option - len(option) + 2}}" if option in selected_options else ""
        option_dict[f"'{option}'{selected_text}"] = None

    exit_on_search = True

    menu = MenuInterface(menu_structure, dontPrintMenu=True)

    menu.addOptions([], option_dict, "options")
    menu.removeOptions([], ["options"])

    while True:
        path = menu.interactWithMenu()

        # ignoring backspace
        if not path:
            continue

        path = path[0]

        if path == "Search":
            # search(links, args)
            dicts = []
            args  = []

            for option in selected_options:
                if isinstance(full_options[option], list):
                    dicts += full_options[option]
                else:
                    args.append(full_options[option])

            search = menu.separateInteraction(function=lambda: input("Search for: "), showCursor=True).replace(' ', '+')
            chrome_arg = " ".join(args)

            if not search or search.isspace():
                continue

            dicts = " ".join([dict.replace("{query}", search) for dict in dicts])

            subprocess.Popen(f'start chrome {chrome_arg} {dicts}', shell=True)

            if exit_on_search:    
                menu.exitInterface()
                return
            
            continue
        
        if path == "Save selection":
            with open(f"{DATAPATH}/selected.json", 'w', encoding="utf-8") as file:
                json.dump(selected_options, file, ensure_ascii=False, indent=4)

            menu.separateInteraction(message="Selection saved.\n")
            continue


        if path[0] == "'":
            new_option = path[1:path.find("'", 1)]

            changes = MenuInterface.selectMultipleOptions([f"'{option}'" for option in selected_options], f"'{new_option}'", [f"'{option}'" for option in options], 'x')
            
            # selecting option
            if new_option not in selected_options:
                selected_options.append(new_option)
            # deselecting option
            else:
                selected_options.remove(new_option)

            menu.changeOptionNames([], changes)
            continue


        if path in [KEEP_RUNNING, QUIT_RUNNING]:
            changes = {}
            if path == KEEP_RUNNING:
                changes[KEEP_RUNNING] = QUIT_RUNNING
            else:
                changes[QUIT_RUNNING] = KEEP_RUNNING
            
            exit_on_search = not exit_on_search
            menu.changeOptionNames([], changes)
            

        if path == "Exit":
            menu.exitInterface()
            return

    return

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
