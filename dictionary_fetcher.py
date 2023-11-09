import requests
from lxml import html

DEBUG_MODE = False  # True, open webpage file (offline). False, request url (online).

class CambridgeDictionaryFetcher:
    def __init__(self):
        self.word = None

    def fetch_webpage(self, url):
        """On success, return the webpage as HTML. On failure, return None."""
        if not DEBUG_MODE:
            HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"}
            webpage = requests.get(url, headers=HEADER)

            if webpage.status_code == 200:
                return webpage
            else:
                print(f"> fetch_webpage failed status code: {webpage.status_code}")
                return None

        else:  # Debug mode
            with open(r"C:\Users\guido\Desktop\translator\env\debug_site.html", "r", encoding="utf-8", ) as file:
                webpage = file.read()

            if webpage:
                return webpage
            else:
                print("> File is empty")
                return None

    def _fetch_html_dictionaries(self, html_object):
        """
        Fetch the dictionary elements from html_object.

        Parameters:
        -----------
            html_object (lxml.html.HtmlElement) :
        Returns:
        --------
            html_dictionarys (list) : list containing lxml.html.HtmlElement objects.
        """
        XPATH_QUERY_DICTIONARY = '(//div[contains(@class,"pr dictionary")])'
        html_dictionarys = html_object.xpath(XPATH_QUERY_DICTIONARY)

        return html_dictionarys

    def _fetch_html_dsenses(self, html_dictionary):
        """
        Parameters:
        -----------
            html_object (lxml.html.HtmlElement) :
        Returns:
        --------
            html_dsenses (list) : list containing lxml.html.HtmlElement objects.
        """
        XPATH_QUERY_DLINK = './/div[contains(@class,"pr dsense")]'  # get first word type (noun, verb, adjective or adverb.)
        html_dsenses = html_dictionary.xpath(XPATH_QUERY_DLINK)

        return html_dsenses

    def _fetch_html_definition_blocks(self, html_object):
        """
        Fetch the ddef_blocks from html_object.

        Parameters:
        -----------
            html_object (lxml.html.HtmlElement) :
        Returns:
        --------
            html_ddef_blocks (list) : list containing lxml.html.HtmlElement objects.
        """
        XPATH_QUERY_DDEF_BLOCK = ('.//div[contains(@class,"ddef_block")]')  # return all defintion blocks
        html_ddef_blocks = html_object.xpath(XPATH_QUERY_DDEF_BLOCK)  # if a word has only one type, then there is no dlink element.

        return html_ddef_blocks

    def _parse_definitions(self, html_ddef_blocks):
        """
        HTML parsing logic to extract the definition.

        Parameters:
        -----------
            html_ddef_blocks (lxml.html.HtmlElement) :

        Returns:
        --------
            str_defintions (str) :

        """
        XPATH_QUERY_DDEF_D = './/div[contains(@class,"ddef_d")]'
        html_ddef_ds = html_ddef_blocks.xpath(XPATH_QUERY_DDEF_D)  # find defintions
        str_defintions = "\n".join([" ".join(element.text_content().split()) for element in html_ddef_ds])

        return str_defintions

    def _parse_examples(self, html_ddef_blocks):
        XPATH_QUERY_DEXAMP = './/div[contains(@class, "dexamp")]'
        html_dexamps = html_ddef_blocks.xpath(XPATH_QUERY_DEXAMP)  # find examples
        str_examples = "\n".join([" ".join(element.text_content().split()) for element in html_dexamps])

        return str_examples

    def _parse_translations(self, html_ddef_blocks):
        XPATH_QUERY_DTRANS = './/span[@class="trans dtrans"]'
        html_dtrans = html_ddef_blocks.xpath(XPATH_QUERY_DTRANS)  # find translations
        str_translations = "\n".join([" ".join(element.text_content().split()) for element in html_dtrans])  # first .join() puts each distinct translation on a new line, the second removes all multiple white spaces from the html elemtn, which is first converted to text(means all syntax is stripped off).

        return str_translations

    def fetch_enLearner_dictionary(self, word):
        self.word = word
        self.url_enLearners = f"https://dictionary.cambridge.org/dictionary/learner-english//{self.word}"  # url Cambridge Learner dictionary EN
        self.url_en = f"https://dictionary.cambridge.org/dictionary/english/{self.word}"  # url Cambridge dictionary EN

        def_blocks = []

        webpage = self.fetch_webpage(self.url_enLearners)

        # redirect
        if not DEBUG_MODE:
            if webpage.url is not self.url_enLearners:
                webpage = self.fetch_webpage(self.url_en)

        if webpage == None:
            print("> fetch_dictionary failed because fetch_webpage failed")
            return []

        if not DEBUG_MODE:
            html_webpage = html.fromstring(webpage.content)
        else:
            html_webpage = html.fromstring(webpage)

        html_dictionarys = self._fetch_html_dictionaries(html_webpage)

        if html_dictionarys:
            html_dsenses = self._fetch_html_dsenses(html_dictionarys[0])  # use first dictionary
        else:
            html_dsenses = self._fetch_html_dsenses(html_webpage)

        for dsense in html_dsenses:
            html_ddef_blocks = self._fetch_html_definition_blocks(dsense)

            for block in html_ddef_blocks:
                definitions = self._parse_definitions(block)
                examples = self._parse_examples(block)
                translations = self._parse_translations(block)

                def_block = dict(Translations=translations,Definitions=definitions,Examples=examples,)  # create dictionary
                def_blocks.append(def_block)  # create a list of dictionaries, each dictionary contains one defintion block (a defintion block contains one of the word meanings)

        return def_blocks

    def fetch_en2nl_dictionary(self, word):
        pass

    def fetch_en_dictionary(self, word):
        self.word = word
        self.url_en2nl = f"https://dictionary.cambridge.org/dictionary/english-dutch/{self.word}"  # url Cambridge dictionary EN->NL
        self.url_en = f"https://dictionary.cambridge.org/dictionary/english/{self.word}"  # url Cambridge dictionary EN
        def_blocks = []

        html_webpage = self.fetch_webpage(self.url_en)

        if html_webpage == None:
            print("> fetch_dictionary failed because fetch_webpage failed")
            return None

        if len(html_webpage) == 0:
            print("> fetch_dictionary failed because html_webpage object is empty")
            return None

        else:
            html_dictionarys = self._fetch_html_dictionaries(html_webpage)

            if html_dictionarys:
                html_dsenses = self._fetch_html_dsenses(
                    html_dictionarys[0]
                )  # use first dictionary

                for dsense in html_dsenses:
                    html_ddef_blocks = self._fetch_html_definition_blocks(dsense)

                    for block in html_ddef_blocks:
                        definitions = self._parse_definitions(block)
                        examples = self._parse_examples(block)
                        translations = self._parse_translations(block)

                        def_block = dict(Translations=translations, Definitions=definitions, Examples=examples,)  # create dictionary
                        def_blocks.append(def_block)  # create a list of dictionaries, each dictionary contains one defintion block (a defintion block contains one of the word meanings)

        return def_blocks

    def print_dictionary(self, input):
        """
        Args:
        -----------
            input (dict) : this parameter must have the same type/structure as def_block or def_blocks in the fetch_dictionary().

        Returns:
        --------
            None
        """
        print("--------------------------")
        if type(input) is list:
            print(f"- Dictionary lookup: {self.word}")
            for i, def_block in enumerate(input):
                print(f"     Definition block {i}:")
                for key, value in def_block.items():
                    print(f"        {key}: {value}")

        elif type(input) is dict:
            print(f"- Dictionary lookup: {self.word}")
            print("     Definition block:")
            for key, value in input.items():
                print(f"        {key}: {value}")
        else:
            print("> Argument has the same type or is empty.")
