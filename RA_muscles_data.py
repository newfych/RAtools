muscle_list = ['l_bicep']
muscle_vtx = {'l_bicep_vtx':[6290,6559,6558,6556]}
def muscleList(*args):
    return muscle_list 
    
def muscleVtx(name):
    vtx = muscle_vtx[str(name)+'_vtx']
    return vtx
    