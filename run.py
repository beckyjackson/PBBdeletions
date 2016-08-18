from reqDeletion import requestForDeletion
import sys

def main():
    """
    Test run with obsolete terms from DOID
    """
    
    obs_list = ['DOID:4700', 'DOID:6609', 'DOID:3521']
    #obs_list = ['DOID:4700']
    #obs_list = []
    pwd = ''
    pID = 'P699'
    ontology = 'DOID'
    
    if (len(obs_list) > 0):
        requestForDeletion(obs_list, pwd, pID, ontology)
    else:
        pass
    
if __name__ == '__main__':
    sys.exit(main())