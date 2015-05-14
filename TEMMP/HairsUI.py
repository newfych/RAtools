from pymel.core import *

init_width = 300
init_height = 195
expand_height = 385
sliders_height = 800
row5_layout = (5,80,90,100,10)
row6_slider_layout = (15,60,60,60,60,60)
row6_slider_height = 50
bgc_red = (0.5,0.4,0.4) 
bgc_green = (0.4,0.5,0.4) 
bgc_blue = (0.3,0.4,0.5)

edit_mode = False
current_set = ''



################################
# FUNCTIONS
################################
def checkForHairNode(*args):
    global edit_mode
    try:
        select(clear=True)
        select('RAHairs')
        n = ls(sl=True)
        if len(n) != 0:
            RAHairs = n[0]
            hair_set_system_names = getAttr('RAHairs.hss')
            if len(hair_set_system_names) > 0:
                edit_mode = True
                print 'Hair node exists with ' + str(len(hair_set_system_names)) + ' sets'
    except:
        pass

# FILL HAIR SET MENU        
def fillHairSetMenu(*args):
    try:
        hair_set_system_names = getAttr('RAHairs.hss')
        hair_set_user_names = getAttr('RAHairs.hsu')
        for hair_set_system_name in hair_set_system_names:
            try:
                i = hair_set_system_names.index(hair_set_system_name)
                hair_set_user_name = str(hair_set_user_names[i])
                menu_item_name = str(hair_set_user_name)
                menuItem( menu_item_name,l=hair_set_user_name)
                menuItem( menu_item_name, p = 'HairsSetsMenu', edit = True)
            except:
                print 'Failed to add "' + str(hair_set_system_name) + '" to sets list'
                pass
        if current_set == '':
            last_set = hair_set_user_names[len(hair_set_user_names)-1]
            optionMenu('HairsSetsMenu', v=last_set, acc=True, edit=True)
        else:
            optionMenu('HairsSetsMenu', v=current_set, acc=True, edit=True)
        selected_set = optionMenu('HairsSetsMenu', v=True, query=True)    
        fillStripsList(selected_set)
    except:
        edit_mode = False

# FILL STRIP LIST    
def fillStripsList(sets_name):
    global current_set
    current_set = optionMenu('HairsSetsMenu', v=True, query=True) 
    strips = getStripsBySetName(sets_name)
    textScrollList('HairsStripsList', ra=True, edit=True)
    textScrollList('HairsStripsList', append=strips, sii=1, edit=True)
    select(cl=True)
    updateStripSelection()
    

# UPDATE STRIP SELECTION
def updateStripSelection(*args):
    selected_strips = textScrollList('HairsStripsList', si=True, query=True)
    select(cl=True)
    select(selected_strips)
    uv_frame = frameLayout('UVEditSection', cl=True, query=True)
    if not uv_frame:
        updateUVSliders()
        
    
# RENAME & DELETE SET & SELECT SET
def renameSet(*args):
    result = promptDialog(
            title='Rename Set',
            message='Enter Name(alphabetic chars only):',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
    if result == 'OK':
        selected_set = optionMenu('HairsSetsMenu', v=True, query=True)
        prompt_name = promptDialog(t=True, query=True)
        if prompt_name == '':
            warning('Name is empty!')
            return
        new_name = ''.join(e for e in prompt_name if e.isalpha())
        hair_set_user_names = getAttr('RAHairs.hsu')
        if new_name == '':
            warning('Name "' + str(prompt_name) + '"is incorrect!(probably name contains illegal characters only)')
            return
        try:
            a = hair_set_user_names.index(new_name)
            print 'Name "' + str(new_name) + '" already eists!'
            return
        except:
            pass
        selected_set = optionMenu('HairsSetsMenu', v=True, query=True)
        i = hair_set_user_names.index(selected_set)
        hair_set_user_names.remove(selected_set)
        hair_set_user_names.insert( i, new_name)
        setAttr('RAHairs.hsu', hair_set_user_names)
        str_to_select = selected_set + '__strip_' + '*'
        select(cl=True)
        select(str_to_select)
        strips = ls(sl=True, transforms=True)
        for strip in strips:
            temp_str = str(strip).split('__')
            new_strip_name = str(new_name) + '__' + temp_str[1]
            rename(strip, new_strip_name)
        openUI()
        optionMenu('HairsSetsMenu', sl=(i+1), acc=True, edit=True)
        selected_set = optionMenu('HairsSetsMenu', v=True, query=True)
        fillStripsList(selected_set)
    
def deleteSet(*args):
    selected_set = optionMenu('HairsSetsMenu', v=True, query=True)
    del_geometry = confirmDialog( t='Delete geometry confirm', m='Delete geometry?', b=['Yes','No'], db='No', cb='No', ds='No' )
    result = confirmDialog( t='Delete set', m='Are you sure to delete "' + str(selected_set) + '" set?', b=['Yes','No'], db='Yes', cb='No', ds='No' )
    if result == 'Yes':
        print 'Delete set "' + str(selected_set) + '" confirmed'
        sets_name = optionMenu('HairsSetsMenu', v=True, query=True)
        strips = getStripsBySetName(sets_name)
        if del_geometry == 'Yes':
            delete(strips)
        else:
            removeStrips(strips)
        hair_set_system_names = getAttr('RAHairs.hss')
        hair_set_user_names = getAttr('RAHairs.hsu')
        i = hair_set_user_names.index(sets_name)
        system_set_to_delete = hair_set_system_names[i]
        hair_set_system_names.remove(system_set_to_delete)
        if len(hair_set_system_names) == 0:
            delete('RAHairs')
        else:
            hair_set_user_names.remove(sets_name)
            setAttr('RAHairs.hss', hair_set_system_names)
            setAttr('RAHairs.hsu', hair_set_user_names)
            global current_set
            current_set = ''
    openUI()
            
        
def selectSet(*args):
    selected_set = optionMenu('HairsSetsMenu', v=True, query=True)
    try:
        str_to_select = selected_set + '__strip_' + '*'
        select(cl=True)
        select(str_to_select)
        s = ls(sl=True)
        #textScrollList('HairsStripsList', da=True, edit=True)
        textScrollList('HairsStripsList', si=s, edit=True)
        updateStripSelection()
    except:
        pass

# REMOVE & DELETE STRIP & UPDATE STRIP SELECTION
def removeStrip(*args):
    result = confirmDialog( t='Remove strip from set', m='Are you sure to remove current strip(s)?', b=['Yes','No'], db='Yes', cb='No', ds='No' )
    if result == 'Yes':
        strips = textScrollList('HairsStripsList', si=True, query=True)
        for strip in strips:
            delAttrs(strip)
            new_name = 'Removed_from_' + str(strip)
            rename(strip, new_name)
            select(cl=True)
        selected_set = optionMenu('HairsSetsMenu', v=True, query=True)
        try:
            str_to_select = selected_set + '__strip_' + '*'
            select(str_to_select)
        except:
            hair_set_system_names = getAttr('RAHairs.hss')
            hair_set_user_names = getAttr('RAHairs.hsu')
            i = hair_set_user_names.index(selected_set)
            system_set_to_delete = hair_set_system_names[i]
            hair_set_user_names.remove(selected_set)
            hair_set_system_names.remove(system_set_to_delete)
            if len(hair_set_system_names) == 0:
                delete('RAHairs')
                global edit_mode
                edit_mode = False
            else:
                setAttr('RAHairs.hss', hair_set_system_names)
                setAttr('RAHairs.hsu', hair_set_user_names)
                global current_set
                current_set = ''
    openUI()
        
def deleteStrip(*args):
    result = confirmDialog( t='Delete strip(s)', m='Are you sure to delete current strip(s)?', b=['Yes','No'], db='Yes', cb='No', ds='No' )
    strips = textScrollList('HairsStripsList', si=True, query=True)
    delete(strips)
    try:
        str_to_select = selected_set + '__strip_' + '*'
        select(str_to_select)
    except:
        hair_set_system_names = getAttr('RAHairs.hss')
        hair_set_user_names = getAttr('RAHairs.hsu')
        i = hair_set_user_names.index(selected_set)
        system_set_to_delete = hair_set_system_names[i]
        hair_set_user_names.remove(selected_set)
        hair_set_system_names.remove(system_set_to_delete)
        
        if len(hair_set_system_names) == 0:
            delete('RAHairs')
            global edit_mode
            edit_mode = False
        else:
            setAttr('RAHairs.hss', hair_set_system_names)
            setAttr('RAHairs.hsu', hair_set_user_names)
            global current_set
            current_set = ''
    openUI()
    
def updateSelectionFromScene(*args):
    selected_set = optionMenu('HairsSetsMenu', v=True, query=True)
    sel = ls(sl=True)
    s = []
    for obj in sel:
        try:
            set_name = str(obj).split('__')[0]
            print set_name
            print selected_set
            if set_name == selected_set:
                s.append(obj)
                print 's = ' + str(s)
        except:
            pass
    print s
    if len(s) != 0:
        textScrollList('HairsStripsList', da=True, edit=True)
        textScrollList('HairsStripsList', si=s, edit=True)
        updateStripSelection()

# SELECTION TYPE SWITCH
def denyMultipleSelection(*args):
    selected_strips = textScrollList('HairsStripsList', si=True, query=True)
    first_selected_strip = selected_strips[0]
    textScrollList('HairsStripsList', si=first_selected_strip, ams=False, edit=True)
    updateStripSelection()
    
def allowMultipleSelection():
    selected_strips = textScrollList('HairsStripsList', si=True, query=True)
    textScrollList('HairsStripsList', si=selected_strips, ams=True, edit=True)
    updateStripSelection()
            
# RESIZE
def resizeForEdit(*args):
    window('HairsUI', edit = True, widthHeight=(init_width, expand_height))
    frameLayout('ConvertFrame', cl=True, edit=True)
    allowMultipleSelection()
    
def resizeBack(*args):
    window('HairsUI', edit=True, widthHeight=(init_width, init_height))
    frameLayout('ConvertFrame', cl=False, edit=True)
    
def resizeForUVSliders(*args):
    denyMultipleSelection()
    updateUVSliders()
    window('HairsUI', edit = True, widthHeight=(init_width, sliders_height))
    
# UV SLIDERS    
def updateUVSliders(*args):
    selected_strips = textScrollList('HairsStripsList', si=True, query=True)
    strip = selected_strips[0]
    for x in xrange(1, 6):
        s = getAttr(strip + '.sus' + str(x))
        floatSlider(('UVscale_' + str(x)), v=s, edit=True)
        t = getAttr(strip + '.sut' + str(x))
        floatSlider(('UVtrans_' + str(x)), v=t, edit=True)
    sush = getAttr(strip + '.sush')
    print str(sush) + ' from upd sliders'
    floatSlider('UVscale_h', v=sush, edit=True)
    suth = getAttr(strip + '.suth')
    print str(suth) + ' from upd sliders'
    floatSlider('UVtrans_h', v=suth, edit=True)
    
def dragUVSliders(*args):
    selected_strips = textScrollList('HairsStripsList', si=True, query=True)
    strip = selected_strips[0]
    for x in xrange(1, 6):
        s_slider_value = floatSlider(('UVscale_' + str(x)), v=True, query=True)
        setAttr(strip + '.sus' + str(x), s_slider_value)
        t_slider_value = floatSlider(('UVtrans_' + str(x)), v=True, query=True)
        setAttr(strip + '.sut' + str(x), t_slider_value)
    h_s_slider_value = floatSlider('UVscale_h', v=True, query=True)
    print str(h_s_slider_value) + ' sh'
    setAttr(strip + '.sush',  h_s_slider_value) 
    h_t_slider_value = floatSlider('UVtrans_h', v=True, query=True)
    print str(h_t_slider_value) + ' th'
    setAttr(strip + '.suth', h_t_slider_value)
 
# CONVERT STRIPS
def convertHairStrips(*args):
    import RA_Hairs_Convert
    reload (RA_Hairs_Convert)
    RA_Hairs_Convert.convert()
    openUI()

# CLOSE UI
def closeUI(*args):
    try:
        deleteUI('HairsUI')
    except:
        pass

# UTILS
def getStripsBySetName(sets_name):
    str_to_select = sets_name + '__strip_' + '*'
    select(cl=True)
    a = ls(sl=True)
    select(str_to_select)
    strips = ls(sl=True, transforms=True)
    return strips
    
def getLastSetNumber(*args):
    hair_set_system_names = getAttr('RAHairs.hss')
    last_set = str(hair_set_system_names[len(hair_set_system_names) -1])
    temp_str = last_set.split('_')
    set_number = int(temp_str[2]) 
    return set_number
    
def delAttrs(strip):
    deleteAttr(strip, at='hso')
    deleteAttr(strip, at='sul')
    # UV ATTR SECTION
    deleteAttr(strip, at='sus1')
    deleteAttr(strip, at='sus2')
    deleteAttr(strip, at='sus3')
    deleteAttr(strip, at='sus4')
    deleteAttr(strip, at='sus5')
    deleteAttr(strip, at='sush')
                    
    deleteAttr(strip, at='sut1')
    deleteAttr(strip, at='sut2')
    deleteAttr(strip, at='sut3')
    deleteAttr(strip, at='sut4')
    deleteAttr(strip, at='sut5')
    deleteAttr(strip, at='suth')
    
    
####################################
# WINDOW SETUP                   
####################################    
def openUI(*args):
    closeUI()
    global edit_mode
    edit_mode = False
    checkForHairNode()
    RAwindow = window('HairsUI', title='RA hairs tool', iconName='RA')
    columnLayout(adjustableColumn=True)
    
    #######################
    # CONVERT FRAME
    #######################
    frameLayout('ConvertFrame', l='Convert hair strips', borderStyle='in', cll=True, cl=(edit_mode))
    columnLayout(adjustableColumn = True)
    separator( h = 5, st = 'none')
    text(l='Steps:', fn='boldLabelFont', h=20)
    separator( h = 5, st = 'none')
    text(l='1. Separate mesh, imported from ZBrush.', align='left')
    separator(h=5, st='none')
    text(l='2. Hide all objects in your scene, except for hair strips.', align='left')
    separator(h=5, st='none')
    text(l='3. Press "Convert" button. :)', align='left')
    separator(h=5, st='none')
    rowLayout(nc=5, cw5=row5_layout)
    text(l='')
    text(l='')
    text(l='')
    button(l='Convert', c=convertHairStrips, w=100, bgc=bgc_green)
    setParent('..')
    separator(h=5, st='none')
    setParent('..')
    setParent('..')
    separator(h=5, st='none')
    
    #print 'Convert frame'
    
    #####################
    # EDIT FRAME
    #####################
    frameLayout('EditFrame',l='Edit hair strips', cc=resizeBack, ec=resizeForEdit, en=edit_mode, cll=True, cl=( not edit_mode))
    columnLayout(adjustableColumn = True)
    
    # HAIR SET SECTION
    text(l='Select hair set', fn='boldLabelFont', h=20)
    separator( h = 5, st = 'none')
    rowLayout( nc = 2,  cw2 = ( 120, 170))
    text(l=' Current hair set:')
    optionMenu('HairsSetsMenu', w=170, acc=True, cc=fillStripsList)
    setParent( '..' )
    
    #print 'Hair set section'
       
    # RENAME & DELETE SET BUTTONS
    separator( h = 5, st = 'none')
    rowLayout( nc = 4,  cw4 = (40,40,25,100))
    button('DeleteSet', l='Delete set', c=deleteSet, w=80, bgc=bgc_red)
    button( 'RenameSet', l='Rename set', c=renameSet, w=80, bgc=bgc_blue)
    text(l='')
    button( 'SelectSet', l='Select set', c=selectSet, w=100, bgc=bgc_green)
    setParent('..')
    separator(h=5, st='in')
    
    #print 'Set edit buttons'
    
    # HAIR LIST SECTION
    text(l='Select hair strips to edit', fn='boldLabelFont', h=20)
    separator(h = 5, st = 'none')
    textScrollList('HairsStripsList', sc=updateStripSelection, nr=5, ams=True)
    setParent('..')

    fillHairSetMenu()
    
    # REMOVE & DELETE STRIP BUTTONS
    rowLayout( nc = 4,  cw4 = (40,40,25,90))
    button('DeleteStrip', l='Delete strip', c=deleteStrip, w=80, bgc=bgc_red)
    button( 'RemoveStrip', l='Remove strip', c=removeStrip, w=80, bgc=bgc_blue)
    text(l='')
    button( 'UpdateSelection', l='Update selection', c=updateSelectionFromScene, w=100, bgc=bgc_green)
    setParent('..')
    separator(h=5, st='in')
    
    #print 'Strip edit buttons'
    
    # HAIR MATERIAL SECTION
    rowLayout(nc=2, cw2=(120,170))
    text(l=' Current strip material: ')
    optionMenu('HairsMaterialMenu', w=170)
    menuItem(l='Default') 
    setParent('..')
    
    #print 'Hair material section'
    
    # HAIR LAYOUT SECTION
    rowLayout(nc=2, cw2=(120,170))
    text(l=' Current strip layout: ')
    optionMenu('HairsLayoutMenu', w=170)
    menuItem(l='1')
    menuItem(l='2')
    menuItem(l='3')
    menuItem(l='4')
    menuItem(l='5')
    setParent('..')
    
    #print 'Hair layout section'
    
    # UV SLIDERS
    frameLayout('UVEditSection',l='UV edit section', cc=resizeForEdit, ec=resizeForUVSliders, cll=True, cl=True)
    text(l='Scale', fn='boldLabelFont', h=20)
    rowLayout(nc=6,cw6=row6_slider_layout)
    text(l='')
    for x in xrange(1, 6):
        floatSlider(('UVscale_'+str(x)), dc=dragUVSliders, min=0, max=2, hr=False, h=row6_slider_height)
    setParent('..')
    floatSlider('UVscale_h', dc=dragUVSliders, min=0, max=2)
    separator(h=5, st='in')
        ###################
    text(l='Translate', fn='boldLabelFont', h=20)
    rowLayout(nc=6,cw6=row6_slider_layout)
    text(l='')
    for x in xrange(1, 6):
        floatSlider(('UVtrans_'+str(x)), dc=dragUVSliders, min=0, max=2, hr=False, h=row6_slider_height)
    setParent('..')
    floatSlider('UVtrans_h', dc=dragUVSliders, min=0, max=2)
    separator(h=5, st='in')
    setParent('..')
    setParent('..')
    
    #print 'UV sliders section'
    
    # MOVE SLIDERS
    
    #print 'Move sliders section'
    
    # CLOSE BUTTON 
    rowLayout(nc=5,  cw5=row5_layout)
    text(l='')
    text('ToolInfo', l='')
    text(l='')
    button(l='Close', c=closeUI, w=100, bgc=(0.6,0.5,0.5))
    setParent('..')
    
    
    window('HairsUI', edit = True, wh=(init_width, init_height))
    if edit_mode:
        resizeForEdit()
    showWindow( RAwindow)
    
def main():
    openUI()
    
main()