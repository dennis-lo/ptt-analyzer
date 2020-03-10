""" A module that helps parsing HTML content. """

from .ptt_board_parser import PttBoardParser
#from . import PttArticleParser

def parse_index(data, parsed_content={}):
    """ Returns information parsed from index page """
    # Parsed content
    return_dict = {}

    if data != None:
        # Create a parser object
        parser = PttBoardParser(parsed_content)

        # Parse HTML content
        return_dict = parser.parse(data)

    # Return parsed content
    return return_dict


def parse_article(data):
    """ Returns information parsed from an article """
    # Parsed content
    return_dict = {}

#    if data != None:
#        # Create a parser object
#        parser = PttArticleParser()
#
#        # Parse HTML content
#        return_dict = parser.parse(data)

    # Return parsed content
    return return_dict
