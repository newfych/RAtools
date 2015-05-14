from pymel.core import *

init_width = 300
init_height = 195
expand_height = 330
sliders_height = 800
row5_layout = (5,80,90,100,10)
row6_slider_layout = (15,60,60,60,60,60)
row6_slider_height = 50
bgc_red = (0.5,0.4,0.4) 
bgc_green = (0.4,0.5,0.4) 
bgc_blue = (0.3,0.4,0.5)

edit_mode = False

################################
# FUNCTIONS
################################

# CHECK FOR MUSCLE NODE

def checkForMuscleNode(*args):
    global edit_mode
    try:
        select(clear=True)
        select('RAmuscle')
        n = ls(sl=True)
        if len(n) != 0:
            RAmuscle = n[0]
            edit_mode = True
            print 'node exists'
    except:
        pass
    
# CREATE MUSCLE SYSTEM
def createMuscleSystem(*args):
    print 'create section'
    import RA_Create_Muscle_System
    reload (RA_Create_Muscle_System)
    RA_Create_Muscle_System.create()
    openUI()
 
def updateMuscleSelection(*args):
    selected_muscle = textScrollList('MusclesList', si=True, query=True)
    select(cl=True)
    select(selected_muscle)  
    
# CLOSE UI
def closeUI(*args):
    try:
        deleteUI('MusclesUI')
    except:
        pass
    
####################################
# WINDOW SETUP                   
####################################  
def openUI(*args):
    closeUI()
    checkForMuscleNode()
    if edit_mode == False:
        openCreateUI(*args)
    else:
        openEditUI(*args)
        
        
    
def openCreateUI(*args):
    RAwindow = window('MusclesUI', title='RA muscles tool', iconName='RA')
    columnLayout(adjustableColumn=True)
    
    #######################
    # START FRAME
    #######################
    frameLayout('CreateFrame', l='Create muscle system', borderStyle='in', ec=resizeBack, cll=True, cl=(edit_mode))
    columnLayout('CL1', adjustableColumn = True)
    separator( h = 5, st = 'none')
    text(l='Steps:', fn='boldLabelFont', h=20)
    separator( h = 5, st = 'none')
    text(l='1. Separate mesh, imported from ZBrush.', align='left')
    separator(h=5, st='none')
    text(l='2. Hide all objects in your scene, except for hair strips.', align='left')
    separator(h=5, st='none')
    radioCollection('ChooseGender', p='CL1')
    radioButton( 'Female', label='Female', sl=True)
    radioButton( 'Male', label='Male' )
    #radioCollection('ChooseGender', sl='Female', edit=True)
    separator(h=5, st='none')
    
    rowLayout(nc=5, cw5=row5_layout)
    text(l='')
    text(l='')
    text(l='')
    button(l='Create', c=createMuscleSystem, w=100, bgc=bgc_green)
    setParent('..')
    separator(h=5, st='none')
    setParent('..')
    setParent('..')
    separator(h=5, st='none')
    
    # CLOSE BUTTON 
    rowLayout(nc=5,  cw5=row5_layout)
    text(l='')
    text('ToolInfo', l='')
    text(l='')
    button(l='Close', c=closeUI, w=100, bgc=bgc_red)
    setParent('..')
    
    
    window('MusclesUI', edit = True, wh=(init_width, init_height))
    showWindow( RAwindow)
  
def openEditUI(*args):
    RAwindow = window('MusclesUI', title='RA muscles tool', iconName='RA')
    columnLayout(adjustableColumn=True)
    
    #####################
    # EDIT FRAME
    #####################
    frameLayout('EditFrame',l='Edit muscles', cc=resizeBack, ec=resizeForEdit, en=edit_mode, cll=True, cl=( not edit_mode))
    columnLayout(adjustableColumn = True)
    
    
    # HAIR LIST SECTION
    text(l='Select muscle to edit', fn='boldLabelFont', h=20)
    separator(h = 5, st = 'none')
    textScrollList('MusclesList', sc=updateMuscleSelection, nr=5, ams=True)
    setParent('..')
    setParent('..')
    
    # CLOSE BUTTON 
    rowLayout(nc=5,  cw5=row5_layout)
    text(l='')
    text('ToolInfo', l='')
    text(l='')
    button(l='Close', c=closeUI, w=100, bgc=bgc_red)
    setParent('..')
    
    
    window('MusclesUI', edit = True, wh=(init_width, init_height))
    showWindow( RAwindow)
    
def main():
    openUI()
    