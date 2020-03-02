import itertools
import re
import warnings
import bs4
import LimeSoup.parser.tools as tl


class ParserPaper:
    journal_name = None
    def __init__(self, raw_html, parser_type='lxml-xml', debugging=False):
        """
        :param raw_html:
        :param parser_type: can be 'html.parser', 'lxml', 'html5lib', 'lxml-xml'
        :param debugging: True or False
        """
        self.debugging = debugging
        # parsers 'html.parser', 'lxml', 'html5lib', 'lxml-xml'
        self.soup = bs4.BeautifulSoup('{:}'.format(raw_html), parser_type)
        self.parser_type = parser_type
        # self.journal_name = None
        self.title = []
        self.keywords = []
        self.data_sections = []
        self.headings_sections = []
        self.number_paragraphs_sections = []
        if debugging:
            self.soup_orig = self.soup

    def deal_with_sections(self):
        """
        Deal with the sections, parse tags that contains <'section_h#'>
        Ex: <'section_h2'>
        :return:
        """
        self.data_sections = []
        self.create_parser_sections(self.soup)

    @staticmethod
    def compile(pattern):
        return re.compile(pattern)

    def create_section(self, name='no_name_section', type_section='no_type', content=[]):
        return {
            'type': type_section
            , 'name': name
            , 'content': content
        }

    def create_parser_sections(self, soup):
        search_str = re.compile('section_h[1-6]')
        section_tags = soup.find_all(search_str)

        # Get all sections
        paras = []
        for tag in section_tags:
            try:
                name = tag.find('h{}'.format(tag.name[-1])).text.strip()
                name = name.replace('\n', '')
                name = ' '.join(name.split())
            except AttributeError:
                continue
            content = []
            for p in tag.find_all('div', class_='NLM_paragraph'):  # for some reason this is the paragraph tag/class that AIP uses for paragraphs
                p = p.getText()
                p = p.strip()
                p = re.sub(r'[\n] *', ' ', p)  # an embedded tag of named_content was adding in whitespaces which wouldn,'t strip but this solved the problem. These embedded tags couldn't be just thrown out because their text had relevant text to the paragraph they were imbedded in
                p = re.sub(r' {2,}', ' ', p)  # common for multiple named_content tags leading to the above line adding more than one space 
                content.append(p)
            if len(content) > 0:
                self.data_sections.append(self.create_section(
                    name=name,
                    type_section=tag.name,
                    content=content))

        
        # Nest data sections
        prev_texts = []
        for i in range(10, 1, -1):
            did_nest = False
            secname = "section_h{}".format(i)
            supersec_name = "section_h{}".format(i - 1)
            curr_sec_set = []
            for j, sec in enumerate(reversed(self.data_sections)):
                if sec['type'] == secname:
                    sec['content'] = [s for s in sec['content'] if s not in prev_texts]
                    prev_texts.extend([c for c in sec['content'] if type(c) == str])
                    curr_sec_set.insert(0, sec)
                elif (sec['type'] == supersec_name) and curr_sec_set:
                    for c in curr_sec_set:
                        curr = c['content']
                        for cu in curr:
                            if cu in sec['content']:
                                sec['content'].remove(cu)
                    for c in curr_sec_set:
                        sec['content'].append(c)
                    curr_sec_set = []
                    did_nest = True

            if did_nest:
                self.data_sections = [s for s in self.data_sections if s['type'] != 'section_h{}'.format(i)]
            else:
                self.data_sections = [s for s in self.data_sections if s['content'] != []]

    @staticmethod
    def create_soup(html_xlm, parser_type='html.parser'):
        # parser_types = ['html.parser', 'lxml', 'html5lib', 'lxml-xml']
        return bs4.BeautifulSoup(html_xlm, parser_type)

    def save_soup_to_file(self, filename='soup.html', prettify=True):
        """
        Save the soup to a file to be analysed. This can be used during the
        debugging process.
        :param filename: str that contain the name of the file
        :param prettify: boolean to add spaces on children tags
        :return: None - just save a file on disk
        """
        with open(filename, 'w', encoding='utf-8') as fd_div:
            if prettify:
                fd_div.write(self.soup.prettify())
                fd_div.write('\n')
            else:
                fd_div.write(str(self.soup))
                fd_div.write('\n')

    def get_title(self, rules):
        try:
            self.title = next(x for x in self.get(rules))
        except StopIteration:
            self.title = None

    def get(self, rules):
        results = list()
        for rule in rules:
            finds = self.soup.find_all(**rule)
            for item in finds:
                text = tl.convert_to_text(item.get_text())
                results.append(text)
                item.extract()
        return results

    def get_keywords(self, rules):
        self.keywords = []
        for rule in rules:
            for keyword in self.soup.find_all(**rule):
                self.keywords.append(tl.convert_to_text(keyword.get_text()))
                keyword.extract()
    
    def get_doi(self, rule={'name': 'ul', 'class': 'breadcrumbs'}):
        self.doi = ''
        try:
            breadcrumbs = self.soup.find(**rule)
            for li in breadcrumbs.find_all('li'):
                if '10.10' in li.getText():
                    doi = li.getText()
                    doi = re.sub(r'[\n] *', '', doi)
                    self.doi = doi
        except:
            pass
    
    def get_journal(self, rule={'name': 'ul', 'class': 'breadcrumbs'}):
        try:
            breadcrumbs = self.soup.find(**rule)
            count=0
            for li in breadcrumbs.find_all('li'):
                count+=1
                if count == 2:
                    journal = li.getText()
                    journal = re.sub(r'[\n] *>*', '', journal)
                    self.journal_name = journal
        except:
            pass



    def remove_tags(self, rules):
        """
        Remove tags from bs4 soup object using a list of bs4 rules to find_all()
        :param rules: list() of dict() of rules of bs4 find_all()
        :return: None
        """
        for rule in rules:
            [s.extract() for s in self.soup.find_all(**rule)]

    def remove_tag(self, rules):
        """
        Remove the first found tag from bs4 soup object using
        a list of bs4 rules to find_all() Remove the first tag.
        :param rules: rules: list() of dict() of rules of bs4 find_all()
        :return: None
        """
        for rule in rules:
            [s.extract() for s in self.soup.find_all(limit=1, **rule)]

    @property
    def headings_orig(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_heading_soup = self.soup_orig.find_all(name=re.compile('^h[1-6]$'))
        list_heading = []
        for item in list_heading_soup:
            list_heading.append(item.get_text())
        return list_heading

    @property
    def headings(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_heading_soup = self.soup.find_all(name=re.compile('^h[1-6]$'))
        list_heading = []
        for item in list_heading_soup:
            list_heading.append(tl.convert_to_text(item.get_text()))
        return list_heading

    @property
    def paragraphs(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_paragraphs_soup = self.soup.find_all('p', 'Para')  # re.compile(
        list_paragraphs = []
        for item in list_paragraphs_soup:
            if len(tl.convert_to_text(item.get_text())) != 0:
                item.string = tl.convert_to_text(item.get_text())
                list_paragraphs.append(item.get_text())
        return list_paragraphs

    @property
    def span(self):
        import copy
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        soup_one = copy.copy(self.soup)
        find_one1 = soup_one.find_all(name=re.compile('^h[1-6]$'))
        for e in find_one1:
            e.extract()
        find_one = soup_one.find_all(name=re.compile('span|p'), limit=1)
        list_paragraphs = []
        while len(find_one) != 0:
            text = tl.convert_to_text(find_one[0].get_text())
            if (find_one[0].name is not None) and (len(text) != 0):
                list_paragraphs.append(text)
            find_one[0].extract()
            find_one = soup_one.find_all(name=re.compile('span|p'), limit=1)
        return list_paragraphs

    @property
    def paragraphs_orig(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        list_paragraphs_soup = self.soup_orig.find_all(name=re.compile('p'))
        list_paragraphs = []
        for item in list_paragraphs_soup:
            list_paragraphs.append(item.get_text())
        return list_paragraphs

    def number_of_paragraphs_inside_parameters(self, parameters):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        soup_sec = self.soup_orig.find_all(parameters)
        number_of_paragraphs_soup_sec = 0
        for it in soup_sec:
            number_of_paragraphs_soup_sec += len(list(
                it.find_all('p', recursive=False)
            ))

    def number_of_paragraphs_children(self):
        if not self.debugging:
            warnings.warn('Debugging mode has to be True when call the class')
            return None
        number_of_paragraphs_children = len(list(list(
            self.soup_orig.children)[0].find_all('p', recursive=True)
                                                 ))
    
    def create_tag_from_selection(self, rule, name_new_tag, name_section='Abstract'):
        """
        Create a tag inside a bs4 soup object from a selection using a rule.
        :param rule: a dict() of rules of bs4 find_all()
        :param name_new_tag: new tag's name
        :param name_section: create a <h2> tag with the name_section content
        :return: None
        """
        inside_tags = self.soup.find_all(**rule)
        section = self.soup.new_tag('section_{}'.format(name_new_tag))
        heading = self.soup.new_tag('h2')
        heading.append(name_section)
        section.append(heading)
        for tag in inside_tags:
            tag.wrap(section)
            section.append(tag)

    def create_tag_to_paragraphs_inside_tag(self, rule, name_new_tag, name_section='Abstract'):
        inside_tags_inter = self.soup.find_all(**rule)
        if len(inside_tags_inter) == 0:
            # self.save_soup_to_file('selction_found_nothing.html')
            # input('Section not created, selection found nothing')
            return 'Section not created, number of paragraphs equal zero.'
        inside_tags = inside_tags_inter[0].find_all(re.compile('(p|ol)|span'), recursive=False)
        # inside_tags = inside_tags_inter[0].find_all('p', recursive=False)
        # inside_tags_ol = inside_tags_inter[0].find_all('ol', recursive=False)
        # inside_tags = inside_tags_p + inside_tags_ol
        if len(inside_tags) == 0:
            # self.save_soup_to_file('selction_found_nothing.html')
            # input('Section not created, number of paragraphs equal zero.')
            return 'Section not created, number of paragraphs equal zero.'
        section = self.soup.new_tag('section_{}'.format(name_new_tag))
        heading = self.soup.new_tag('h2')
        heading.append(name_section)
        section.append(heading)
        for tag in inside_tags:
            tag_next_sibling = tag
            while True:
                tag_next_sibling = tag_next_sibling.next_sibling
                if tag_next_sibling is None:
                    break
                if tag_next_sibling.name is None:
                    continue
                else:
                    break
            tag.wrap(section)
            section.append(tag)
            if tag_next_sibling is None: break
            if 'section_h' in tag_next_sibling.name:
                break

    def operation_tag_remove_space(self, rules):
        for rule in rules:
            tags = self.soup.find_all(**rule)
            for tag in tags:
                if tag is not None:
                    if tag.name is not None:
                        tag.string = tag.get_text().strip()

    def create_tag_sections(self, rule=None):
        """
        Create the standard tags (<section_#>) using a rule to bs4 find_all()
        :param rule:
        :return:
        """
        search_str = re.compile('NLM_sec_level_[2-6]')
        sub_sections = self.soup.find_all(class_=search_str)
        for s in sub_sections:
            s.contents[1].name = 'h'+str(int(s['class'][1][-1])+3)

        tag_names = ['h{}'.format(i) for i in range(1, 10)]
        for tag_name in tag_names:
            tags = self.soup.find_all(tag_name)  # Tags corresponded to headings
            for each_tag in tags:
                if each_tag.name == 'h4':
                    inside_tags = [x for x in each_tag.parent.next_siblings]
                else:  # this feels extremely hacky, but this is the simplist way if I am to build off the already established ParserPaper. Essentially after the h4 tag the same order for internal paragraphs is not followed so this is necessary
                    inside_tags = [x for x in each_tag.next_siblings]
                section = self.soup.new_tag('section_{}'.format(tag_name))
                each_tag.wrap(section)
                # for tag in inside_tags:
                if inside_tags:
                    for tag in inside_tags:
                        section.append(tag)

    def rename_tag(self, rule, new_name='section_h4'):
        tags = self.soup.find_all(**rule)
        for tag in tags:
            tag.name = new_name

    def strip_tags(self, rules):
        """
        Replace some tag with the children tag.
        :param rules: list of rules for bs4 find_all()
        :return: None
        """
        tags = list()
        for rule in rules:
            for tag in self.soup.find_all(**rule):
                tag.replace_with_children()
                tags.append(tag.name)
        return tags

    def change_name_tag_sections(self):
        tags = self.soup.find_all(re.compile('^h[2-6]'))
        for each_tag in tags:
            each_tag.parent.name = 'section_{}'.format(each_tag.name)

    @property
    def raw_html(self):
        return self.soup.prettify()

    def handle_lists(self):
        """
        This handles list so they show up as one paragraph and ensure that list elements do not get double counted as two paragraphs
        This function will extra the contents of a list, delete the list and then reinsert the list contents as separate paragraphs
        """
        # unordered lists (bulleted lists)
        list_tags = self.soup.find_all('table', class_='listgroup')
        for unordered_list in list_tags:
            paras_to_add = unordered_list.find_all('div', class_='NLM_paragraph')
            # paras_to_add.append(unordered_list.find_all('div', class_='Para'))
            parent_of_list = unordered_list.parent
            # parent_of_list.insert_after(para)
            for para in paras_to_add[::-1]:
                parent_of_list.insert_after(para)
            # unordered_list.extract()
        # Ordered lists (numbered lists)
        list_tags = self.soup.find_all('ol', class_='NLM_list-list_type-alpha-lower')
        for nlm_list in list_tags:
            paras_to_add = nlm_list.find_all('p')
            parent_of_list = nlm_list.parent
            for para in paras_to_add[::-1]:
                para.name='div'
                para['class']='NLM_paragraph'
                parent_of_list.insert_after(para)
        
        list_tags = self.soup.find_all('ul', class_='NLM_list-list_type-simple')
        for nlm_list in list_tags:
            paras_to_add = nlm_list.find_all('p')
            parent_of_list = nlm_list.previous_sibling
            for para in paras_to_add[::-1]:
                para.name='div'
                para['class']='NLM_paragraph'
                parent_of_list.insert_after(para)
    
    def create_tag_for_untitled_sections(self):
        """
        This function will create a section header for body paragraphs which are unlabelled. The name will be set to untitled
        """
        # first need to find paragraphs which do not belong to a section
        untitled_paras = []
        # this means the paragraph has no section header
        for para in self.soup.find_all('div', class_='NLM_paragraph'):
            check=True

            for tag in ['h{}'.format(str(i)) for i in range(1, 10)]:
                if tag in para.parent.name:
                    check = False
                    break
            try:
                if check:
                    for parent in para.parents:
                        if parent.name == 'div' and parent['class'] == ["hlFld-Fulltext"]:
                            untitled_paras.append(para)
                            break
            except:
                pass
        if len(untitled_paras)>0:
            untitled_paras[0].wrap(self.soup.new_tag('section'))
            untitled_paras[0].wrap(self.soup.new_tag('section_h4'))
            untitled_paras[0].wrap(self.soup.new_tag('div', class_='content'))
            newtag = self.soup.new_tag('h4', class_='Heading')
            newtag.append('Untitled')
            untitled_paras[0].parent.insert_before(newtag)
            for para in untitled_paras[1:]:
                untitled_paras[0].parent.append(para)