muscle_list = ['l_bicep']
muscle_vtx = {'l_bicep_vtx':[1,2,3]}
def muscleList(*args):
    return muscle_list 
    
def muscleVtx(name):
    vtx = muscle_vtx[str(name)+'_vtx']
    return vtx
    