
=============  What do the Blender and python script do =========

We used Blender to build several 3D models representing the cactus, set up light sources and scenes for them, and set up camera paths to render photos from different angles to simulate the real world photos. The script automatically rotates the cactus model, sets the camera to take photos in different locations, and renders and categorizes a specified number of photos. For each generated photo, the script also segmented them so that the cactus was in the foreground and labeled, and everything else was in the background and ignored. The advantage of this is that the script can automatically produce hundreds of images, saving the time needed to manually photograph the cactus and annotate the image. As long as you have the model, you can also generate new kinds of images for later precess.




The following steps show how to run the blender file on your computer to automatically generate a series of segmented cactus images.

============== Install and set up environment =================

1. Go to https://www.blender.org and download and version between Blender2.80 and Blender2.93. To find the previous versions, go to https://download.blender.org/release/  
The latest version is Blender3.1 when writing this readMe file. Just for reference, the blender file using here is been build on Blender3.0. However, to run the segmentation script, the version required is strict, the script needs to be run on version 2.8+ or 2.9+



2. Go to https://github.com/DIYer22/bpycv and install the 'bpycv' utils for generate segmented images. The issue that bpycv does not support Blender3.0+ has been known to contributors but has not been resolved as of this writing.


================= Open the blender file ======================

For MAC users:
1. Go to the Applications in Finder
2. Right click the Blender icon
3. Select 'Show Package Contents'
4. Contents -> MacOS -> Blender excitable file
5. Select the file 'cacti_dataset.blender' from the interface displayed inside the software

For Windows users:
1. Double click the Blender icon
2. Select the file 'cacti_dataset.blender' from the interface displayed inside the software
3. Find the 'Window' option in the menu bar at the top of the screen
4. Window -> toggle System Console


======================== Run script ==========================

1. Find the 'Scripting' option in the menu bar at the top of the screen.
2. You should see 'cacti_script.py' is already loaded, if not goto Text -> Open -> choose cacti_script.py
3. Change the output path to your own path in script line 46.
4. Click the play icon 'Run Script' and wait.
5. You will be able to see the output images in the file path you specified while it's generated.


==================== Q & A that might be helpful ================

Q: Why the output image is all purple/pink? 
A: The model representing the cacti are built with textures, you need to tell the blender render where to find these textures. Menu bar 'File' option -> external data -> finding missing files -> double click 'Lancy_tex' folder(which in its original state should be in the same folder as the blender file) -> right bottom button choose 'Find missing files'


Q: How to change the number of images generated?
A: In script 'cacti_script.py' line 42, change the number as you prefer. See the comments inside the file. You can do the change either inside the blender script window or change it outside the blender and change on the cacti_script.py. If you do it outside, use the 'Reload' under the 'Text' menu to reload your script.


Q: How to change the output images quality?
A: Go to the 'Properties' control panel on the right side of your blender window (short cut for MAC is shift+F7). Find the 'Render Properties' which has a camera icon. Change the number of samples to render for each pixel value in 'Sampling'->'Render' -> 'Samples'. The higher the number, the higher the quality of the image, but the time required to render increases as the rendering quality increases.


Q: How to change the output images size?
A: Go to the 'Properties' control panel on the right side of your blender window (short cut for MAC is shift+F7). Find the 'Output Properties' which has a printer icon. Change the number of horizontal and vertical pixels in the render image in 'Format'->'Resolution X / Y'.


Q: What to do if you do not need the annotation images just want the normal image?
A: You do not need to install the 'bpycv' and there is no limit to your Blender version. Comment out the part about adding segmentation in the script.










