from pymel.core import *
    
####################################    
def openUI(*args):
    closeUI()
    RAwindow = window( 'GenesisUI', title='RA Genesis tool', iconName='RA', widthHeight=(200, 200) )
    columnLayout( adjustableColumn=True )
    button( label='Init scene', command = RAscene )
    button( label='Close', command = closeUI )
    setParent( '..' )
    showWindow( RAwindow)
    
def closeUI(*args):
    try:
        deleteUI('GenesisUI')
    except:
        pass
        
####################################       
def RAscene(*args):
    import RAscene
    reload ( RAscene)
    RAscene.initRAscene()
