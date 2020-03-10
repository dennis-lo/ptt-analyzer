""" A parser that processes HTML content retrieved from PTT. """

from html.parser import HTMLParser

class PttHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parsed_tags = []
        self.parsed_content = {}


    def handle_starttag(self, tag, attrs):
        """ Handles start-tag

        Appends tag to the end of list and checks whether further processing is
        required.
        """
        # Construct element name with attributes
        element_name = tag
        attr_str = ''

        if bool(attrs):
            for pair in attrs:
                if bool(pair[0] and pair[1]):
                    # Append separator or bracket
                    if bool(attr_str):
                        attr_str += ','
                    else:
                        attr_str += '['

                    # Append name and value
                    attr_str += pair[0] + '=' + pair[1]

            # Append bracket
            if bool(attr_str):
                attr_str += ']'

        # Append attributes
        element_name += attr_str

        # Append name to list
        self.parsed_tags.append(element_name)


    def handle_endtag(self, tag):
        """ Pops last parsed element if it matches the end-tag """
        if bool(self.parsed_tags):
            if self.parsed_tags[-1].startswith(tag):
                self.parsed_tags.pop()


    def parse(self, data : str):
        """ Returns parsed information. """
        # Feed text to parser
        if data != None:
            super().feed(data)

        # Returned parsed data
        return self.parsed_content

