from typing import Tuple, List

from selenium import common, webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement


class BeatportBot:
    """
    @author - David Lim
    Bot to scrape label name and release information from https://www.beatport.com/
    """

    def __init__(self, chromedriver_path: str = 'chromedriver.exe'):
        self.service = Service(chromedriver_path)
        self.service.start()
        self.driver = webdriver.Remote(self.service.service_url)
        self.driver.maximize_window()

    def get_record_label_name(self, url: str) -> str:
        """
        Get a name of a record label from a given Beatport URL.
        :param url: The URL of a label page
        :return: The name of the label
        """
        self.driver.get(url)
        try:
            name = self.driver.find_element_by_class_name('interior-title').find_element_by_tag_name(
                'h1').get_attribute('textContent')
            return name
        except common.exceptions.NoSuchElementException:
            return "Page Not Found"

    def has_new_releases(self, url: str) -> Tuple[bool, int]:
        """
        Determine whether a label is currently active and the number of tracks they have from a given Beatport URL.
        :param url: The url of a label page
        :return: Whether the label is currently active and the number of tracks they have
        """
        new_release: bool = False
        self.driver.get(url + '/tracks?sort=release-desc')

        # Find all the tracks and store them in a list
        tracks: List[WebElement] = self.driver.find_elements_by_class_name('buk-track-meta-parent')

        track_years: List[int] = []
        counter: int = 0

        # Find the dates the latest two tracks were released at and store them in the track_years list
        track: WebElement
        for track in tracks:

            # Find the date the specific track was released
            track_date = track.find_element_by_class_name('buk-track-released').text

            # Add the year the track was created to the track_years list
            track_years.append(int(track_date[:4]))

            counter += 1
            if counter == 2:
                break

        twenty_nineteens: int = track_years.count(2019)
        twenty_eighteens: int = track_years.count(2018)
        count: int = twenty_nineteens + twenty_eighteens

        if len(track_years) != 0:
            if track_years[0] == 2020:
                new_release = True

            elif count == 2:
                new_release = True

        return new_release, len(tracks)
