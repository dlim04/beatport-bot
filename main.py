from re import sub
from typing import List, Union, Any

from progressbar import progressbar
from selenium.common.exceptions import WebDriverException

from beatport_bot import beatport_csv
from beatport_bot.BeatportBot import BeatportBot
from beatport_bot.ConfigManager import ConfigManager


def boolean_input(prompt: str) -> bool:
    user_input: str = input(prompt + ' [y/n]\n')
    return user_input == 'y' or user_input == 'Y'


def main():
    config = ConfigManager()

    url_path_input: bool = False
    while not url_path_input:
        if boolean_input('Is "%s" the correct path for the URLs?' % config.url_file_path):
            url_path_input = True
        else:
            user_input: Any = input('Enter the new path for the URLs\n')
            try:
                beatport_csv.validate_file_path(user_input)
                file = open(user_input, 'r')
                file.close()
            except (TypeError, ValueError, FileNotFoundError) as error:
                print(error)
            else:
                config.url_file_path = user_input

    save_path_input: bool = False
    while not save_path_input:
        if boolean_input('Is "%s" the correct path for the save file?' % config.save_file_path):
            save_path_input = True
        else:
            user_input: Any = input('Enter the new path for the save file\n')
            try:
                beatport_csv.validate_file_path(user_input)
            except (TypeError, ValueError) as error:
                print(error)
            else:
                config.save_file_path = user_input

    data: List[List[Union[str, bool, int]]] = []
    urls: List[str] = beatport_csv.import_urls(config.url_file_path)
    beatport_bot: BeatportBot = BeatportBot(config.chromedriver_file_path)

    error_occurred: bool = False

    i: int
    url: str
    for i, url in enumerate(progressbar(urls)):
        try:
            label_data: List[Union[str, bool, int]] = [url, beatport_bot.get_record_label_name(url)]
            label_data.extend(beatport_bot.has_new_releases(url))
            data.append(label_data)
        except (KeyboardInterrupt, WebDriverException):
            error_occurred = True
            config.save_file_path = beatport_csv.write_csv(config.save_file_path, data)

            completed_urls: List[List[str]] = []

            j: int
            for j in range(i):
                completed_urls.append([urls[j]])

            uncompleted_urls: List[List[str]] = []

            for j in range(i, len(urls)):
                uncompleted_urls.append([urls[j]])

            trimmed_file_path: str = sub(r'.csv$', '', config.url_file_path)
            beatport_csv.write_csv('%s %s' % (trimmed_file_path, 'Completed.csv'), completed_urls)
            beatport_csv.write_csv('%s %s' % (trimmed_file_path, 'Uncompleted.csv'), uncompleted_urls)
            break

    if not error_occurred:
        config.save_file_path = beatport_csv.write_csv(config.save_file_path, data)

    print('\n\nCompleted %d of %d labels' % (i + 1, len(urls)))
    input('Press enter to exit...')


if __name__ == '__main__':
    main()
