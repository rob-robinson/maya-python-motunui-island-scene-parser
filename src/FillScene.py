import maya.cmds as cmds
import os
import json
import string
from sys import platform

class FillScene:
    config = {
        "base_platform": {
            "darwin": "/Users/robrobinson/Documents/maya/projects/default/assets/island",
            "win32": "C:/Users/robro/Documents/maya/projects/MoanaScene/assets/island-basepackage-v1.1/island",
            "linux": ""
        },
        "elements" : [
            'isBayCedarA1',
            'isBeach',
            'isCoastline',
            'isCoral',
            'isDunesA',
            'isDunesB',
            'isGardeniaA',
            'isHibiscus',
            'isHibiscusYoung',
            'isIronwoodA1',
            'isIronwoodB',
            'isKava',
            'isLavaRocks',
            'isMountainA',
            'isMountainB',
            'isNaupakaA',
            'isPalmDead',
            'isPalmRig',
            'isPandanusA',
            'osOcean'
        ]
    }

    baseDir = ""
    current_element = ""

    def __init__(self):

        # get set up for the proper workstation ...
        # TODO: extract this into a config that can be imported from file

        # if platform == "linux" or platform == "linux2":
        #     pass
        #
        # elif platform == "darwin":
        #     self.baseDir = config["base_platform"]["darwin"]
        #
        # elif platform == "win32":
        #     self.baseDir = config["base_platform"]["win32"]

        self.baseDir = self.config["base_platform"][platform]

        # only run a subset of elements, the ommitted ones don't yet work ...

        for el_index in [ 1, 2, 3, 4, 5, 12, 13, 14, 16, 17]:

            # set global notification of the current working element
            self.current_element = self.config["elements"][el_index]

            # import items from element
            self.create_one_set_of_elements(self.current_element)

    def create_one_set_of_elements(self, element):

        jsonDir = os.path.join(os.path.abspath(self.baseDir + "/json"), element)

        # read the json file that lists the objects to create:
        base_element_dict_from_json = self.readJsonFile(os.path.join(jsonDir, element + ".json"))

        # import the objects:
        self.import_obj_file(base_element_dict_from_json["geomObjFile"], "", element)

        # place the base object where it is supposed to be located:
        if cmds.objExists(str(base_element_dict_from_json['name'] + "_default_grp")):
            # transform matrix location is located in the json file
            cmds.xform(str(base_element_dict_from_json['name'] + "_default_grp"), matrix=base_element_dict_from_json["transformMatrix"])
        else:
            pass

        # read the materials json file
        materialDict = self.readJsonFile(os.path.join(jsonDir, "materials.json"))

        # make the textures from materialDict
        self.make_textures(materialDict)

        # fix hierarchy:
        # get_hier_setup(base_element_dict_from_json["geomObjFile"])

        # get a list of elements / objects to be created as copies:
        copies = base_element_dict_from_json["instancedCopies"] if "instancedCopies" in base_element_dict_from_json else []

        # create each copy
        for instance_copy in copies:

            print(" " * 60)
            print("-" * 60)
            print(" " * 60)

            print("-*-*- single instance copy:", str(instance_copy), "listed name:", str(copies[instance_copy]["name"]))

            if copies[instance_copy]["geomObjFile"]:
                print("  == get object:" + str(copies[instance_copy]["geomObjFile"]) + " with namespace:" + str(copies[instance_copy]["name"]))
                self.import_obj_file(str(copies[instance_copy]["geomObjFile"]), str(copies[instance_copy]["name"]), "")
            else:
                print('copies[instance_copy]["geomObjFile"] did not exist for: ' + instance_copy)

            # move copy to proper location:
            if cmds.objExists(str(copies[instance_copy]["name"] + "_grp")):
                print("    +++ get matrix for:" + str(copies[instance_copy]["name"]) + " : " + str(copies[instance_copy]["transformMatrix"]))
                cmds.xform(str(copies[instance_copy]["name"] + "_grp"), matrix=copies[instance_copy]["transformMatrix"])
            else:
                print("    --- name did not exist ...:", str(copies[instance_copy]["name"]))

            # import heir
            # get_hier_setup(copies[instance_copy]["geomObjFile"])

        # for xgen:
        # if "instancedPrimitiveJsonFiles" in base_element_dict_from_json:
        #     for primitive, ipDict in base_element_dict_from_json["instancedPrimitiveJsonFiles"].iteritems():
        #         #printPrimitiveInfo(primitive, ipDict)
        #         print(primitive)

        self.assign_textures()



    def readJsonFile(self, jsonFile):
        """
        Wrapper script to import json file as dict.
        :param jsonFile: file as string
        :return: dict
        """
        with open(os.path.abspath(jsonFile), "r") as jf:
            jsonDict = json.load(jf)

        return jsonDict if jsonDict else {}

    # def printPrimitiveInfo(self, primitive, pDict):
    #
    #     global jsonDir
    #     global element
    #
    #     if pDict["type"] == "archive":
    #
    #         primDict = self.readJsonFile(os.path.join(jsonDir, element + "_" + primitive + ".json"))
    #
    #         for archive, instances in primDict.iteritems():
    #
    #             print '\t'.join([primitive, "primitive archive", archive, str(len(instances)) ])
    #
    #     elif pDict["type"] == "curve":
    #
    #         curveDict = self.readJsonFile(os.path.join(jsonDir, element + "_" + primitive + ".json"))
    #         print '\t'.join([primitive, "primitive curve", "", "", "", str(len(curveDict))])
    #
    #     elif pDict["type"] == "element":
    #
    #         variantDict = self.readJsonFile(os.path.join(jsonDir, element + "_" + primitive + ".json"))
    #         for var in pDict["variants"]:
    #             instances = len(variantDict[var])
    #             print '\t'.join([primitive, "primitive element", "See file info under %s %s" % (pDict["element"], var),"","","", str(instances)])

    def import_obj_file(self, geomObjFile, namespace, element):

        if namespace == '':

            cmds.file(  self.baseDir + '/' + geomObjFile,
                        type="OBJ",
                        namespace=element + "_default",
                        i=True,
                        groupReference=True,
                        groupName=element + "_default_grp"
                     )
        else:
            cmds.file(  self.baseDir + '/' + geomObjFile,
                        type="OBJ",
                        namespace=namespace,
                        i=True,
                        groupReference=True,
                        groupName=namespace + "_grp")

    def make_a_texture(self, base_object, ptex_object):

        texDir = os.path.join(os.path.abspath(self.baseDir + "/textures"), base_object)

        # ideally, the lambert view shader would be similar in color to the actual pxr_surface color for modeling
        lambert_shader = cmds.shadingNode('lambert', asShader=True, name=base_object + "_" + ptex_object + '_lambert')

        actual_shader = cmds.shadingNode('PxrSurface', asShader=True, name=base_object + "_" + ptex_object + '_pxr')

        actual_texture = cmds.shadingNode('PxrPtexture', asTexture=True, name=base_object + "_" + ptex_object + '_ptex')

        cmds.setAttr(base_object + "_" + ptex_object + '_ptex' + ".filename",
                     texDir + '/Color/' + ptex_object + '.ptx', type="string")

        cmds.connectAttr(actual_texture + '.resultRGB', actual_shader + '.diffuseColor')

        actual_shading_group = cmds.sets(r=True, nss=True, em=True, n=actual_shader + 'SG')

        cmds.connectAttr(actual_shader + '.outColor', actual_shading_group + '.rman__surface')

        cmds.connectAttr(lambert_shader + '.outColor', actual_shader + 'SG' + '.surfaceShader')

    def make_textures(self, in_json):

        for item in in_json:

            if in_json[item]["assignment"]:
                print(in_json[item]["assignment"])

                for tex in in_json[item]["assignment"]:
                    if str(tex[:2]) != 'xg' and 'archive' not in str(tex):
                        print(self.current_element + " . " + tex)
                        self.make_a_texture(self.current_element, tex)


    def assign_textures(self):

        # cmds.select(cmds.ls( 'pSphere*'))
        # try something like search for items like trunk, then have them emit face ids, and then attach the proper surface to them...

        print(cmds.select(cmds.ls('*:trunk*geo')))

        actionable_items = cmds.select(cmds.ls('*:trunk*geo'))

        print(actionable_items)

        for ai in actionable_items or []:
            cmds.setAttr(ai+'.rman_emitFaceIDs', 1)

        # setAttr "isPalmRig_default1:trunk0001_geoShape.rman_emitFaceIDs" 1;


    def get_hier_setup(geomObjFile):

        global baseDir

        # this function will likely need some updating ... it is supposed to do the following:
        # 1.) Read the .hier file for a given element type and parse into data variable
        # 2.) Determine is the parsed hier group name exists
        #    -- if it does exist, then place the proper object into it
        #    -- if it does not exist, then create the group, and then place the proper object into it ...

        hier_file = string.replace(geomObjFile, '.obj', '.hier')

        with open(baseDir + '/' + hier_file, "r") as read_file:

            data = json.load(read_file)

        for base_geo in data.keys():

            layers = data[base_geo].split('|')

            # remove blank layers
            if layers[0] == u'':
                del layers[0]

            for i in range(0, len(layers)):
                #
                # print("------")
                # print("in number " + str(i) + ": " + str(layers[i]))
                # print('\'|\'.join(layers[0:i+1])' + " : " + '|'.join(layers[0:i+1]))
                # print("------")

                print(str('|'.join(layers[0:i+1])), ' and ', str('|'.join(layers[0:i])))

                if cmds.objExists(str('|'.join(layers[0:i+1]))):

                    print(i, layers[i], ' obj exists, move on ' + str('|'.join(layers[0:i+1])))
                    # pass

                elif cmds.objExists(str('|'.join(layers[0:i]))):

                    print("Create layer " + str(layers[i]) + " with parent : (" + str('|'.join(layers[0:i])) + ')')

                    cmds.group(em=True, name=layers[i], parent=str('|'.join(layers[0:i])))

                else:

                    print(i, str(layers[i]), 'create base layer ' + str(layers[i]) + " because " + str('|'.join(layers[0:i+1])) + " and " + str('|'.join(layers[0:i])) + " does not exist")
                    cmds.group(em=True, name=str(layers[i]))

            if cmds.objExists(base_geo):

                cmds.parent(base_geo, str('|'.join(layers[0:i])))


# if __name__ == "__main__":
#     if main():
#         sys.exit(0)
#     sys.exit(1)

f = FillScene()
