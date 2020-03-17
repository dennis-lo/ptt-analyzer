""" A module that retrieves content from PTT. """

import urllib.request

from . import boards
from parsers import parser
from parsers import merger

# Altered User-agent
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
}

def read_html_content(page_url: str) -> str:
    """ Retrieves content of the specified page

    Arguments:
        page_url -           Path to the page

    Returns -           Content of the page (decoded text)
    """
    # Return content
    ret_content = None

    # Create a request object to update headers
    req = urllib.request.Request(page_url, headers=REQUEST_HEADERS)

    # Retrieve content
    with urllib.request.urlopen(req) as resp:
        ret_content = resp.read().decode('utf-8')

    # Return result
    return ret_content


def read_index_page(board_name: str, page: int = None) -> str:
    """ Retrieves content of the index page of a board

    Arguments:
        board_name -    Name of the board
        page -          Page number

    Returns -           Content of the index page (decoded text)
    """
    # Return content
    ret_content = None

    # Retrieve URL of the index page
    page_url = boards.get_url(board_name, page=page)

    if page_url != None:
        ret_content = read_html_content(page_url)

    # Return result
    return ret_content


def read_article(board_name: str, article_path: str) -> str:
    """ Retrieves content of an article
    Arguments:
        board_name -    Name of the board
        article_path -  Relative path to the particle

    Returns -           Content of the article (decoded text)
    """
    # Return content
    ret_content = None

    # Retrieve URL of the article
    page_url = boards.get_url(board_name, article_path=article_path)

    if page_url != None:
        ret_content = read_html_content(page_url)

    # Return result
    return ret_content


def read_board(board_name: str, min_count: int = 30, start_date=None):
    """ Retrieves the list of articles from the specified board

    Arguments:
        board_name -    Name of the board
        min_count -     Min. num of articles should be retrieved
        start_date -    Date from which the search should begin

    Returns -           Parsed content (Please refer to individual parser for
                        detailed explanation)

    TODO:
        - Search with start_date
        - Search with period
    """
    # Return dictionary
    ret_content = {}

    # Page number
    page = None

    # Num of articles retrieved
    count_articles = 0

    # Continue until min num of articles is reached
    while count_articles < min_count:
        # Retrieve content
        page_content = read_index_page(board_name, page=page)

        # Parse HTML content
        if page_content != None:
            # Parse index page
            parsed_content = parser.parse_index(page_content)

            # Merge results
            merger.merge_index_pages(ret_content, parsed_content)

            # Update count
            count_articles = ret_content['count']

            # Update (previous) page number
            page = ret_content['page_num'] - 1

        else:
            # Exit loop
            break

    if ret_content and ret_content['articles']:
        # Retrieve articles
        for article_path in ret_content['articles'].keys():
            # Retrieve article content
            page_content = read_article(board_name, article_path)

            # Parse HTML content
            if page_content != None:
                # Parse article
                parsed_content = parser.parse_article(page_content, \
                        page_name=article_path)

                # Merge results
                merger.merge_article_content(ret_content['articles'], \
                        parsed_content)

    # Return parsed result
    return ret_content

