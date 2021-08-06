import time
import os
import sys
import shutil
import winreg
import xml.etree.ElementTree as Et

# Environment variables
APP_DATA_PATH = os.environ.get('APPDATA')
HOME_PATH = os.path.join(os.environ.get('HOMEDRIVE'), os.environ.get('HOMEPATH'))

# Registry path
WEBSTORM_REG_PATH = r'SOFTWARE\JavaSoft\Prefs\Jetbrains\webstorm'


def find_webstorm_dirs():
    webstorm_dirs = []

    # Trying get with 2020.1 and above versions
    jetbrains_dir = os.path.join(APP_DATA_PATH, 'Jetbrains')

    if os.path.exists(jetbrains_dir):
        for directory in os.listdir(jetbrains_dir):
            if directory.lower().startswith('webstorm'):
                webstorm_dirs.append(os.path.join(jetbrains_dir, directory))

    # Trying get with 2019.3.x and below versions
    for directory in os.listdir(HOME_PATH):
        if 'webstorm' in directory.lower():
            webstorm_dir = os.path.join(HOME_PATH, directory)

            if 'config' in os.listdir(webstorm_dir):
                webstorm_dirs.append(os.path.join(webstorm_dir, 'config'))

    return webstorm_dirs


def find_eval_dirs(webstorm_dirs):
    eval_dirs = []

    for directory in webstorm_dirs:
        if 'eval' in os.listdir(directory):
            eval_dirs.append(os.path.join(directory, 'eval'))

    return eval_dirs


def remove_eval_dirs(eval_dirs):
    for directory in eval_dirs:
        shutil.rmtree(directory)
        print(f'[+] evl dir {directory} has been removed')


def handle_eval(webstorm_dirs):
    print('\n[!] Eval dir')
    eval_dirs = find_eval_dirs(webstorm_dirs)

    if not eval_dirs:
        return print('[!] Can not find any eval dir. Skipping')

    remove_eval_dirs(eval_dirs)


def find_options_dirs(webstorm_dirs):
    options_dirs = []

    for directory in webstorm_dirs:
        if 'options' in os.listdir(directory):
            options_dirs.append(os.path.join(directory, 'options'))

    return options_dirs


def remove_xml_elements(options_dirs):
    xml_files = ('options.xml', 'other.xml')

    for options_dir in options_dirs:
        for file in xml_files:
            xml_path = os.path.join(options_dir, file)

            try:
                tree = Et.parse(xml_path)
                print(f'[+] XML file: {xml_path} found. Handling')
            except FileNotFoundError:
                continue

            root = tree.getroot()

            # Filter the component element of the properties by checking "name" attribute
            properties_component = \
                tuple(filter(lambda el: el.get('name') == 'PropertiesComponent', root.findall('component')))[0]

            for element in properties_component[:]:
                if element.get('name').startswith('evl'):
                    properties_component.remove(element)
                    print(f"[+] {element.get('name')} element has been removed")

            # Saving xml file and break, because the desired file has been found
            tree.write(xml_path)
            break


def handle_xml(webstorm_dirs):
    print('\n[!] XML file')
    options_dirs = find_options_dirs(webstorm_dirs)

    if not options_dirs:
        print('[!] Can not find any options dir. Skipping')

    remove_xml_elements(options_dirs)


def handle_reg():
    print('\n[!] Registry')

    # Running over all sub keys of "webstorm" key and delete their subs and themself
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, WEBSTORM_REG_PATH) as webstorm_key:
            webstorm_sub_keys_names = [winreg.EnumKey(webstorm_key, sub_key_index)
                                       for sub_key_index in range(winreg.QueryInfoKey(webstorm_key)[0])]

            for sub_key_name in webstorm_sub_keys_names:
                with winreg.OpenKey(webstorm_key, sub_key_name) as sub_key:
                    delete_sub_keys(sub_key)
                    print(f'[+] {sub_key_name} key has been removed')
    except FileNotFoundError:
        print(f'[!] {WEBSTORM_REG_PATH} registry can not be found. Skipping')
    except PermissionError:
        print(f'[-] There is not permission for {WEBSTORM_REG_PATH} registry ')


def delete_sub_keys(key):
    """
    Because it is impossible to delete key with sub keys, there is a need to delete the sub keys recursively.
    After that, delete the root key itself.
    :param key: The desired root key delete its sub keys
    :return: None
    """
    sub_keys_amount = winreg.QueryInfoKey(key)[0]

    for sub_key_index in range(sub_keys_amount):
        sub_key_name = winreg.EnumKey(key, 0)

        try:
            winreg.DeleteKey(key, sub_key_name)
            print(f'[+] {sub_key_name} key has been removed')
        except PermissionError:
            delete_sub_keys(winreg.OpenKey(key, sub_key_name))

    winreg.DeleteKey(key, '')


def choose_webstorm_dir_manual():
    from tkinter import filedialog, Tk

    root = Tk()
    root.withdraw()

    webstorm_dir = filedialog.askdirectory(title='Choose Webstorm config folder')

    if not webstorm_dir:
        print('[!] No folder selected. Exiting')
        close()

    return webstorm_dir


def choose_specific_webstorm_dir(webstorm_dirs):
    print(f'[!] {len(webstorm_dirs)} dirs have been found.')
    print('\tWhich of them do you want to reset?')

    for i, directory in enumerate(webstorm_dirs):
        print(f'\t\t{i + 1} - {directory}')
    print(f'\t\t{i + 2} - All')

    user_choose = input('\tYour choose: ')
    while not is_valid_choose(user_choose, 1, len(webstorm_dirs) + 1):
        user_choose = input('\tYour choose: ')

    if int(user_choose) <= len(webstorm_dirs):
        return [webstorm_dirs[int(user_choose) - 1]]

    return webstorm_dirs


def is_valid_choose(choose, min_value, max_value):
    try:
        user_choose = int(choose)

        return min_value <= user_choose <= max_value
    except ValueError:
        return False


def close():
    os.system('pause')
    sys.exit(0)


def main():
    webstorm_dirs = find_webstorm_dirs()

    if not webstorm_dirs:
        print('[!] The Webstorm config dir can not be found. Please choose it manually')
        time.sleep(2)
        webstorm_dirs.append(choose_webstorm_dir_manual())
    elif len(webstorm_dirs) > 1:
        webstorm_dirs = choose_specific_webstorm_dir(webstorm_dirs)

    handle_eval(webstorm_dirs)
    handle_xml(webstorm_dirs)
    handle_reg()

    print('\n[!] Done!')
    close()


if __name__ == '__main__':
    main()
