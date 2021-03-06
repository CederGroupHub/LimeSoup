from synthesis_api_hub import api_method
from synthesis_api_hub.apiegg import APIEgg

from LimeSoup.ACSSoup import ACSSoup
from LimeSoup.AIPSoup import AIPSoup
from LimeSoup.APSSoup import APSSoup
from LimeSoup.ECSSoup import ECSSoup
from LimeSoup.ElsevierSoup import ElsevierSoup
from LimeSoup.NatureSoup import NatureSoup
from LimeSoup.RSCSoup import RSCSoup
from LimeSoup.SpringerSoup import SpringerSoup
from LimeSoup.WileySoup import WileySoup


class LimeSoupWorker(APIEgg):
    namespace = 'html_parser'

    @api_method
    def version_ecs(self):
        return ECSSoup.version

    @api_method
    def parse_ecs(self, html_string):
        return ECSSoup.parse(html_string)

    @api_method
    def version_rsc(self):
        return RSCSoup.version

    @api_method
    def parse_rsc(self, html_string):
        return RSCSoup.parse(html_string)

    @api_method
    def version_elsevier(self):
        return ElsevierSoup.version

    @api_method
    def parse_elsevier(self, html_string):
        return ElsevierSoup.parse(html_string)

    @api_method
    def version_springer(self):
        return SpringerSoup.version

    @api_method
    def parse_springer(self, html_string):
        return SpringerSoup.parse(html_string)

    @api_method
    def version_nature(self):
        return NatureSoup.version

    @api_method
    def parse_nature(self, html_string):
        return NatureSoup.parse(html_string)

    @api_method
    def version_wiley(self):
        return WileySoup.version

    @api_method
    def parse_wiley(self, html_string):
        return WileySoup.parse(html_string)

    @api_method
    def version_acs(self):
        return ACSSoup.version

    @api_method
    def parse_acs(self, html_string):
        return ACSSoup.parse(html_string)

    @api_method
    def version_aps(self):
        return APSSoup.version

    @api_method
    def parse_aps(self, html_string):
        return APSSoup.parse(html_string)

    @api_method
    def version_aip(self):
        return AIPSoup.version

    @api_method
    def parse_aip(self, html_string):
        return AIPSoup.parse(html_string)
