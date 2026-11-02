from ConsoleListInterface import MenuInterface, moveCursor, cls
from termcolor import colored
from readchar import key
import subprocess
import yaml
import json
import sys
import os

HOMEPATH = os.path.dirname(os.path.realpath(__file__))
DATAPATH = f"{HOMEPATH}/data"
sys.stderr = open(f'{DATAPATH}/errors.txt', "a")


if not os.path.exists(f"{HOMEPATH}/options.yaml"):
    os.replace(f"{DATAPATH}/options_setup.yaml", f"{HOMEPATH}/options.yaml")

if not os.path.exists(f"{DATAPATH}/selected.json"):
    os.replace(f"{DATAPATH}/selected_setup.json", f"{DATAPATH}/selected.json")


KEEP_RUNNING = "Keep running after search"
QUIT_RUNNING = "Stop running after search"

def main():
    # direct search from command-line
    if '-s' in sys.argv or '--search' in sys.argv:
        clear = ('-c' in sys.argv or '--clear' in sys.argv)
        
        if clear:
            cls()
            moveCursor(max(int(os.get_terminal_size()[1] / 2) - 4, 0), 0)
        
        full_options = yaml.safe_load(open(f"{HOMEPATH}/options.yaml"))
        selected_options = json.load(open(f"{DATAPATH}/selected.json"))
        
        dicts = []
        args  = []

        # respecting order from HOMEPATH/options.yaml
        for option in [option for option in full_options if option in selected_options]:
            if isinstance(full_options[option], list):
                dicts += full_options[option]
            else:
                args.append(full_options[option])

        if not clear:
            print()
        print(f'{colored("Selected options", "light_blue")}: {", ".join([option for option in full_options if option in selected_options])}.\n')
        search = input(f'{colored("Search for", "light_blue")}: ').replace(' ', '+')
        print()

        chrome_arg = " ".join(args)

        if not search or search.isspace():
            return

        dicts = " ".join([dict.replace("{query}", search) for dict in dicts])

        subprocess.Popen(f'start chrome {chrome_arg} {dicts}', shell=True)
        
        return

    os.system('title Dictionaries')

    menu_structure = yaml.safe_load(open(f"{DATAPATH}/main_menu.yaml"))

    full_options = yaml.safe_load(open(f"{HOMEPATH}/options.yaml"))
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

        # ignoring backspace to main menu
        if not path:
            continue

        path = path[0]

        if path == "Search":
            # search(links, args)
            dicts = []
            args  = []

            # respecting order from HOMEPATH/options.yaml
            for option in [option for option in full_options if option in selected_options]:
                if isinstance(full_options[option], list):
                    dicts += full_options[option]
                else:
                    args.append(full_options[option])

            search = menu.separateInteraction(function=lambda: input(f'{colored("Selected options", "light_blue")}: {", ".join([option for option in full_options if option in selected_options])}.\n\n{colored("Search for", "light_blue")}: '), showCursor=True).replace(' ', '+')
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

            menu.separateInteraction(message=colored("Selection saved.\n", "light_blue"), waitInsteadOfEnter=0.5)
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
            

        if path in ["Exit", key.ESC, key.BACKSPACE]:
            menu.exitInterface()
            return


if __name__ == "__main__":
    main()
