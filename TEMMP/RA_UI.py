windowRA  = 0

def createUIRA(*args):
    global windowRA
    deleteUIRA()
    windowRA = window( title="Long Name", iconName='Short Name', widthHeight=(200, 200) )
    columnLayout( adjustableColumn=True )
    button( label='Create scene', command = createSceneRA )
    button( label='Close', command = deleteUIRA )
    setParent( '..' )
    showWindow( windowRA )
    
def deleteUIRA(*args):
    global windowRA
    try:
        deleteUI(windowRA, window=True) 
    except:
        pass
        
def createSceneRA(*args):
    NewScene()
    importFile("C:\RAtools\Genesis2_base_female.fbx")
    createDisplayLayer(name='Genesis_skeleton', n=1, e=True)
    createDisplayLayer(name='Genesis_mesh', n=1, e=True)
    createDisplayLayer(name='Duplicated_mesh', n=1, e=True)
    createDisplayLayer(name='Transformed_mesh', n=1, e=True)
    select(all=True)
    j = ls( sl=True, type='joint' )
    #unparent mesh
    
    
    #duplicate mesh and rename
    
    
    #separate mesh and rename
    
    
    #select(clear=True)
    #select(j)
    
    #add to layers
    editDisplayLayerMembers('Genesis_skeleton', j)