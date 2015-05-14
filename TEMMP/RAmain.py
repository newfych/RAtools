from pymel.core import *

####################################
def startRA(*args):
    print 'hi'
    createRAmenu()
    
def finishRA(*args):
    print 'by'
    closeUI()
    deleteRAmenu()
    
####################################    
def createRAmenu():
    RAmenu = menu( 'RAmenu', label='RA tools', p='MayaWindow' )
    menuItem( label='RA Genesis UI', command = openGenesisUI)
    menuItem( label='RA Hairs UI', command = openHairsUI)
    print 'OK to load RA tools\n'
    
def deleteRAmenu():
    try:
        deleteUI('RAmenu', menu=True)
        print 'OK to unload RA tools\n'
    except:
        pass
        
####################################    
def openGenesisUI(*args):
    import GenesisUI
    reload (GenesisUI)
    GenesisUI.openUI()  
       
def openHairsUI(*args):
    import HairsUI
    reload (HairsUI)
    HairsUI.main()
 
#################################### 
def closeUI(*args):
    try:
        deleteUI('GenesisUI')
    except:
        pass
    try:
        deleteUI('HairsUI')
    except:
        pass   

    