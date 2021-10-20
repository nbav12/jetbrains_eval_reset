import time

from utils.eval_utils import handle_eval
from utils.fs_utils import find_products_dirs, choose_product_dir_manual, choose_specific_dirs
from utils.registry_utils import handle_reg
from utils.utils import close
from utils.xml_utils import handle_xml


def main():
    product_name = 'webstorm'
    product_dirs = find_products_dirs(product_name)

    if not product_dirs:
        print(f'[!] The {product_name} config dir can not be found. Please choose it manually')
        time.sleep(2)
        product_dirs.append(choose_product_dir_manual())
    elif len(product_dirs) > 1:
        product_dirs = choose_specific_dirs(product_dirs)

    handle_eval(product_dirs)
    handle_xml(product_dirs)
    handle_reg()

    print('\n[!] Done!')
    close()


if __name__ == '__main__':
    main()
