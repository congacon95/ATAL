def get(get, people, root, rows):
    for char in get.string.ascii_lowercase:
        url='https://www.akerman.com/en/people/index.html?l='+char
        get.log('> GET '+url) 
        get._SOUP = get.soup(url)
        people = get.bes('people-search-result__photo-container')
        for div in people:
            rows.append({'URL':root+div.a['href']})
    return rows, 'nodriver'

def parse(get, row, root):
    get.name(row, get.bet('bio-header__name', 'h1'))
    row['Position Title']=get.bet('bio-header__title', 'p')
    row['Office']=get.bet('bio-header__office', 'p')
    row['Phone']=get.bep('bio-header__telephone','p')
    mail=get.be('bio-header__email', 'p')
    if mail: row['Email']=mail.a['data-href'].replace('mailto:','')
    vcard=get.be('type__bio-info text-gray', 'p')
    if vcard: row['Vcard']=root+vcard.a['href']
    linkedin=get.be('bio-header__linkedin-link', 'a')
    if linkedin: row['LinkedIn']=linkedin['href']
    for div in get.bes('hybrid-accordion'):
        row[get.bet('js-hybrid-accordion__header', parent=div)]=get.bet('js-hybrid-accordion__content', parent=div).strip()
    for div in get.bes('js-sidebar-accordion'):
        col_name = get.bet('js-sidebar-accordion__header', parent=div)
        content = get.be('js-sidebar-accordion__content', parent=div)
        if content.h3:
            h3s = content.findAll('h3')
            uls = content.findAll('ul')
            for i, h3 in enumerate(h3s):
                row[col_name+' '+h3.text.strip()]=uls[i].text.strip()
        else:
            row[col_name] = '\n'.join([li.text.strip() for li in content.findAll('li')])
    extras = get.bes('content-accordion')
    if extras:
        for div in extras:
            divs = get.bes('content-accordion__item', parent=div)
            text= [div.text.strip() for div in divs]
            row[div.h2.text] = '\n'.join(text)