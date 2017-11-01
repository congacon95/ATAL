from ptl import get
import importlib
#get.st(debug=True, new_driver=False)
get.st(debug=False, new_driver=True)
def check_career(string):    
    if type(string) is str:
        return string.split('\n')        
    else:
        return []
try:
    people= 'Lawyer ID Pages'
    career=  'Career Link 1'
    df_input = get.df('input.csv')[[people, career]]
    scripts = [ {'domain':get.dmn(page[0]), 'people':page[0], 'career': check_career(page[1])} for k, page in df_input.iterrows()]
    if len(get.sys.argv)==2:
        index = int(get.sys.argv[1])
        scripts = scripts[index:index+1]
    for i, script in enumerate(scripts):
        try:      
            module = importlib.import_module("scripts."+script['domain'])
            root = get.dmr(script['people'])
            file_name =  get.fi(i,4)+'_'+script['domain']
            get.log('> File name:\t'+file_name)
            get.log('> Run script:\tscripts.'+script['domain'])        
            get.log('> GET data')
            if get.DEBUG:
                data_path = 'raw/'+get.os.listdir('raw')[-1]+'/'+file_name+'P.csv'
                get.log('> Load data from: '+ data_path)
                df = get.df(data_path)
                rows = []
                for k, row in df.iterrows():
                    rows.append({'URL':row['URL'], 'SOUP':get.bs(row['SOUP'],'html.parser')})
            else:
                get.log('> Load data from: '+script['people'])
                rows, method = module.get(get, script['people'], root, [])         
                get.download_soups(rows, method= method)
                get.log('> Save raw data')
                get.save(rows, 'raw/'+get.START_TIME+'/'+file_name+'P')
            get.log('> PARSE data')
            for row in rows:        
                get.__SOUP__ = row['SOUP']
                module.parse(get, row, root)

            get.save(rows, 'output/'+get.START_TIME+'/'+file_name+'P', ['SOUP'])
            get.save_logs(script['domain'])
        except:
            get.pe()
except:
    get.pe()
    get.time.sleep(20)
get.quit()
if get.DEBUG:
    get.time.sleep(20)