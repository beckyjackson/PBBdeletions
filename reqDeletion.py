from ProteinBoxBot_Core import PBB_Core
from ProteinBoxBot_Core import PBB_login
import requests

__author__ = 'Becky Tauber'

def requestForDeletion(obs_list, pwd, pID, ontology):
    """
    Checks if obsolete terms are present in WikiData and, if so,
    posts a request for deletion.
    :param obs_list: list of obsolete term IDs
    :param pwd: bot password
    :param pID: ontology property ID in WikiData
    :param ontology: ontology lookup code
    """   
    
    # TODO: get correct server
    ''' #Uncomment this section for posting!
    #login = PBB_login.WDLogin(user='', pwd=pwd, server='')
    '''
    obs_qids = []
    
    for o in obs_list:   
        if "_" in o:
            o = o.replace("_", ":")
        wdID = getWikiDataID_PBB(o, pID)
        
        if (wdID != None):
            obs_qids.append(wdID)
        
    if (len(obs_qids) == 0):
        print "No obsolete terms in WikiData"
        
    # One term, do deletion request
    if (len(obs_qids) == 1):
        req_text = \
            '''{{{{rfd links|{}|{}}}}} \n\n'''.format(obs_qids[0], 'Deprecated term from {}'.format(ontology))
        
        req_text = req_text + 'Deprecated term from {}'.format(ontology)
        print req_text
        
        ''' #Uncomment this section for posting!
        #title = obs_qids[0]
        #r = postRequest(req_text, login, title)
        #pprint.pprint(r.json())
        '''
           
    # More than one term, do bulk deletion request    
    else:
        req_text_prfx = \
            '''{{subst:Rfd group | '''
        
        for ot in obs_qids:
            req_text_prfx = req_text_prfx + '{} | '.format(ot)
        
        req_text_sfx = 'reason = Deprecated terms from {}}}}}'.format(ontology)    
        req_text = req_text_prfx + req_text_sfx 
        print req_text
        
        ''' #Uncomment this section for posting!
        #title = 'Bulk Deletion Request - Deprecated Terms'
        #r = postRequest(req_text, login, title)
        #pprint.pprint(r.json())
        '''
            

def postRequest (req_text, login, title):      
    params = {
                  'action': 'edit',
                  'title': 'Wikidata:Requests_for_deletions',
                  'section': 'new',
                  'sectiontitle': title,
                  'appendtext': req_text,
                  'token': login.get_edit_token(),
                  'format': 'json'
                  }
    
    # TODO: get correct URL
    r = requests.post(url='', data=params, cookies=login.get_edit_cookie())
    return r
       
       
def getWikiDataID_PBB(oboID, pID):
    '''
    Search WikiData for any item that has the claim of given pID
    (ontology ID property) with the oboID as a string. If no results
    found, return None.
    '''   
    query = 'string[{}:"{}"]'.format(pID.split("P",1)[1], oboID)
    wd_items = PBB_Core.WDItemList(query).wditems
    
    if (wd_items['status']['items'] == 1):
        wdID = 'Q{}'.format(wd_items['items'][0])
    
    else:
        wdID = None
        
    return wdID
  
