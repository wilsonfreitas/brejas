# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from lxml import etree
import lxml.html

# Read in a page
site = 'http://www.brejas.com.br'
url = "http://www.brejas.com.br/cerveja"

# pages = range(1, 300)

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
for elm in root.cssselect(".jrRow"):
    if len(elm.cssselect('.jrContentTitle')) == 0:
        continue
    el = elm.cssselect('.jrContentTitle a')[0]
    cerva = {}
    cerva['nome'] = el.text_content().strip()
    cerva['url'] = '{0}{1}'.format(site, el.attrib['href'])
    el = elm.cssselect('.jrListingInfo')[0]
    cerva['pais'] = el.text.strip()
    el = elm.cssselect('.jrFieldRow.jrCervejaria .jrFieldValue a span')[0]
    cerva['cervejaria'] = el.text.strip()
    el = elm.cssselect('.jrFieldRow.jrEstilo .jrFieldValue a')[0]
    cerva['estilo'] = el.text.strip()
    el = elm.cssselect('.jrFieldRow.jrAlcool .jrFieldValue')[0]
    cerva['alcool'] = el.text.strip()
    el = elm.cssselect('.jrOverallRatings .jrOverallUser .jrRatingValue')[0]
    cerva['rating'] = el.text.strip()
    el = elm.cssselect('.jrOverallRatings .jrOverallUser .jrRatingValue .count')[0]
    cerva['rating_count'] = el.text.strip()
    
    html = scraperwiki.scrape(cerva['url'])
    el = lxml.html.fromstring(html)
    
    el = el.cssselect('.jrRatingTable')[0]
    print(etree.tostring(el))
    # el = el.cssselect('.jrRatingTable .jrRatingValue')[0]
    # print(el.text)


# Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
