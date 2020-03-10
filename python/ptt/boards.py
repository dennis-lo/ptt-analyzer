""" A module that helps retrieve the mapped URL of a board. """

# Mappings from board name to URL
URL_MAPPINGS = {
    'Baseball': 'https://www.ptt.cc/bbs/Baseball/',
    'Chelsea': 'https://www.ptt.cc/bbs/Chelsea/',
    'Elephants': 'https://www.ptt.cc/bbs/Elephants/',
    'FAPL': 'https://www.ptt.cc/bbs/FAPL/',
    'SoftbankHawk': 'https://www.ptt.cc/bbs/SoftbankHawk/'
}

def get_url(name: str = None, page: int = None) -> str:
    """ Returns the mapped URL of the board """
    # Retrieved mapped URL
    return_url = URL_MAPPINGS.get(name)

    # Determine the path of the page under the mapped directory
    if return_url != None:
        if page != None:
            # Page number provided, insert
            return_url += 'index' + str(page) + '.html'

        else:
            # Page number not provided, visit index page directly
            return_url += 'index.html' 

    # Mapped URL
    return return_url

