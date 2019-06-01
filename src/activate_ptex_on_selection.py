import maya.cmds as cmds

# result = cmds.ls(orderedSelection=True)

element_sets_to_run = [
#    ['isBeach', 'beach', 0, 0],
#    ['isCoastline', 'coastline0001_hi', 0, 0],
    ['isCoral', 'antler', 1, 75],
    ['isCoral', 'barnacle', 1, 113],
    ['isCoral', 'cauliflower', 1, 31],
    ['isCoral', 'clubbedfinger', 1, 862],
    ['isCoral', 'clubbedthumb_a', 1, 2],
    ['isCoral', 'clubbedthumb_b', 1, 2],
    ['isCoral', 'clubbedtthumb_c', 1, 2],
    ['isCoral', 'clubbedthumb_d', 1, 2],
    ['isCoral', 'coralmoss', 1, 13],
    ['isCoral', 'coralrock', 1, 74],
    ['isCoral', 'coralstone', 1, 25],
    ['isCoral', 'fingercoral', 1, 625],
    ['isCoral', 'knobbybrain', 1, 16],
    ['isCoral', 'ricecoral', 1, 17],
    ['isCoral', 'seaweed', 1, 326],
    ['isCoral', 'starhornplate', 1, 121],
    ['isCoral', 'starhornstem', 1, 5],
#    ['isDunesA', 'dirt', 1, 3],
#    ['isDunesA', 'roots', 1, 753],
#    ['isDunesA', 'topsoil', 1, 2],
#    ['isDunesB', 'dune', 1, 3],
    ['isLavaRocks', 'rockfacebg', 1, 2],
    ['isLavaRocks', 'rockfacemain', 1, 2],
    ['isLavaRocks1', 'lavarocks', 4, 7],
    ['isLavaRocks1', 'rockfacebg', 1, 2],
    ['isLavaRocks1', 'rockfacemain', 1, 2],
    ['isLavaRocks1', 'rocksm', 1, 6],
#    ['isMountainA', 'mountain', 0, 0],
#    ['isMountainB', 'mountainb', 1, 6],
#    ['isMountainB', 'mountbring', 0, 0],
    ['isPalmDead', 'rootball', 1, 2],
    ['isPalmDead', 'trunk', 1, 2],
    ['isPalmRig', 'deadstrand', 1, 27],    
    ['isPalmRig', 'frondspine', 1, 27],
    ['isPalmRig', 'roots', 0, 0],        
    ['isPalmRig', 'sheatha', 1, 4],    
    ['isPalmRig', 'sheathb', 1, 4],
    ['isPalmRig', 'sheathc', 1, 6],        
    ['isPalmRig', 'sheathd', 1, 4],    
    ['isPalmRig', 'sheathe', 1, 6],    
    ['isPalmRig', 'sheathf', 1, 6],    
    ['isPalmRig', 'sheathg', 1, 3],    
    ['isPalmRig', 'sheathh', 1, 2],    
    ['isPalmRig', 'sheathi', 1, 2],    
    ['isPalmRig', 'skirt', 0, 0],    
    ['isPalmRig', 'trunk', 1, 2]  
]

for element_set in element_sets_to_run:

    el = element_set[0]

    for i in range(element_set[2],element_set[3]):

        if element_set[2] == 0 and element_set[3] == 0:
            item = element_set[1] + "_geo"
        else:
            item = element_set[1] + "%04d_geo" % i

        result = cmds.ls(el + "*:" + item)
    
        for objectName in result:
            print("update:" + str(objectName))
            cmds.setAttr(objectName + ".rman_emitFaceIDs", True)
            cmds.select(objectName)

            if cmds.objExists(el + '_' + item + '_pxrSG'):
                cmds.sets(forceElement=el + '_' + item + '_pxrSG')
            else:
                print("item: " + el + '_' + item + '_pxrSG' + " does not exist ...")
