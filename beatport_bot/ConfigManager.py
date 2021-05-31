from configparser import ConfigParser
from typing import TextIO, List

from beatport_bot import beatport_csv


class ConfigManager:
    """
    Manager for the config file.
    """

    def __init__(self, config_filename="config.ini"):
        """
        Constructor for the ConfigManager.
        :param config_filename: The name of the config file
        """
        self.__config_filename: str = config_filename

        file: TextIO
        try:
            file = open(self.__config_filename, 'r')
        except FileNotFoundError:
            file = open(self.__config_filename, 'x')

        file.close()

        config: ConfigParser = ConfigParser()
        config.read(self.__config_filename)

        self.__chromedriver_file_path: str = '../chromedriver.exe'
        self.__url_file_path: str = '../Beatport URLs.csv'
        self.__save_file_path: str = '../Extract.csv'

        error_raised: bool = False

        try:
            self.chromedriver_file_path = config['DEFAULT']['chromedriver_path']
        except (KeyError, TypeError, ValueError):
            error_raised = True

        try:
            self.url_file_path = config['DEFAULT']['url_file_path']
        except (KeyError, TypeError, ValueError):
            error_raised = True

        try:
            self.url_file_path = config['DEFAULT']['url_file_path']
        except (KeyError, TypeError, ValueError):
            error_raised = True

        try:
            self.save_file_path = config['DEFAULT']['save_file_path']
        except (KeyError, TypeError, ValueError):
            error_raised = True

        if error_raised:
            self.__update_configuration_file()

    def __update_configuration_file(self):
        """
        Write config data to the config file
        """
        config = ConfigParser()
        config['DEFAULT']['chromedriver_path'] = self.__chromedriver_file_path
        config['DEFAULT']['url_file_path'] = self.__url_file_path
        config['DEFAULT']['save_file_path'] = self.__save_file_path

        configfile = open(self.__config_filename, 'w')
        config.write(configfile)
        configfile.close()

    @property
    def chromedriver_file_path(self) -> str:
        return self.__chromedriver_file_path

    @chromedriver_file_path.setter
    def chromedriver_file_path(self, chromedriver_file_path):
        if not isinstance(chromedriver_file_path, str):
            raise TypeError('file_path must be a string')

        invalid_characters: List[str] = ['<', '>', ':', '"', '|', '?', '*', '%']
        character: str
        if [character for character in invalid_characters if (character in chromedriver_file_path)]:
            raise ValueError('file_path cannot contain any of the following invalid characters: <, >, :, ", |, ?, *')

        self.__chromedriver_file_path = chromedriver_file_path
        self.__update_configuration_file()

    @property
    def url_file_path(self) -> str:
        """
        Getter for url_file_path
        :return: The file path for the URLs CSV
        """
        return self.__url_file_path

    @url_file_path.setter
    def url_file_path(self, url_file_path: str):
        """
        Setter for the url_file_path
        :param url_file_path: The file path for the URLs CSV
        """
        beatport_csv.validate_file_path(url_file_path)

        self.__url_file_path = url_file_path
        self.__update_configuration_file()

    @property
    def save_file_path(self) -> str:
        """
        Getter for the save_file_path
        :return: The file path for the save file CSV
        """
        return self.__save_file_path

    @save_file_path.setter
    def save_file_path(self, save_file_path: str):
        """
        Setter for the save_file_path
        :param save_file_path: The file path for the save file CSV
        """
        beatport_csv.validate_file_path(save_file_path)

        self.__save_file_path = save_file_path
        self.__update_configuration_file()
