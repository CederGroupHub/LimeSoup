from LimeSoup.RSCSoup import RSCSoup
from LimeSoup.WileySoup import WileySoup
import pprint as pp


with open('LimeSoup/test/new_rsc_papers/101039b201206e.html', 'r') as f:
    html_str = f.read()
print(type(html_str))

with open('LimeSoup/test/wiley_papers/web_test_1.html', 'r') as f:
    html_str = f.read()
print(type(html_str))
data = WileySoup.parse(html_str)
#data = RSCSoup.parse(html_str)

pp.pprint(data['obj']['Keywords'])
pp.pprint(data['obj']['Title'])
print(data['obj']['DOI'])
print(data['obj']['Journal'])