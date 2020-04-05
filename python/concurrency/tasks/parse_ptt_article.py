""" A class that represents a task of parsing content of a certain format """

from .parse_content_task import ParseContentTask


class ParsePttArticle(ParseContentTask):
    def __init__(self, data: str, article_path: str):
        """ Instantiation

        Arguments:
            data -          Content to be parsed
            article_path -  Relative path to the article
        """
        super().__init__(data)
        self.article_path = article_path
