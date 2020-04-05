""" A module that helps retrieve the mapped URL of a board. """

# Mappings from board name to URL
URL_MAPPINGS = {
    'Baseball': 'https://www.ptt.cc/bbs/Baseball/',
    'Chelsea': 'https://www.ptt.cc/bbs/Chelsea/',
    'Elephants': 'https://www.ptt.cc/bbs/Elephants/',
    'FAPL': 'https://www.ptt.cc/bbs/FAPL/',
    'SoftbankHawk': 'https://www.ptt.cc/bbs/SoftbankHawk/'
}


def get_url(name: str, page: int = None, article_path: str = None) -> str:
    """ Returns the mapped URL of the board

    Arguments:
        name -          Name of the board
        page -          Page number
        article_path -  Relative path to the article

    Returns -           Mapped URL of the (paged) board / article
    """
    # Retrieved mapped URL
    return_url = URL_MAPPINGS.get(name)

    # Determine the path of the page under the mapped directory
    if return_url is not None:
        if article_path is not None:
            # Article path provided, append
            return_url += article_path

        elif page is not None:
            # Page number provided, insert
            return_url += 'index' + str(page) + '.html'

        else:
            # Page number not provided, visit index page directly
            return_url += 'index.html'

    # Mapped URL
    return return_url
