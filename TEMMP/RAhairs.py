from pymel.core import *
import sys


RAHairs = 0
hairs_list = []
hairs_uvs_list = []
v_scale = 5

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

def createHairsList(*args):
    hairs_set = len(getAttr('RAHairs.hss')) 
    try:    
        select(cl=True)
        hairs_transforms = ls( transforms=True, visible=True)
        print hairs_transforms
        hairs_transforms = cleanupHairsList(hairs_transforms)
        if len(hairs_transforms) == 0 :
            warning('Nothing to convert')
            sys.exit('Something went wrong...')
        i = 0
        for hair in hairs_transforms:
            temp_name = 'Hair_strip_' + str(hairs_set + 1) + '_' + str(i+1)
            rename( hair, temp_name)
            hairs_list.append( hair)
            i +=1
    except:
        warning( "Failed to create hair list")
        sys.exit('Something went wrong...')
    select( clear = True)

def cleanupHairsList(hairs_transforms):
    temp_list = hairs_transforms
    for x in xrange (0, (len(hairs_transforms)-1)):
        obj = temp_list[x]
        is_already_hair_strip = attributeQuery( 'hso', node=obj, exists=True)
        if is_already_hair_strip:
            hairs_transforms.remove(obj)
    if len(hairs_transforms) == 0:
        warning('Nothing to convert!!!')
        sys.exit('Something went wrong...')
    return hairs_transforms
        
def mergeHairVertices(*args):
    for hair in hairs_list:
        select( clear = True)
        select( hair)
        polyMergeVertex( d = 1e-006)
        num_verts = float(polyEvaluate( vertex = True))        
        hair_divs = float(num_verts/3)
        if ( hair_divs != int(hair_divs) or num_verts < 8):
            warning( str(hair) + ' not a hair strip object!')
            undo()
            hairs_list.remove(hair)
    addHairAtrr()
    select( clear = True)
    
def addHairAtrr():
    for hair in hairs_list:
        select( clear = True)
        select( hair)
        addAttr(sn='hso', ln='hair_strip_object', at = 'bool')
        temp_str = str(hair)+'.hso'
        setAttr(str(hair)+'.hso', True)
    
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
    v_offset = float((1.0/v_scale)/4)
    for uvs in hairs_uvs_list:
        uvs_index = str(hairs_uvs_list.index(uvs) + 1)
        convert_status =  uvs_index + ' of '+ num_of_strips + ' hair strip processing...'
        print convert_status
        num_divs = len(uvs)/3
        u_offset = float(1.0/(num_divs - 1))
        for x in xrange( 0, len(uvs)/3):
            for y in xrange(0, 3):
                sel = uvs[x*3 + y]
                select( sel)
                u = x*u_offset
                v = v_offset + y*v_offset
                polyEditUV( u = 0, v = 0, relative = False)
                polyEditUV( u = u, v = v, relative = False)
    select( clear = True)

# TO DO   
def delHistory(*args):
    for hair in hairs_list:
        select(hair, r=True)
        delete(ch=True)
    select(cl=True)

def createHairsSetNode(*args):
    hair_sets_system = getAttr('RAHairs.hss')
    len_sets_count = len(hair_sets_system)
    if len_sets_count > 0 :
        last_set_name = str(hair_sets_system[len_sets_count - 1])
        temp_list= last_set_name.split('_')
        set_number = int(temp_list[2]) + 1
    else:
        set_number = 1
    set_count = len(hair_sets_system)
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

def convert(*args):
    
    print 'Convertion starts'
    createRAHairsNode()   
    createHairsList()
    mergeHairVertices()
    createHairsUVs()
    createHairsUVsList() 
    transformHairsUVs()
    delHistory()
    createHairsSetNode()
    select(cl=True)
    
    print  'Convertion done.'
    
convert()        