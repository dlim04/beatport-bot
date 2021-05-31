import csv
from re import search, sub, Match
from typing import Optional, TextIO, List, Union


def validate_file_path(file_path: str) -> None:
    """
    Validate a file path for a CSV file. Raise an exception if the path is not valid.
    :param file_path: The file path to be validated
    """
    if not isinstance(file_path, str):
        raise TypeError('file_path must be a string')

    if not file_path.endswith('.csv'):
        raise ValueError("file_path must end with substring '.csv'")

    if file_path.count('.csv') != 1:
        raise ValueError("file_path must can only contain substring '.csv' once")

    invalid_characters: List[str] = ['<', '>', ':', '"', '|', '?', '*']
    character: str
    if [character for character in invalid_characters if (character in file_path)]:
        raise ValueError('file_path cannot contain any of the following invalid characters: <, >, :, ", |, ?, *')


def import_urls(file_path: str) -> List[str]:
    """
    Import a list of urls from a CSV file.
    :param file_path: The path the CSV file is located at
    :return: A list of URLs
    """
    validate_file_path(file_path)
    urls: List[str] = []
    file: TextIO = open(file_path, 'r', newline='')

    reader = csv.reader(file)

    row: List[str]
    for row in reader:
        urls.append(row[0])

    file.close()

    return urls


def write_csv(file_path: str, rows: List[List[Union[str, bool, int]]]) -> str:
    """
    Write data to a new CSV file. If the path is already taken add a number to the end of the path.
    :param file_path: The path to save the CSV file to
    :param rows: The data to write to the CSV
    :return: The file path the CSV was written to
    """
    validate_file_path(file_path)
    file_opened: bool = False
    file: TextIO

    while not file_opened:
        try:
            file = open(file_path, 'x', newline='')
            file_opened = True

        except FileExistsError:
            trimmed_file_path: str = sub(r'.csv$', '', file_path)
            count_match: Optional[Match] = search(r'\d+$', trimmed_file_path)

            if count_match is not None:
                trimmed_file_path = sub(r' \d+$', '', trimmed_file_path)

                file_count: int = int(count_match.group())
                file_count += 1

            else:
                file_count = 1

            file_path = '%s %d.csv' % (trimmed_file_path, file_count)

    writer = csv.writer(file)

    row: List[Union[str, bool, int]]
    for row in rows:
        try:
            writer.writerow(row)
        except UnicodeEncodeError:
            writer.writerow(["Name Could Not Be Described"])

    file.close()
    return file_path
