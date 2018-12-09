# Steps to success for this project:

## Level 01:

### Goals:

* Import items from the isLavaRocks ( isLavaRocks and isLavaRocks1 )
  * This includes understanding how the transformMatrix works for the base object, and instancedCopies which in this case is isLavaRocks1
* Create and apply pTex surfaces as pxrSurfaces

### Implementation:

* Start with json/isLavaRocks.json
  * transformMatrix sets the base location
  * Use the xform command to place the object cmds.xform('isLavaRocks', matrix=[transformMatrix])
  * geomObjFile specifies the .obj file for import
  * matFile sets the location of the material.json file for this .obj
  * name sets the name of the obj
  * instancedCopies describes copies of the object
    * instancedCopies have their own (transformMatrix, geomObjFile, matFile, name)
    * I think the transformMatrix for the instanced copy is relative to the base object ... but I am not 100% certain of this ...
    
### References:  
    