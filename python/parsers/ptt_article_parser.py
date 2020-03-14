""" A parser that processes content of an article

Parsed content format:
    {
        title:              Title of the board
        page_num:           Current page number
        articles: {
            <page name>: {
                title:      Title of the article
                author:     Author (user name) of the article
                date:       Published date of the article
                content:    Content of the article
                comments: [ {
                    author:     Author (user name) of the comment
                    content:    Content of the coment
                    date:       Date of the comment
                } ]
            }
        }
        count:              Num of articles retrieved
    }
"""

from .ptt_html_parser import PttHtmlParser

class PttArticleParser(PttHtmlParser):
    def __init__(self, parsed_content, page_name: str = None):
        super().__init__()

        # Indicate whether it is necessary to process read content
        self.flag_process = True

        if parsed_content:
            # Update parsed content dict
            self.parsed_content = parsed_content

        if page_name:
            # Init page name
            self.page_name = page_name


    def add_article_element(self, name, value):
        """ Adds named value to article """
        if self.page_name and name and value:
            # Init dictionary if necessary
            if self.page_name not in self.parsed_content['articles']:
                self.parsed_content['articles'][self.page_name] = {}

            # Assign named value
            self.parsed_content['articles'][self.page_name][name] = value


    def append_article_element(self, name, value):
        """ Appends to named value of the article """
        if self.flag_process and self.page_name and name and value:
            # Init dictionary if necessary
            if self.page_name not in self.parsed_content['articles']:
                self.parsed_content['articles'][self.page_name] = {}

            # Init list if necessary
            if name not in self.parsed_content['articles'][self.page_name]:
                self.parsed_content['articles'][self.page_name][name] = []

            # Append to the end of list
            self.parsed_content['articles'][self.page_name][name].append(value)


    def handle_startendtag(self, tag, attrs):
        """ Stores properties of start-end-tags """
        if self.flag_process:
            if tag == 'link':
                if ('rel', 'canonical') in attrs:
                    dict_attrs = dict(attrs)
                    if 'herf' in dict_attrs:
                        # Page name
                        self.page_name = dict_attrs['href']

            elif tag == 'meta':
                if ('name', 'description') in attrs:
                    dict_attrs = dict(attrs)
                    if 'content' in dict_attrs:
                        # Content
                        self.add_article_element('content', \
                                dict_attrs['content'])


    def handle_starttag(self, tag, attrs):
        """ Stores properties of start-tags """
        if self.flag_process:
            super().handle_starttag(tag, attrs)

            # Reuse handle_startendtag()
            self.handle_startendtag(tag, attrs)


    def handle_endtag(self, tag):
        """ Looks for a certain types of end-tags """
        # Stop proceeding further if all comments have been processed
        if self.flag_process:
            if self.parsed_tags and \
                    self.parsed_tags[-1].startswith('div[id=main-content'):
                self.flag_process = False

        # Remove tag from stack
        super().handle_endtag(tag)


    def handle_data(self, data):
        """ Stores parsed data into dictionary. """
        if self.flag_process and self.parsed_tags:
            if self.parsed_tags:
                if 'div[class=push]' in self.parsed_tags:
                    if self.parsed_tags[-1].endswith('push-userid]'):
                        # Comment author
                        self.article_comment = {'author': data}

                    elif self.parsed_tags[-1].endswith('push-content]'):
                        # Comment
                        self.article_comment['content'] = data[2:]

                    elif self.parsed_tags[-1].endswith('datetime]'):
                        # Date time
                        self.article_comment['dateTime'] = data.strip()
                        self.append_article_element('comments', \
                                self.article_comment)

