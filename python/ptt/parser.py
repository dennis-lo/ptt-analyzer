""" A module that helps parsing HTML content. """

from parsers.ptt_board_parser import PttBoardParser
from parsers.ptt_article_parser import PttArticleParser


def parse_index(data: str):
    """ Returns information parsed from the content of an index page """
    # Parsed content
    return_dict = {}

    if data is not None:
        # Create a parser object
        parser = PttBoardParser()

        # Parse HTML content
        return_dict = parser.parse(data)

    # Return parsed content
    return return_dict


def parse_article(data: str, page_name: str = None):
    """ Returns information parsed from the content of an article """
    # Parsed content
    return_dict = {}

    if data is not None:
        # Create a parser object
        parser = PttArticleParser(page_name)

        # Parse HTML content
        return_dict = parser.parse(data)

    # Return parsed content
    return return_dict
