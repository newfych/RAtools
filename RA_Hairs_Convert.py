from pymel.core import *
import sys


RAHairs = 0
hairs_list = []
hairs_uvs_list = []
v_scale = 5

def createHairsList(*args):
    convert_status = True
    try:    
        select(cl=True)
        hairs_transforms = ls( transforms=True, visible=True)
        if len(hairs_transforms) == 0 :
            warning('There is no objects to convert.')
            convert_status = False
            return convert_status
        hairs_transforms = cleanupHairsList(hairs_transforms)
        if len(hairs_transforms) == 0 :
            warning('There is probably only already converted objects in the scene.')
            convert_status = False
            return convert_status
        set_number = getLastSetNumber()
        i = 0
        for hair in hairs_transforms:
            set_number = getLastSetNumber()
            name_for_set_node = 'Hair_set_' + str(set_number)
            temp_name = name_for_set_node +'__strip_' + str(i+1)
            rename( hair, temp_name)
            hairs_list.append(hair)
            i +=1
    except:
        warning( "Failed to create hair list")
        convert_status = False
    select( clear = True)
    return convert_status

def cleanupHairsList(hairs_transforms):
    temp_list = []
    for obj in hairs_transforms:
        is_already_hair_strip = attributeQuery( 'hso', node=obj, exists=True)
        if is_already_hair_strip:
            print str(obj) + ' is already converted object. Removed from convertion list'
        else:
            temp_list.append(obj)
    hairs_transforms = temp_list        
    return hairs_transforms

def createRAHairsNode(*args):
    try:
        select( clear = True)
        select('RAHairs')
        n = ls( sl = True)
        if len(n) != 0:
            RAHairs = n[0]  
    except:
        RAHairs = createNode('materialInfo', n = 'RAHairs')
        addAttr( sn='hs', ln='hairs_set', at = 'long')
        setAttr('RAHairs.hs', 0)
        empty_array = []
        addAttr( sn='hss', ln='hairs_sets_system', dt = 'stringArray')
        setAttr('RAHairs.hss', empty_array)
        addAttr( sn='hsu', ln='hairs_sets_user', dt = 'stringArray')
        setAttr('RAHairs.hsu', empty_array)
                
def mergeHairVertices(*args):
    global hairs_list
    convert_status = True
    temp_list = []
    for hair in hairs_list:
        select(cl=True)
        select(hair)
        polyMergeVertex(d=1e-006)
        num_verts = float(polyEvaluate(vertex=True))        
        hair_divs = float(num_verts/3)
        if ( hair_divs != int(hair_divs) or num_verts < 9):
            warning( str(hair) + ' not valid hair strip object. Removed from convertion list')
            undo()
        else:
            temp_list.append(hair)
    hairs_list = temp_list
    if len(hairs_list) == 0 :
            warning('There is no valid objects in the scene.')
            convert_status = False
    addHairAtrr()
    select( clear = True)
    return convert_status
    
def addHairAtrr():
    for hair in hairs_list:
        select( clear = True)
        select( hair)
        addAttr(sn='hso', ln='hair_strip_object', at = 'bool')
        temp_str = str(hair)+'.hso'
        setAttr(str(hair)+'.hso', True)
        # UV LAYOUT SECTION
        addAttr(sn='sul', ln='strip_uv_layout', at = 'byte')
        setAttr(str(hair)+'.sul', 1)
    
def createHairsUVs(*args):
    for hair in hairs_list:
        select(clear = True)
        select(hair)
        mel.eval( 'PolySelectConvert 1;')  
        polyProjection()    
    select( clear = True)

def createHairsUVsList(*args):
    for hair in hairs_list:
        hair_verts = [2, 1, 5, 3, 0, 4]
        hair_uvs = []
        select( clear = True)
        select( hair)
        num_verts = polyEvaluate( vertex = True)
        for x in xrange( 6, num_verts):
            hair_verts.append(x)
        num_divs = len(hair_verts)/3
        for y in xrange(1, num_divs-1):
            str_to_sel_1 = str(hair) + '.vtx[' + str(hair_verts[y*3]) + ']'
            str_to_sel_2 = str(hair) + '.vtx[' + str(hair_verts[y*3+1]) + ']'
            str_to_sel_3 = str(hair) + '.vtx[' + str(hair_verts[y*3+2]) + ']'
            select( clear = True)
            select( str_to_sel_1)
            select( str_to_sel_2, add = True)
            select( str_to_sel_3, add = True)
            mel.eval( 'PolySelectConvert 4;')
            polyMapSewMove() 
        for v in hair_verts:
            select( clear = True)
            str_to_sel = str(hair) + '.vtx[' + str(v) + ']'
            select( str_to_sel)
            mel.eval( 'PolySelectConvert 4;')
            uv = ls(sl = True)
            hair_uvs.append(uv)
        hairs_uvs_list.append(hair_uvs)

def transformHairsUVs(*args):
    num_of_strips = str(len(hairs_uvs_list))
    v_offset = float((1.0/v_scale)/2)
    for uvs in hairs_uvs_list:
        uvs_index = str(hairs_uvs_list.index(uvs) + 1)
        convert_status =  uvs_index + ' of '+ num_of_strips + ' hair strip processing...'
        text('ToolInfo', l=convert_status, edit=True)
        print convert_status
        num_divs = len(uvs)/3
        u_offset = float(1.0/(num_divs - 1))
        for x in xrange( 0, len(uvs)/3):
            for y in xrange(0, 3):
                sel = uvs[x*3 + y]
                select( sel)
                u = x*u_offset
                v = y*v_offset
                polyEditUV( u = 0, v = 0, relative = False)
                polyEditUV( u = u, v = v, relative = False)
    select( clear = True)

def delHistory(*args):
    for hair in hairs_list:
        select(hair, r=True)
        delete(ch=True)
    select(cl=True)

def createHairsSetNode(*args):
    hair_sets_system = getAttr('RAHairs.hss')
    set_number = getLastSetNumber()
    name_for_set_node = 'Hair_set_' + str(set_number)
    RAHairs = createNode('materialInfo', n = name_for_set_node)
    addAttr( sn='hsn', ln='hair_set_name', dt = 'string')
    attr_name = name_for_set_node + '.hsn'
    setAttr(attr_name, name_for_set_node)
    hair_sets_system.append(name_for_set_node)
    setAttr('RAHairs.hss', hair_sets_system)
    hair_sets_user = getAttr('RAHairs.hsu')
    hair_sets_user.append(name_for_set_node)
    setAttr('RAHairs.hsu', hair_sets_user)

def getLastSetNumber(*args):
    hair_set_system_names = getAttr('RAHairs.hss')
    len_system_names = len(hair_set_system_names)
    if len_system_names == 0:
        set_number = 1
    else:
        last_set = str(hair_set_system_names[len(hair_set_system_names) -1])
        temp_str = last_set.split('_')
        set_number = int(temp_str[2]) + 1
    return set_number

def convert(*args):
    print 'Convertion starts'
    createRAHairsNode()
    if createHairsList() == True:
        if mergeHairVertices():
            createHairsUVs()
            createHairsUVsList() 
            transformHairsUVs()
            delHistory()
            createHairsSetNode()
            select(cl=True)
            print  'Convertion done.'
    else:
        print 'Something went wrong, see script editor for details'