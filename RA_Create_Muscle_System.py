from pymel.core import *

import RA_muscles_data
reload (RA_muscles_data)

muscle_list=[]  

def create(*args):
    importData()
    gender = radioCollection('ChooseGender', query=True, sl=True)
    print gender
    if gender == 'Female':
        importFile("C:/RAtools/Muscles_start_female.ma")
    else:
        print 'Not working yet'
    createMuscleNode()
        
def createMuscleNode(*args):
    try:
        select( clear = True)
        select('RAmuscle')
        n = ls( sl = True)
        if len(n) != 0:
            RAmuscle = n[0]  
            print 'node exists'
    except:
        RAmuscle = createNode('materialInfo', n = 'RAmuscle')
        global muscle_list
        muscle_list = RA_muscles_data.muscle_list[:]
        addAttr( sn='ml', ln='muscle_list', dt = 'stringArray')
        setAttr('RAmuscle.ml', muscle_list)
        createCurves()

def createCurves():
        print muscle_list