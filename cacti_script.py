import bpy
import math
import random
import time
import bpycv
import cv2
import numpy as np
from mathutils import Euler, Color
from pathlib import Path


def randomly_rotate_object(obj_to_change):
    """ Applies a random rotation to an object
    """
    random_rot = (0, 0, random.random() * 2 * math.pi)
    obj_to_change.rotation_euler = Euler(random_rot, 'XYZ')
   

def randomly_change_color(material_to_change):
    """ Changes the Principled BSDF color of a material to a random color
    """
    color = Color()
    hue = random.random() * .2 # random between 0 and .2
    saturation = random.random() * .6 + .2 # random between .2 and .8
    color.hsv = (hue, saturation, 1)
    rgba = [color.r, color.g, color.b, 1]
    material_to_change.node_tree.nodes["Principled BSDF"].inputs[0].default_value = rgba
    
def randomly_set_camera_position():
    # Set the circular path position (0 to 100)
    bpy.context.scene.objects['CameraContainer'].constraints['Follow Path'].offset = random.random() * 100
    
    # Set the arc path position (0 to -100, not sure why, to be honest)
    bpy.context.scene.objects['CircleContainer'].constraints['Follow Path'].offset = random.random() * -100

# Object names to render
cacti_names = ['Empty', 'Bob', 'Lancy']
obj_count = len(cacti_names)

# Number of images to generate of each object for each split of the dataset
# Example: ('train', 100) means generate 100 images each of one name in cacti_names resulting in 300 training images
obj_renders_per_split = [('train', 3)]
#obj_renders_per_split = [('train', 500), ('val', 120), ('test', 200)]

# Output path
output_path = Path('/Users/i52/Downloads/tmp')
output_path_seg = Path('/Users/i52/Downloads/tmp/segmentation')

# For each dataset split (train/val/test), multiply the number of renders per object by
# the number of objects. Then compute the sum.
# This will be the total number of renders performed.
total_render_count = sum([obj_count * r[1] for r in obj_renders_per_split])

# Set all objects to be hidden in rendering
for name in cacti_names:
    if name != 'Empty':
        bpy.context.scene.objects[name].hide_render = True
    
# Tracks the starting image index for each object loop
start_idx = 0

# Keep track of start time (in seconds)
start_time = time.time()

# Loop through each split of the dataset
for split_name, renders_per_object in obj_renders_per_split:
    print(f'Starting split: {split_name} | Total renders: {renders_per_object * obj_count}')
    print('=============================================')
    
    # Loop through the objects by name
    for obj_name in cacti_names:
        print(f'Starting object: {split_name}/{obj_name}')
        print('.............................................')
        # Get the next object and make it visible
        if obj_name != 'Empty':
            obj_to_render = bpy.context.scene.objects[obj_name]
            obj_to_render.hide_render = False
        
        # Loop through all image renders for this object
        for i in range(start_idx, start_idx + renders_per_object):
            # Change the object
            if obj_name != 'Empty':
                rotated_object = bpy.context.scene.objects[obj_name]
                randomly_rotate_object(rotated_object)
            randomly_set_camera_position()
            # randomly_change_color(obj_to_render.material_slots[0].material)
            
            # Log status
            print(f'Rendering image {i + 1} of {total_render_count}')
            seconds_per_render = (time.time() - start_time) / (i + 1)
            seconds_remaining = seconds_per_render * (total_render_count - i - 1)
            print(f'Estimated time remaining: {time.strftime("%H:%M:%S", time.gmtime(seconds_remaining))}')
            
            # Update file path and render
            bpy.context.scene.render.filepath = str(output_path / split_name / obj_name / f"{str(i).zfill(6)}.png")
            #bpy.context.space_data.params.filename = f"{str(i).zfill(6)}.png"
            bpy.ops.render.render(write_still=True)

            # add the segmentation
            if obj_name != 'Empty':
                #obj = bpy.context.active_object
                obj = bpy.context.scene.objects[obj_name]       #有问题 直接不渲了 很离谱
                # set each instance a unique inst_id, which is used to generate instance annotation.
                obj["inst_id"] = 50000      # this number is the test best visible value, dont know why
                # render image, instance annoatation and depth in one line code
                result = bpycv.render_data()
                # # save result
                # visualization inst_rgb_depth for human
                cv2.imwrite(str(output_path_seg / split_name / obj_name / f"{str(i).zfill(6)}-vis(inst_rgb_depth).jpg"), result.vis()[..., ::-1])
                
                # save instance map as 16 bit png
                # the value of each pixel represents the inst_id of the object to which the pixel belongs
                cv2.imwrite(str(output_path_seg / split_name / obj_name / f"{str(i).zfill(6)}inst.png"), np.uint16(result["inst"]))

            
        if obj_name != 'Empty':
            # Hide the object, we're done with it
            obj_to_render.hide_render = True
        
        # Update the starting image index
        start_idx += renders_per_object

# Set all objects to be visible in rendering
for name in cacti_names:
    if name != 'Empty':
        bpy.context.scene.objects[name].hide_render = False