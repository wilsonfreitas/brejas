# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from lxml import etree
import lxml.html
import textparser

class BrejasParser(textparser.NumberParser):
    def parseRating(self, text, match):
        r'^(\d+)\/(\d+)'
        return eval(match.group(1)), eval(match.group(2))

    def parseAlcool(self, text, match):
        r'^(\d+(\.\d+)?)% ABV'
        return float(match.group(1))/100

parser = BrejasParser()

def get_cerva(elm):
    cerva = {}
    el = elm.cssselect('.jrContentTitle a')[0]
    cerva['nome'] = el.text_content().strip()
    cerva['url'] = '{0}{1}'.format(site, el.attrib['href'])
    el = elm.cssselect('.jrListingInfo')[0]
    cerva['pais'] = el.text.strip()
    el = elm.cssselect('.jrFieldRow.jrCervejaria .jrFieldValue a span')[0]
    cerva['cervejaria'] = el.text.strip()
    el = elm.cssselect('.jrFieldRow.jrEstilo .jrFieldValue a')[0]
    cerva['estilo'] = el.text.strip()
    el = elm.cssselect('.jrFieldRow.jrAlcool .jrFieldValue')[0]
    cerva['alcool'] = parser.parse(el.text.strip())
    el = elm.cssselect('.jrOverallRatings .jrOverallUser .jrRatingValue')[0]
    cerva['rating'] = parser.parse(el.text.strip())
    el = elm.cssselect('.jrOverallRatings .jrOverallUser .jrRatingValue .count')[0]
    cerva['rating_count'] = parser.parse(el.text.strip())
    
    html = scraperwiki.scrape(cerva['url'])
    el = lxml.html.fromstring(html)
    el = el.cssselect('.jrReviewSummary .jrRatingTable')[1]
    # e_label = el.cssselect('.jrRatingTable .jrRatingLabel')[0]
    e_rating = el.cssselect('.jrRatingTable .jrRatingValue')[0]
    cerva['overall_rating'] = parser.parse(e_rating.text)
    for i in range(5):
        e_label = el.cssselect('.jrRatingTable .jrRatingLabel a')[i]
        e_rating = el.cssselect('.jrRatingTable .jrRatingValue')[i+1]
        rating = parser.parse(e_rating.text)
        lbl = e_label.text.lower()
        cerva[lbl] = rating[0]
        lbl_max = '%s_max' % lbl
        cerva[lbl_max] = rating[1]
    return cerva

# Read in a page
site = 'http://www.brejas.com.br'
url = "http://www.brejas.com.br/cerveja/?order=reviews"

for p in range(1, 223):
    _url = '{0}&page={1}'.format(url, p)
    print(_url)
    html = scraperwiki.scrape(_url)
    root = lxml.html.fromstring(html)
    for elm in root.cssselect(".jrRow"):
        if len(elm.cssselect('.jrContentTitle')) == 0:
            continue
        try:
            cerva = get_cerva(elm)
        except Exception as ex:
            n = elm.cssselect('.jrContentTitle a')[0].text_content().strip()
            print('Error:', n, ex.message)
        else:
            print(cerva['nome'])
            scraperwiki.sqlite.save(unique_keys=['nome', 'pais'], data=cerva)

