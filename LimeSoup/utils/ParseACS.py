from LimeSoup.ACSSoup import ACSSoup
import json


with open("data/acs/acs.cgd.5b00741.xml", "r", encoding="utf-8") as f:
    paper = f.read()

parsed_paper = ACSSoup.parse(paper)
data = parsed_paper
print (data)
