#PyEye.py

"""
1. Create canvas (600 x 250)
2. Create noise block (default pattern, can take input) (150 x 250)
3. Copy noise block and fill canvas
4. Copy and paste a shape (<= width of noise block)
5. Move shape 10 pixels to the right
6. Copy shape, move width of noise block to the left.
"""

import matplotlib.pyplot as plt
import numpy
from PIL import Image
#import pdb

def main(dim=(250,600)): # strange how it makes you put it in y,x
    num_blocks = 4    
    slice_size = dim[1]/num_blocks

    top_corner = ( 0, (dim[1] - slice_size)/2 - 50 )
    # TODO: actually fix the shadow.  Minus 50 just shifts the image
    # enough so the shadow gets pushed off.

    canvas = CreateCanvas(dim=dim)

    # TODO: should we just start with the noise block and replicate it out?
    #       maybe we don't neeeed a CreateCanvas...

    # TODO: ATM, canvas size has to be a multiple of block size.
    #noise_block = CreateNoiseBlock(dim=dim,num_blocks=num_blocks)

    noise_block = ReadNoiseBlock()
    canvas = CopyNoiseBlock(canvas,noise_block,num_blocks)
    
    # pdb.set_trace()    
    # TODO: make function to convert depth to shift
    mask_panel = MakeMask() # default is circle.bmp
    decal_panel = GetShape(canvas, mask_panel, top_corner) # we really need to rename "shape"
    final_img = AssembleLayer(canvas, mask_panel, decal_panel, top_corner, primary_shift=10, shadow_shift=-slice_size) 
    
    return final_img
    # TODO: write out image to file

def CreateCanvas(dim):
    a=numpy.zeros([dim[0],dim[1],4],dtype='uint8')
    return a

def ReadNoiseBlock():
    img = Image.open('noisy_pattern2.png')
    #img = Image.open('grid.png')
    img = numpy.array(img)
    # TODO: maybe add Gaussian noise? (numpy.random.normal)
    return img

def CopyNoiseBlock(img, noise_block, num_blocks): # maybe call this ReplicateNoiseBlock ?
    final = img.copy()
    # final = img
    for i in range(num_blocks):
        size = 150
        start = i * size
        final[:,start:size+start,:]=noise_block
    return final

def MakeMask(maskfile='circle.bmp'):
    # read the img file
    mask = Image.open(maskfile)
    mask = numpy.array(mask) > (255/2) # super simple comparator
    return mask

# more like "fill template"
def GetShape(img, mask, position):
    ylen=mask.shape[0]
    xlen=mask.shape[1]


    # position is the top left corner
    ystart = position[0]
    xstart = position[1]

    yend = ystart + ylen
    xend = xstart + xlen

    cut_slice = numpy.zeros([ylen,xlen,4],dtype='uint8')
    cut_slice[:,:,0:3] = img[ ystart:yend, xstart:xend, 0:3 ] * mask

    cut_slice[:,:,3] = 255

    return cut_slice

# put filled template on empty canvas-sized layer at the right place
def ShiftShape(img_size, mask_panel, cut_shape, insert_position, shift):
    canvas_with_shifted_shape = numpy.zeros(img_size)
    # paste the cut shape on the array of zeros, at the shifted position

    cut_shape_primary=cut_shape.copy()

    inv_template = numpy.invert(mask_panel)    
    inv_template_primary = inv_template.copy()

    ystart = insert_position[0]
    xstart = insert_position[1] + shift

    if (xstart < 0): # left shift
        cut_shape_shadow = cut_shape[:,-xstart:]
        inv_template_shadow = inv_template[:,-xstart:]

    if (xstart + cut_shape.shape[1] > img_size[1]): # right shift
        cut_shape_primary = cut_shape[:,0:img_size[1]-xstart]
        inv_template_primary = inv_template[:,0:img_size[1]-xstart]
    # TODO: Need to do the same for y-axis

    cut_shape_ylen = cut_shape.shape[0]
    cut_shape_xlen = cut_shape.shape[1]

    xend = xstart + cut_shape_xlen
    yend = ystart + cut_shape_ylen

    canvas_with_shifted_shape[ max(ystart,0):min(yend,img_size[0]),\
            max(xstart,0):min(xend,img_size[1]), 0:3 ] = cut_shape[:,:,0:3]

    return canvas_with_shifted_shape

# 'canvas' is indian food on canvas-sized layer
# we need a word for filled template, panel-sized - decalpanel
# also for filled template, canvas-sized - decallayer, "layer means 'canvas-sized'"
# what's a word for filled template?
def ApplyDecalLayerToCanvas(canvas, decal_layer):
    # This will return the canvas with decal applied at the shift location
    p = decal_layer!=0 
    canvas[p] = decal_layer[p]
    return canvas
    # the cheese slab is half a line now.

# TODO: change "position" to "top_corner"
# SHADOW SHIFT MUST BE NEGATIVE
def AssembleLayer(canvas, mask_panel, decal_layer, insert_position, primary_shift, shadow_shift):
    # xstart for shadow: (shift = shadow_shift + primary_shift)
    # for shadow_shift: shift is relative to primary shift
    
    #ShiftShape(img_size, cut_shape, insert_position, shift):
    
    img_size = canvas.shape
    primary_decal_layer = ShiftShape(img_size, mask_panel, decal_layer, insert_position, primary_shift)
    canvas = ApplyDecalLayerToCanvas(canvas, primary_decal_layer)
    shadow_decal_layer = ShiftShape(img_size, mask_panel, decal_layer, insert_position, shadow_shift + primary_shift)
    canvas = ApplyDecalLayerToCanvas(canvas, shadow_decal_layer)
    return canvas

    # 1. get primary decal_layer (tells ShiftShape how much to shift)
    # 1b. apply decal layer to canvas
    # 2. get shadow decal_layer (tells ShiftShape how much to shift)
    # 2b. apply decal layer to canvas
    # 3. Rinse, repeat.


if __name__=="__main__":
    p=main()
    print 'test'
    #plt.figure(),plt.imshow(p)
    
    fig = plt.figure()
    ax = plt.subplot(111)
    plt.imshow(p)
    
