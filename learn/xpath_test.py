import operator
from collections import namedtuple
from lxml import etree

fpath = r"like.html"
tree = etree.HTML(open(fpath).read())

#
hrefs = tree.xpath("/html/body/div[2]/div/center/div[@class='row']/div[1]/a/@href")
qualities = tree.xpath("/html/body/div[2]/div/center/div[@class='row']/div[2]/p/text()")
assert hrefs and "cannot find hrefs"
assert qualities and "cannot find qualities"
assert len(hrefs) == len(qualities) and "qualities count not equal to hrefs"

hrefs = tree.xpath("/html/body/div[2]/div/center/div[@class='row']/div[1]/a")
qualities = tree.xpath("/html/body/div[2]/div/center/div[@class='row']/div[2]/p")
assert hrefs and "cannot find hrefs"
assert qualities and "cannot find qualities"
assert len(hrefs) == len(qualities) and "qualities count not equal to hrefs"
hrefs = [i.attrib["href"] for i in hrefs]
qualities = [i.text for i in qualities]


Links = namedtuple("Links", ['width', 'height', "area", "href"])
links = []
for i in range(len(hrefs)):
    w, h = qualities[i].split(':')[0].strip().split('x')
    w = int(w)
    h = int(h)
    links.append(Links(w, h, w * h, hrefs[i]))
links.sort(key=operator.itemgetter(2), reverse=True)
print(links)
