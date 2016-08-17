# TODO: Replace helperFunctions with ProteinBotBoxFunctions.py from diseaseOntology
import helperFunctions as HF
import json
from ProteinBoxBot_Core import PBB_login
import pywikibot
import requests
import urllib2
import pprint

__author__ = 'Becky Tauber'

'''
This script retrieves all terms with a deprecated status from an ontology.
It then checks if the terms are present in WikiData, and if they are, it
requests for them to be deleted.
'''

def requestForDeletion(obs_list, pwd, pID, ontology):
    
    '''
    obs_list = list of obsolete term IDs
    pwd = bot password
    pID = ontology property ID in WikiData
    ontology = ontology lookup code
    '''    
    
    site = pywikibot.Site('test', 'wikidata')
    # site = pywikibot.Site('wikidata', 'wikidata')
    
    # TODO: get correct server
    ''' #Uncomment this section for posting!
    #login = PBB_login.WDLogin(user='', pwd=pwd, server='')
    '''
    
    # No obsolete terms, do nothing
    if (len(obs_list) == 0):
        print 'No obsolete terms in {}.'.format(ontology)
        pass
    
    else:
        obs_qids = []
        
        for o in obs_list:
            # Format for OLS URL
            if ":" in o:
                urlForm = o.replace(":", "_")
                searchID = o
                
            # Format for WikiData search
            if "_" in o:
                urlForm = o
                searchID = o.replace("_", ":")
                
            # get label from ID
            tUrl = 'http://www.ebi.ac.uk/ols/api/ontologies/{}/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F{}'.format(ontology, urlForm)
            tRequest = urllib2.Request(tUrl)
            tU = urllib2.urlopen(tRequest)
            info = tU.read()
            lib = json.loads(info)
            label = lib['label']
            
            wdID = getWikiDataID(site, searchID, label, pID)
            
            if (wdID != None):
                obs_qids.append(wdID)
            else:
                pass
        
        # No obsolete terms in WikiData
        if (len(obs_qids) == 0):
            pass
            print "No obsolete terms in WikiData"
            
        # One term, do deletion request
        if (len(obs_qids) == 1):
            req_text = \
                '''{{{{rfd links|{}|{}}}}} \n\n'''.format(obs_qids[0], 'Deprecated term from {}'.format(ontology))
            
            req_text = req_text + 'Deprecated term from {}'.format(ontology)
            print req_text
            
            ''' #Uncomment this section for posting!
            #title = deprecated_terms[0]
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
            
            
def getNumTerms(ontology):
    '''
    Get ontology version information from OLS
    Get WikiData ID of release, if it exists
    '''
    
    olsUrl = 'http://www.ebi.ac.uk/ols/api/ontologies/{}'.format(ontology)
    request = urllib2.Request(olsUrl)
    u = urllib2.urlopen(request)
    ontology = u.read()
    lib = json.loads(ontology)
    
    
    numTerms = lib['numberOfTerms']
    
    return numTerms



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
       
       
def getWikiDataID(site, oboID, label, pID):
    '''
    Search WikiData for OBO ID and return the WikiData ID.
    If no results, check for search by label and return that ID.
    Double check to make sure an ontology property (pID) is used.
    Otherwise, return None.
    
    Uses the following functions from diseaseOntology/ProteinBoxBotFunctions.py.
    (Imported as helperFunctions as HF):
    getItems and claimExists
    '''
    # search full wikidata
    site=pywikibot.Site('wikidata', 'wikidata')
    wDataByLabel = HF.getItems(site, label)
    lenByLabel = len(wDataByLabel['search'])
    
    if (oboID != None):
        wDataByID = HF.getItems(site, oboID)
        lenByID = len(wDataByID['search'])
    else:
        lenByID = 0

    # If there is exactly one hit on ID search, that is the WD ID
    if (lenByID == 1):
        wdID = wDataByID['search'][0]['id']
        
    # If there are no results...
    elif (lenByID == 0):
        # If there is exactly one label result...
        if (lenByLabel == 1):
            checkID = wDataByLabel['search'][0]['id']
            # Check if ontology property is used with OBO ID
            exists = HF.claimExists(site, checkID, pID, oboID)
            if exists == True:
                wdID = checkID
            # If not, it is not the WD ID
            else:
                wdID = None
        
        # If there are more than one results for the label search...
        elif (lenByLabel > 1 and label != 'Thing'):
            match = []
            # Find all exact matches
            for w in wDataByLabel['search']:
                if w['label'] == label:
                    match.append(w['id'])
            
            # If there is only 1 match...
            if (len(match) == 1):
                checkID = wDataByLabel['search'][0]['id']
                # Check if ontology property is used with OBO ID
                exists = HF.claimExists(site, checkID, pID, oboID)
                if exists == True:
                    wdID = checkID
                else:
                    wdID = None
                
            # If there are more than 1 matches...
            elif (len(match) > 1):
                testID = ''
                for w in wDataByLabel['search']:
                    checkID = w['id']
                    # Check if ontology property is used with OBO ID
                    exists = HF.claimExists(site, checkID, pID, oboID)
                    if exists == True:
                        testID = checkID
                    else:
                        pass
                    
                if (testID != ''):
                    wdID = testID
                else:
                    wdID = None
                    
            else:
                wdID = None
        else:
            wdID = None
    else:
        wdID = None
    
    return wdID
    
    