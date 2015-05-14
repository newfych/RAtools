from pymel.core import *

####################################
def startRA(*args):
    createRAmenu()
    
def finishRA(*args):
    closeUI()
    deleteRAmenu()
    
####################################    
def createRAmenu():
    RAmenu = menu( 'RAmenu', label='RA tools', p='MayaWindow' )
    menuItem( label='RA Hairs UI', command = openHairsUI)
    menuItem( label='RA Muscles UI', command = openMusclesUI)
    print 'OK to load RA tools\n'
    
def deleteRAmenu():
    try:
        deleteUI('RAmenu', menu=True)
        print 'OK to unload RA tools\n'
    except:
        pass
        
####################################          
def openHairsUI(*args):
    import HairsUI_Free
    reload (HairsUI_Free)
    HairsUI_Free.main()
    
def openMusclesUI(*args):
    import MusclesUI
    reload (MusclesUI)
    MusclesUI.main()
 
#################################### 
def closeUI(*args):
    try:
        deleteUI('HairsUI')
        deleteUI('MusclesUI')
    except:
        pass   

    