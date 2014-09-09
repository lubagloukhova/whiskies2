__author__ = 'lubagloukhov'

from urllib import urlopen
import sys
import bs4

from pandas import DataFrame
from pandas import Series
import pandas as pd


import types as types

####################################################################
# UTILITY FUNCTIONS
####################################################################

# Given page URL with table (http://www.whiskybase.com/brand/81358),
# get links of all paginations to follow
def whiskPages(url):

    html = urlopen(url).read()
    soup = bs4.BeautifulSoup(html)

    table = soup.find("div", {"class" : "pagination"})

    links = table.findAll("a", href=True)
    linkbase = [l["href"] for l in links]
    lbase = url + "?page="
    lend = "" #"&sort=bottle_date&direction=desc"
    pages = [(l.get_text().encode('ascii', 'ignore')) for l in links]

    for i in range(len(pages)):
        try:
            pages[i] = int(pages[i] )
        except:
            del pages[i]

    pages=range( min(pages),max(pages)+1)

    links = [lbase + str(pages[l]) + lend for l in range(len(pages))]
    return links

# Get Links to top Brands from table page.
def distLinks(url):

    #url = url + "?brandname[]=&sort=votes&direction=desc" # redefine url to that of page sorted by vote count
    html = urlopen(url).read()
    soup = bs4.BeautifulSoup(html)

    # [div['class'] for div in soup.find_all('table')]
    # for tag in soup.find_all("table", {"class" : re.compile("whisky")}): # find all tag contains t
    #     print tag
    # subsoup = soup.find("div", {"id" : "distillery-whiskies"})

    table = soup.find("table", {"class" : re.compile("whisky")})

    rows = table.findAll('tr')

    header = rows[0]
    headeris = header.findAll('th')
    headeris=map(lambda x:  " ".join(x.get_text().encode('ascii', 'ignore').split()), headeris)

    rows = rows[1:] # exclude header
    cols = [tr.findAll('td') for tr in rows]

    datasets = [dict(zip(['url']+headeris, [c[1].find("a", href=True)['href']] + map(lambda x:  " ".join(x.get_text().encode('ascii', 'ignore').split()), c) )) for c in cols]

    for sub in datasets:
        for key in sub:
            try:
                sub[key] = int(sub[key])
            except:
                try:
                    sub[key] = float(sub[key])
                except:
                    try:
                        sub[key] = float(sub[key].strip('%'))/100
                    except:
                        pass


    return datasets

# Given a Brand url page (http://www.whiskybase.com/brand/81358?page=41) or (http://www.whiskybase.com/brand/81358),
# obtain links to individual whiskies
def whiskLinks(url):

    url = url + "?sort=bottle_date&direction=desc"
    html = urlopen(url).read()
    soup = bs4.BeautifulSoup(html)

    table = soup.find("table", {"class" : "whiskytable table table-sortable"})

    rows = table.findAll('tr')

    header = rows[0]
    headeris = header.findAll('th')
    headeris=map(lambda x:  " ".join(x.get_text().encode('ascii', 'ignore').split()), headeris)

    rows = rows[1:] # exclude header
    cols = [tr.findAll('td') for tr in rows]

    datasets = [dict(zip(['url']+headeris, [c[1].find("a", href=True)['href']] + map(lambda x:  " ".join(x.get_text().encode('ascii', 'ignore').split()), c) )) for c in cols]

    for sub in datasets:
        for key in sub:
            try:
                sub[key] = int(sub[key])
            except:
                try:
                    sub[key] = float(sub[key])
                except:
                    try:
                        sub[key] = float(sub[key].strip('%'))/100
                    except:
                        pass


    datasetS = datasets
    return datasetS

# GIVEN A URL OF ALL WHISKY REVIEWS, GET LIST OF URLS OF SPECIFIC WHISKY PAGES
def linkList(url):
    html = urlopen(url).read()

    soup = bs4.BeautifulSoup(html)
    list = soup.find_all("div", {"class" : "note-whisky"})
    linkList = [x.find("a", href=True)['href'] for x in list]
    return linkList

# GIVEN A URL OF SPECIFIC WHISKY PAGE, GET DATA INFO RETURNED AS A DICT
def dataDict(url): #isinstance(x, types.NoneType)
    html = urlopen(url).read()
    soup = bs4.BeautifulSoup(html)
    table = soup.find("table", {"class" : "datalist"})

    # if type(table) is not 'NoneType':
    if isinstance(table, types.NoneType):
        dataDict = {'Age': "-", 'Bottled': "-", 'Bottler': "-", 'Category': "-",  'District': "-",
                    'Number of bottles': "-", 'Price': "-", 'Size': "-", 'Strength': "-", 'Vintage': "-",
                    'header': "-", 'url': url}


    else:
        header = soup.find("h1", { "class" : "whisky-header" })
        cats = table.findAll("td", { "class" : "key" })
        vals = table.findAll("td", { "class" : "val" })

        catsS=map(lambda x:  " ".join(x.get_text().encode('ascii', 'ignore').split()), cats)
        valsS=map(lambda x:  " ".join(x.get_text().encode('ascii', 'ignore').split()), vals)

        catsS.append('header')
        headerS=" ".join(header.get_text().encode('ascii', 'ignore').split())
        valsS.append(headerS)

        catsS.append('url')
        valsS.append(url)

        tList = zip(catsS,valsS)
        dataDict = dict(tList)
    return dataDict

# GIVEN A URL OF SPECIFIC WHISKY PAGE, GET flavor DATA INFO RETURNED AS A DICT
def flavorDict(url):
    html = urlopen(url).read()
    soup = bs4.BeautifulSoup(html)

    subsoup = soup.find("div", {"id" : "panel-average-reviews"})

    orate = soup.find("div", {"class" : "whisky-rated"})

    # if type(orate) is not 'NoneType':
    if isinstance(orate, types.NoneType):
        dataDict = {'Body': '-', 'Finish': '-','Initial taste': '-','Nose - Aroma': '-',
                    'Presentation': '-','Price': '-','Weighted Rate': '-','number of member votes': '-',
                    'overall rating': '-', 'url': url}

    else:
        orateS= " ".join(orate.get_text().encode('ascii', 'ignore').split())

        votes = soup.find("span", {"id" : "whisky-rating-text"})
        votesS= votes.get_text().encode('ascii', 'ignore').strip(" member votes")

        categs = subsoup.findAll("div", {"class" : "ratingcontrol-label"})
        ratings = subsoup.findAll("div", {"class" : "rating-control-indicator"})


        categsS=map(lambda x: " ".join(x.get_text(" ").encode('ascii', 'ignore').split()[:-1]), categs)
        ratingsS=map(lambda x: x.get_text(" ").encode('ascii', 'ignore'), ratings)

        categsS.append('overall rating')
        categsS.append('number of member votes')

        ratingsS.append(orateS)
        ratingsS.append(votesS)

        categsS.append('url')
        ratingsS.append(url)

        tList = zip(categsS,ratingsS)
        dataDict = dict(tList)

    return dataDict

# TAKE LISTS OF DATA DICTS INPUT AND RETURN A DATAFRAME (UNION):
def dataDF(diction):
    keys =[diction[i].keys() for i in range(len(diction))]
    cats = (set([item for sublist in keys for item in sublist]))
    sList = []

    for i in range(len(diction)):
        s = Series(diction[i],index=cats)
        sList.append(s)

    df = pd.concat(sList, axis=1)
    df = df.transpose()
    df.index = [x.split("/")[-1] for x in df.loc[:,'url']]

    return df

# GIVEN A URL OF SPECIFIC WHISKY PAGE, GET review DATA INFO RETURNED AS A list of DICTs
# url = "http://www.whiskybase.com/whisky/27641/1981-ca"
def notesDict(url):

    html = urlopen(url).read()
    soup = bs4.BeautifulSoup(html)
    sub= soup.find("div", {"id":"tab-notes"})

    noteTaste = soup.findAll("div", {"class" : "whisky-note whisky-note-tasting"})
    # noteAll = soup.findAll("div", {"class" : "whisky-note whisky-note-note"})

    # if type(orate) is not 'NoneType':
    if isinstance(noteTaste, types.NoneType): #or isinstance(noteAll, types.NoneType):
        nDict =    {'Color': '-', 'Nose': '-','Taste': '-','Finish': '-',
                    'Comments': '-', 'noterating': "-", 'url': url}



    else:
        noteList = []
        for n in noteTaste:
            noterating = n.find("div", {"class" : "note-rating"})

            if isinstance(noterating, types.NoneType):
                noterating = "-"
            else:
                noterating = noterating.find("b").get_text().encode('ascii', 'ignore')

            categs = n.findAll("div", {"class" : "note-tasting-label"})
            categs = [c.get_text().encode('ascii', 'ignore') for c in categs]
            categs.append('url')
            categs.append('noterating')
            notes = n.findAll("div", {"class" : "note-tasting-content"})
            notes = [" ".join(n.get_text().encode('ascii', 'ignore').split()) for n in notes]
            notes.append(url)
            notes.append(noterating)


            nList = zip(categs,notes)
            nDict = dict(nList)
            noteList.append(nDict)

    return noteList

# Small function for narrowing down scope of url selection
def logicaltest(value,n):
    if type(value)==int:
        return value>n
    else:
        return False

####################################################################
# SCRAPING: Get the links
####################################################################


url ="http://www.whiskybase.com/brands"
links = [url] + whiskPages(url)

dlinks = [distLinks(u) for u in links] # get distillery links

dlinks = [j for i in dlinks for j in i] # flatten

# Example 1: Selecting only those w/ >100 votes
logical = [logicaltest(d['Votes'],100) for d in dlinks]
# Example 2: Selecting only those bottled after 2012
# logical = [logicaltest(d['Bottled'],2012) for d in ilinks]


numeric = [i for i, elem in enumerate(logical) if elem]

dlinksS = [dlinks[i] for i in numeric]

urlS = [d['url'] for d in dlinksS]

links =[[u] + whiskPages(u) for u in urlS] # for each brand, obtain  list of pagination links
links = [j for i in links for j in i] # flatten

ilinks = [whiskLinks(u) for u in links] # for each pagination link, get links to whisky bottle pages
ilinks = [j for i in ilinks for j in i] # flatten

# Save the links
pickle.dump(ilinks, open( "save2.p", "wb" ))
wlinks = [i['url'] for i in ilinks]

a = []
for item in set(wlinks):
    a.append(item)

####################################################################
# SCRAPING: Get the data, flavor notes & reviews
####################################################################

# Execute the following to replicate:
f = [flavorDict(u) for u in a]
flavorDF = dataDF(f)
# flavorDF.to_csv('flavorDF.csv', index=True)


# Get data for each whisky page
d = [dataDict(u) for u in a]
dDF = dataDF(d)
# dDF.to_csv("dataDF.csv", index=True)


# Get notes for each whisky page
n = [notesDict(u) for u in a]
n = [x for x in n if x != []] # remove empty list elemnts
n = [j for i in n for j in i] # flatten
nDF = dataDF(n)
# nDF.to_csv('noteDF.csv', index=True)


# merge all three data frames
mainDF = pd.merge(nDF, dDF, how='outer', on='url')
MainDF = pd.merge(mainDF, flavorDF, how='outer', on='url')
# MainDF.to_csv('MainDF.csv', index=True)

####################################################################
# EXPORTING
####################################################################

# Dump to csv
pickle.dump(MainDF, open( "MainDFsave.p", "wb" ))

# We can dump subssets of dataframe to csv
MainDF['Nose'][MainDF['Nose'].notnull()].to_csv('text/byNote/Nose.csv', index=True)
MainDF['Taste'][MainDF['Taste'].notnull()].to_csv('text/byNote/Taste.csv', index=True)
MainDF['Comments'][MainDF['Comments'].notnull()].to_csv('text/byNote/Comments.csv', index=True)
MainDF['Finish_x'][MainDF['Finish_x'].notnull()].to_csv('text/byNote/Finish_x.csv', index=True)

# By distillery region, a separate file for each & all in a new folder:
dist = pd.unique(MainDF['District'].values.ravel())
for d in dist:
    tempdata = MainDF[MainDF['District'] == d]
    path = 'text/byDist'
    if not os.path.exists(path):
        os.makedirs(path)
    tempdata[['Nose','Taste','Comments','Finish_x']][tempdata[['Nose','Taste','Comments','Finish_x']].notnull()].to_csv('%s/%s_allNotes.csv' %(path,d), index=True)

# By note, a separate file for each & all in a new folder:
dist = pd.unique(MainDF['District'].values.ravel())
for d in dist:
    tempdata = MainDF[MainDF['District'] == d]
    path = 'text/byDist/%s/byNote/' %d
    if not os.path.exists(path):
        os.makedirs(path)
    tempdata['Nose'][tempdata['Nose'].notnull()].to_csv('%s/Nose.csv' %path, index=True)
    tempdata['Taste'][tempdata['Taste'].notnull()].to_csv('%s/Taste.csv' %path, index=True)
    tempdata['Comments'][tempdata['Comments'].notnull()].to_csv('%s/Comments.csv' %path, index=True)
    tempdata['Finish_x'][tempdata['Finish_x'].notnull()].to_csv('%s/Finish_x.csv' %path, index=True)

