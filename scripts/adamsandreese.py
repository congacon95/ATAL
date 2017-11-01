def get(get, people, root, rows):
    soup = get.soup(people, get=True)    
    for tr in soup.find('table').find('tbody').findAll('tr'):
        rows.append({'URL':(tr.div.a['href'])})
    return rows, 'driver'
def get_office(get, office, root):
    soup = get.soup(office)    
def parse(get, row, root):        
    try:
        #print(row['SOUP'])
        title = get.be('titleinfo')
        if title:
            get.name(row, title.div.h1.text)
            #get.log('> Parsing '+row['Full Name'])
            row['Position Title'] = get.bet('level', parent=title)
            row['Email'] = get.bet('email',parent=title)
            vcard = title.find('a')
            if vcard:
                row['Vcard'] = root+vcard['href']
            row['Position Title'] = title.findAll('a')[1].text
        offices = get.be('office')
        if offices:
            offices = offices.findAll('li')
            for office in offices:
                idx = offices.index(office)
                row['Office_'+str(idx)+'_Location']=get.bet('name',parent=office)
                row['Office_'+str(idx)+'_Tel']=get.bep('phone',parent=office)
                row['Office_'+str(idx)+'_Fax']=get.bep('fax',parent=office)
            
        row['LinkedIn'] = get.bet('linkedin')
        divs = get.be('rightside').findAll('div', recursive=False)
        cols = [div for div in divs[:-1]] + [div for div in divs[-1].findAll('div', recursive=False)]
        for col in cols:
            name = col.h2.text.title()
            text = col.div.text.strip().replace('\n\n', '\n').replace(', \n', ', ')
            row[name] =  text    
    except:
        get.pe(row['URL'])