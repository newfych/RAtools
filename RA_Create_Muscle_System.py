from pymel.core import *

muscle__list = []

def create(*args):
    print 'create'
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
        print 'node created'
        addAttr( sn='ml', ln='muscle_list', dt = 'stringArray')
        setAttr('RAmuscle.ml', muscle_list)
