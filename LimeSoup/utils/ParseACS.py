from LimeSoup.ACSSoup import ACSSoup
import json
from bs4 import BeautifulSoup

# filename = "data/acs/ja016991d.xml"
# filename = "data/acs/acs.cgd.5b00741.xml"
# filename = "data/acs/acs.chemmater.7b01467.xml"
filename = "data/acs/cg701151m.xml"

with open(filename, "r", encoding="utf-8") as f:
    paper = f.read()

print ("-" == "-")

parsed_paper = ACSSoup.parse(paper)
data = parsed_paper["obj"]
print (data)

with open("data/acs/acs_parsed_paper.json", "w") as f:
    f.write(json.dumps(data, indent=2))

soup = BeautifulSoup(paper, "lxml")
print (soup.find_all(**{"name":"journal-title"}))