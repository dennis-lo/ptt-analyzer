""" A module that retrieves content from PTT. """

import urllib.request

from . import boards
from parsers import parser

def read_board(name: str, min_count: int = 30, start_date=None):
    """ Retrieves the list of articles from the specified board

    Arguments:
        name -          Name of the board
        min_count -     Min. num of articles should be retrieved
        start_date -    Date from which the search should begin

    Returns -           Parsed content (Please refer to individual parser for
                        detailed explanation)

    TODO:
        - Search with start_date
        - Search with period
    """
    # Return dictionary
    parsed_content = {}

    # Page number
    page = None

    # Num of articles retrieved
    count_articles = 0

    # Alter user-agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    }

    while count_articles < min_count:
        # Retrieve URL of the index page
        page_url = boards.get_url(name, page)
        print(page_url)

        # Retrieve content of the index page
        if page_url == None:
            # Failed to retrieve URL, exit loop
            break

        else:
            # Create a request object to update headers
            req = urllib.request.Request(page_url, headers=headers)

            # Retrieve content
            page_content = None
            with urllib.request.urlopen(req) as resp:
                page_content = resp.read().decode('utf-8')

            # Parse HTML content
            if page_content != None:
                parsed_content = parser.parse_index(page_content, \
                        parsed_content)

                # Update count
                count_articles = parsed_content['count']

                # Update (previous) page number
                page = parsed_content['page_num'] - 1

            else:
                # Exit loop
                break
        print(parsed_content)


