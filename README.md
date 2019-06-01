# maya-python-motunui-island-scene-parser
Python playground for parsing and working with the Motunui island scene from WDAS :
( https://www.technology.disneyanimation.com/islandscene )

These parsing scripts have been created as a learning process by a programmer trying to learn more about how python can interact with Maya 2018.4 and Renderman 22.1. 

You are free to use them however you like. 

## How to use:

1. download the large zipped island scene [www.technology.disneyanimation.com/islandscene](https://www.technology.disneyanimation.com/islandscene) from [this link](http://datasets.disneyanimation.com/moanaislandscene/island-basepackage-v1.1.tgz)...

2. Unzip the file contents and note where the island directory is located

3. clone this repo

4. open src/FillScene.py and update the config.base_platform for the platform that you are using and paste the location of the island directory.  

5. from maya, open and run the script src/FillScene.py to import the items from the island directory into maya.

6. from maya, open and run the script src/activate_ptex_on_selection.py to activate the ptex faces and apply pixar shading groups to the elements.

7. there will be lots of feedback from steps 5 and 6 above. 

8. Once the scripts have run, you will need to add light to be able to render in renderman.

9. Good luck, and happy hacking :-)

## Known issues

* there are many issues with this setup...
* not all objects are imported. This was meant to be a learning experience for me to get the objects placed and adding shader groups.
* archive objects are not imported. items created with xgen or banzai were not imported because doing so would have taken hours ... 
* items will still have jagged edges when rendered. again this is because of the lack of wanting to burn down my computer ...
* defined cameras are not set.