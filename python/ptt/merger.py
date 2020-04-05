""" A module that merges dictionaries parsed from HTML content.

TODO:
    - Move this module to a better location (difficulty naming the directory)
"""

# Dictionary key for list-of-articles
KEY_ARTICLES = 'articles'

# Dictionary key for article-comments
KEY_COMMENTS = 'comments'

# Dictionary key for article-content
KEY_CONTENT = 'content'

# Dictionary key for num-of-articles
KEY_COUNT = 'count'

# Dictionary key for name
KEY_NAME = 'name'

# Dictionary key for page-number
KEY_PAGE_NUM = 'page_num'

# Dictionary key for board-title
KEY_BOARD_TITLE = 'title'


def merge_index_pages(src_index, in_index):
    """ Merges parsed content of two different index pages.

    Arguments:
        src_index - Base dictionary into which the input will be merged
        in_index -  Input dictionary whose content will be merged into src_dict
    """
    if src_index is not None and in_index:
        # Assign board name
        if KEY_NAME not in src_index:
            src_index[KEY_NAME] = in_index.get(KEY_NAME)

        # Assign board title
        if KEY_BOARD_TITLE not in src_index:
            src_index[KEY_BOARD_TITLE] = in_index.get(KEY_BOARD_TITLE)

        # Update page name
        if in_index.get(KEY_PAGE_NUM):
            src_index[KEY_PAGE_NUM] = in_index.get(KEY_PAGE_NUM)

        # Init dict if necessary
        if KEY_ARTICLES not in src_index:
            src_index[KEY_ARTICLES] = {}

        # List of articles to be merged into base
        in_articles = in_index.get(KEY_ARTICLES)

        # Merge list of articles
        if in_articles is not None:
            for page_name in in_articles.keys():
                if in_articles[page_name]:
                    src_index[KEY_ARTICLES][page_name] = in_articles[page_name]

        # Update num of articles
        if KEY_ARTICLES in src_index:
            src_index[KEY_COUNT] = len(src_index[KEY_ARTICLES])

        else:
            src_index[KEY_COUNT] = 0


def merge_article_content(src_articles, in_article):
    """ Merges parsed article content to provided list.

    Arguments:
        src_articles -  List of articles into which the content will be merged
        in_article -    Parsed content of an article
    """
    if src_articles is not None and in_article:
        for page_name in in_article.keys():
            # Article content
            dict_article = in_article[page_name]

            # Assign article content
            if KEY_CONTENT in dict_article:
                src_articles[page_name][KEY_CONTENT] = \
                        dict_article.get(KEY_CONTENT)

            # Assign article comments
            if KEY_COMMENTS in dict_article:
                src_articles[page_name][KEY_COMMENTS] = \
                        dict_article.get(KEY_COMMENTS)
