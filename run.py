from reqDeletion import requestForDeletion
import sys

'''
Must have user-config.py for pywikibot to run
'''

def main():
    # Test run with obsolete terms
    obs_list = ['DOID:4700', 'DOID:6609', 'DOID:3521']
    #obs_list = ['DOID:4700']
    pwd = ''
    pID = 'P699'
    ontology = 'DOID'
    
    requestForDeletion(obs_list, pwd, pID, ontology)
    
if __name__ == '__main__':
    sys.exit(main())