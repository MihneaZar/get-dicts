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
        # selected dictionary entry and chrome arguments
        selected = json.load(open(f"{DATAPATH}/selected.json"))
        selected_dict = selected["dict"]
        selected_args = selected["args"]
        
        dicts = full_options[selected_dict]
        args  = []
        for arg in selected_args:
            args.append(full_options[arg])

        if not clear:
            print()
        print(f'{colored("Selected dictionary", "light_blue")}: {selected_dict}.\n{colored("Selected arguments", "light_blue")}: {", ".join([arg for arg in full_options if arg in selected_args])}.\n')
        search = input(f'{colored("Search for", "light_blue")}: ').replace(' ', '+')
        print()

        chrome_arg = " ".join(args)

        if not search or search.isspace():
            return

        dicts = " ".join([dict.replace("{query}", search) for dict in dicts])

        subprocess.Popen(f'start chrome {chrome_arg} {dicts}', shell=True)
        
        return
    # command-line search end

    os.system('title Dictionaries')

    menu_structure = yaml.safe_load(open(f"{DATAPATH}/main_menu.yaml"))

    # full options.yaml (python dict with the dictionary links and the actual chrome args)
    full_options = yaml.safe_load(open(f"{HOMEPATH}/options.yaml"))
    # getting option names in the order of options.yaml
    options = [option for option in full_options if option and option[0] != '_' and full_options[option]]

    # list of all dict entries
    all_dicts = [dict for dict in options if isinstance(full_options[dict], list)]

    # list of all arg entries
    all_args = [arg for arg in options if isinstance(full_options[arg], str)]

    # selected dictionary entry and chrome arguments
    selected = json.load(open(f"{DATAPATH}/selected.json"))
    selected_dict = selected["dict"]
    selected_args = selected["args"]

    max_option = max([len(option) for option in options])

    option_dict = {}
    for option in options:
        # + 2 for the " x" part
        selected_text = f"{'x':>{max_option - len(option) + 2}}" if option in [selected_dict] + selected_args else ""
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
            dicts = full_options[selected_dict]
            args  = []
            for arg in selected_args:
                args.append(full_options[arg])
            
            search_prompt  = f'{colored("Selected dictionary", "light_blue")}: {selected_dict}.\n'
            search_prompt += f'{colored("Selected arguments", "light_blue")}: {", ".join([arg for arg in full_options if arg in selected_args])}.\n\n'''
            search_prompt += f'{colored("Search for", "light_blue")}: '
            search = menu.separateInteraction(function=lambda: input(search_prompt), showCursor=True).replace(' ', '+')
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
                json.dump({"dict": selected_dict, "args": selected_args}, file, ensure_ascii=False, indent=4)

            menu.separateInteraction(message=colored("Selection saved.\n", "light_blue"), waitInsteadOfEnter=0.5)
            continue


        if path[0] == "'":
            new_option = path[1:path.find("'", 1)]

            # reselecting the same dictionary is ignored
            if new_option == selected_dict:
                continue

            if new_option in all_dicts and new_option != selected_dict: 
                # single option for dicts (only one dict can be selected at a time)
                changes = MenuInterface.selectOption(f"'{selected_dict}'", f"'{new_option}'", [f"'{dict}'" for dict in all_dicts], 
                                                     'x', maxOptionLength=max_option+2) # + 2 for the quotes ''

                selected_dict = new_option

            if new_option in all_args:
                # multiple options for args (multiple args can be selected at the same time)
                changes = MenuInterface.selectMultipleOptions([f"'{arg}'" for arg in selected_args], f"'{new_option}'", 
                                                              [f"'{arg}'" for arg in all_args], 'x', maxOptionLength=max_option+2) # + 2 for the quotes ''

                # selecting option
                if new_option not in selected_args:
                    selected_args.append(new_option)
                # deselecting option
                else:
                    selected_args.remove(new_option)

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
