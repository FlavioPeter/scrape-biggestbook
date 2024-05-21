from termcolor import (
    colored,
)  # Make sure you have termcolor installed using pip if you're using this
from processing_functions import *


def main():
    ids = get_ids()
    count = 0
    total = len(ids)
    dir_path = "BiggestBook"
    create_dir(dir_path=dir_path)
    for id in ids:
        count += 1
        full_path = os.path.join(dir_path, id) + ".json"
        if not os.path.exists(full_path):
            try:
                json_data = get_json_data(id=id)
                json_data_formatted = format_json_data(json_data)
                export_to_json(full_path, json_data_formatted)
                print(colored(f"{count}/{total}: {id} | DOWNLOADED", "green"))
            except Exception as e:
                print(colored(f"{count}/{total}: {id} | COULD NOT DOWNLOAD", "red"))
                print(e)
        else:
            print(colored(f"{count}/{total}: {id} | ALREADY DOWNLOADED", "yellow"))


# This is required to run the async main function from the synchronous Python script entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("Processing interrupted", "magenta"))
