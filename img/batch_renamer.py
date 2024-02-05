"""
Tool for batch renaming of multiple files in a folder
"""

import os

PREFIX = ''
START_COUNTER = 1
ZEROS = 5  # or None for auto


class Files:
    @staticmethod
    def rename():
        path = input('\033[36m' + f'Enter file path in which files are located:\n' + '\033[99m')
        files = [file for file in os.listdir(path)]
        nr_of_files = len(files)
        input('\033[93m' + f'{nr_of_files}' + '\033[36m' + ' file(s) found. Press ENTER to continue.' + '\033[99m')
        c = START_COUNTER
        nr_format = f'%0{len(str(nr_of_files)) if not ZEROS else ZEROS}d'  # trailing zeros
        for file in files:
            new_name = PREFIX + nr_format % c + file[-4:].lower()  # append file type ending (e.g. '.jpg')
            if file != new_name:
                os.rename(os.path.join(path, file), os.path.join(path, new_name))
            c += 1
        print('\033[36m' + 'Renaming complete!' + '\033[99m')


def main():
    Files.rename()


if __name__ == '__main__':
    main()
