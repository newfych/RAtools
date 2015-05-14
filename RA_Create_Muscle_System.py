from pymel.core import *

import RA_muscles_data
reload (RA_muscles_data)

body_parts = {'left_arm':['l_bicep']}
muscle_list=[]
sex = ''

##################################################
# FUNCTIONS
##################################################

def delIfExists():
    try:
        delete('RAmuscle')
    except:
        pass
        
def fillMuscleList():
    global muscle_list
    for part in body_parts.keys():
        for muscle in body_parts[part]:
            muscle_list.append(muscle)

def create(*args):
    global sex
    gender = radioCollection('ChooseGender', query=True, sl=True)
    print gender
    if gender == 'Female':
        sex = 'female'
        importFile("C:/RAtools/Muscles_start_female.ma")
        
    else:
        sex = 'male'
        print 'Not working yet'
    delIfExists()
    createMuscleNode()
        
def createMuscleNode(*args):
    try:
        select( clear = True)
        select('RAmuscle')
        n = ls( sl = True)
        print n
        if len(n) != 0:
            RAmuscle = n[0]  
    except:
        fillMuscleList()
        RAmuscle = createNode('materialInfo', n = 'RAmuscle')
        addAttr( sn='ml', ln='muscle_list', dt = 'stringArray')
        setAttr('RAmuscle.ml', muscle_list)
        createCurves()

def createCurves():
        print muscle_list
        for muscle in muscle_list:
            vtx_list = RA_muscles_data.muscleVtx(muscle)
            vtx_pos_list = []
            i = 0
            for vtx in vtx_list:
                v = str(sex + '_base.vtx[' + str(vtx) + ']')
                pos = xform(v, t=True, query=True, ws=True)
                select(cl=True)
                j = sex + '__' + str(muscle) + '__' + str(i) + '__joint'
                joint(n=j, p=pos)
                select(cl=True)
                vtx_pos_list.append(pos)
                i = +1
            curve_name = str(muscle) + '_curve'
            curve( n=curve_name, p=vtx_pos_list )
            
            