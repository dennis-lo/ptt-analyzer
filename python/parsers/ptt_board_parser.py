""" A parser that processes content of an index page.

Parsed content format:
    {
        title:          Title of the board
        page_num:       Current page number
        articles: {
            <page name>: {
                title:  Title of the article
                author: Author (user name) of the article
                date:   Published date of the article
            }
        }
        count:          Num of articles retrieved
    }
"""

import re

from .ptt_html_parser import PttHtmlParser

class PttBoardParser(PttHtmlParser):
    def __init__(self, parsed_content):
        super().__init__()

        # Pattern used to retrieve page name
        self.p_page_name = re.compile(r'^.*?\/([^\/]+)\]$')

        if parsed_content:
            # Update parsed content dict
            self.parsed_content = parsed_content

            # Update num of articles
            if 'count' in parsed_content:
                self.num_of_articles = parsed_content['count']

            else:
                self.num_of_articles = 0
        else:
            # Init num of articles
            self.num_of_articles = 0


    def handle_starttag(self, tag, attrs):
        """ Handles start-tag """
        super().handle_starttag(tag, attrs)

        # Reset page name if tag <div class="title"> is found
        if tag == 'div' and ('class', 'title') in attrs:
            self.page_name = None


    def handle_data(self, data):
        """ Stores parsed data into dictionary. """
        if bool(self.parsed_tags):
            if 'div[class=title]' in self.parsed_tags and \
                    self.parsed_tags[-1].startswith('a'):
                # Store article title and link
                self.add_article_title(data)

            elif 'div[class=author]' in self.parsed_tags:
                # Author
                self.add_article_author(data)

            elif 'div[class=date]' in self.parsed_tags:
                # Date
                self.add_article_date(data)

            elif 'title' in self.parsed_tags:
                # Store title
                self.set_title(data)

            elif data.endswith('上頁'):
                # Retrieve page number
                if self.parsed_tags[-1].startswith('a'):
                    self.set_page_num(self.parsed_tags[-1])


    def add_article_element(self, name, value, flagInit=False):
        """ Adds named value to article identified by page_name """
        if self.page_name and name and value:
            # Init dictionary if necessary
            if flagInit:
                self.parsed_content['articles'][self.page_name] = {}
            self.parsed_content['articles'][self.page_name][name] = value


    def add_article_author(self, author):
        """ Specifies author of the article """
        self.add_article_element('author', author)


    def add_article_date(self, date):
        """ Specifies date of the article """
        if date:
            self.add_article_element('date', date.strip())


    def add_article_title(self, title):
        """ Adds article title to list """
        # Initilize dictionary if necessary
        if 'articles' not in self.parsed_content:
            self.parsed_content['articles'] = {}

        # Retrieve page name
        m = self.p_page_name.match(self.parsed_tags[-1])
        if m:
            # Page name
            page_name = m.group(1)
            self.page_name = page_name

            # Increase num of articles by 1
            self.num_of_articles += 1
            self.parsed_content['count'] = self.num_of_articles

            # Initialize dict for the article
            self.add_article_element('title', title, True)


    def set_title(self, title):
        """ Stores the title of the board """
        self.parsed_content['title'] = title


    def set_page_num(self, element_name):
        """ Determines page number """
        # Match attributes with pattern
        m = re.match(r'^.*index(\d+)\.html\]$', element_name)

        # Store page number if retrieved successfully
        if m:
            self.parsed_content['page_num'] = int(m.group(1)) + 1

