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
from pylab import *
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
    print 'Canvas shape: ', canvas.shape

    # TODO: should we just start with the noise block and replicate it out?
    #       maybe we don't neeeed a CreateCanvas...

    # TODO: ATM, canvas size has to be a multiple of block size.
    #noise_block = CreateNoiseBlock(dim=dim,num_blocks=num_blocks)

    noise_block = ReadNoiseBlock()
    canvas = CopyNoiseBlock(canvas,noise_block,num_blocks)

    print 'Canvas2 shape: ',canvas.shape
    
    # pdb.set_trace()    
    # TODO: make function to convert depth to shift
    mask_panel = MakeMask('star.bmp') # default is circle.bmp
    decal_panel = GetShape(canvas, mask_panel, top_corner) # we really need to rename "shape"
    final_img = AssembleLayer(canvas, mask_panel, decal_panel, top_corner, primary_shift=10, shadow_shift=-slice_size) 

    print 'decal_panel shape: ',decal_panel.shape
    print 'mask_panel shape: ',mask_panel.shape
    print 'final_img shape: ',final_img.shape

    figure(),imshow(final_img)
    savefig('final_img.png',format='png',bbox_inches='tight')
    
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
    
    # by making a new array and copying?
    numask = numpy.ones([mask.shape[0], mask.shape[1], 4])
    numask[:,:,3] = 255
    numask[:,:,0:3] = mask

    return numask

# more like "fill template"
def GetShape(canvas, mask, position):

    figure(),imshow(canvas)
    savefig('gs_canvas.png',format='png',bbox_inches='tight')
    
    figure(),imshow(mask)
    savefig('gs_mask.png',format='png',bbox_inches='tight')

    print 'GetShape mask shape is: ', mask.shape

    ylen=mask.shape[0]
    xlen=mask.shape[1]

    # position is the top left corner
    ystart = position[0]
    xstart = position[1]

    yend = ystart + ylen
    xend = xstart + xlen

    cut_slice = numpy.zeros([ylen,xlen,3],dtype='uint8')
    cut_slice = canvas[ ystart:yend, xstart:xend, 0:3 ] * mask

    #cut_slice = numpy.zeros([ylen,xlen,4],dtype='uint8')
    #cut_slice[:,:,0:3] = canvas[ ystart:yend, xstart:xend, 0:3 ]
    #cut_slice[:,:,3] = 255

    #cut_slice = img[ ystart:yend, xstart:xend, 0:4 ]


    #figure(),imshow(cut_slice)
    #savefig('gs_cut_slice.png',format='png',bbox_inches='tight')

    return cut_slice

# put filled template on empty canvas-sized layer at the right place
def ShiftShape(img_size, mask_panel, cut_shape, insert_position, shift):

    canvas_with_shifted_shape = numpy.zeros([img_size[0],img_size[1],4],dtype='uint8')
    # paste the cut shape on the array of zeros, at the shifted position
    
    figure(),imshow(cut_shape)
    savefig('ss_cut_shape.png',format='png',bbox_inches='tight')

    ystart = insert_position[0]
    xstart = insert_position[1] + shift
    
    ########################
    # 24 JULY 2012: testing, because ShiftShape produces inverted colors in cutout when
    # shape is added to canvas.
    #
    cut_shape_ylen = cut_shape.shape[0]
    cut_shape_xlen = cut_shape.shape[1]

    xend = xstart + cut_shape_xlen
    yend = ystart + cut_shape_ylen

    print canvas_with_shifted_shape.shape # size is 3
    print cut_shape.shape

    canvas_with_shifted_shape[ ystart:yend, xstart:xend, 0:3 ] = cut_shape[:,:,0:3]

    figure(),imshow(cut_shape)
    savefig('ss_cut_shape.png',format='png',bbox_inches='tight')
    numpy.save('cut_shape.npy',cut_shape) 
    figure(),imshow(canvas_with_shifted_shape[ ystart:yend, xstart:xend, 0:3 ])
    savefig('ss_canvas_with_shifted_shape_panel.png',format='png',bbox_inches='tight')
    figure(),imshow(canvas_with_shifted_shape)
    savefig('BALALALALLALAL.png',format='png',bbox_inches='tight')
    numpy.save('canvas_with_shifted_shape.npy',canvas_with_shifted_shape)

    #
    ########################

    '''
    if (xstart < 0): # left shift
        cut_shape = cut_shape[:,-xstart:]
        #inv_template = inv_template[:,-xstart:]

    if (xstart + cut_shape.shape[1] > img_size[1]): # right shift
        cut_shape = cut_shape[:,0:img_size[1]-xstart]
        #inv_template = inv_template[:,0:img_size[1]-xstart]
    # TODO: Need to do the same for y-axis

    #figure(),imshow(mask_panel)
    #savefig('ss_mask_panel.png',format='png',bbox_inches='tight')

    #figure(),imshow(cut_shape)
    #savefig('ss_cut_shape.png',format='png',bbox_inches='tight')


    cut_shape_ylen = cut_shape.shape[0]
    cut_shape_xlen = cut_shape.shape[1]

    xend = xstart + cut_shape_xlen
    yend = ystart + cut_shape_ylen

    canvas_with_shifted_shape[ max(ystart,0):min(yend,img_size[0]),\
            max(xstart,0):min(xend,img_size[1]), 0:3 ] = cut_shape[:,:,0:3]

    '''

    return canvas_with_shifted_shape

# 'canvas' is indian food on canvas-sized layer
# we need a word for filled template, panel-sized - decalpanel
# also for filled template, canvas-sized - decallayer, "layer means 'canvas-sized'"
# what's a word for filled template?
def ApplyDecalLayerToCanvas(canvas, decal_layer):
    # This will return the canvas with decal applied at the shift location
    figure(),imshow(decal_layer)
    savefig('adltc_decal_layer.png',format='png',bbox_inches='tight')

    p = decal_layer!=0 
    canvas[p] = decal_layer[p]
    return canvas
    # the cheese slab is half a line now.

# TODO: change "position" to "top_corner"
# SHADOW SHIFT MUST BE NEGATIVE
def AssembleLayer(canvas, mask_panel, decal_panel, insert_position, primary_shift, shadow_shift):
    # xstart for shadow: (shift = shadow_shift + primary_shift)
    # for shadow_shift: shift is relative to primary shift
    
    #ShiftShape(img_size, cut_shape, insert_position, shift):
    
    img_size = canvas.shape

    primary_decal_layer = ShiftShape(img_size, mask_panel, decal_panel, insert_position, primary_shift)

    print 'primary_decal_layer.shape is: ',  primary_decal_layer.shape
    figure(),imshow(primary_decal_layer)
    savefig('ex_primary_decal_layer.png',format='png',bbox_inches='tight')
    
    canvas1 = ApplyDecalLayerToCanvas(canvas, primary_decal_layer)
    
    figure(),imshow(canvas1)
    savefig('ex_canvas1.png',format='png',bbox_inches='tight')


    shadow_decal_layer = ShiftShape(img_size, mask_panel, decal_panel, insert_position, shadow_shift + primary_shift)
    canvas2 = ApplyDecalLayerToCanvas(canvas1, shadow_decal_layer)


    figure(),imshow(shadow_decal_layer)
    savefig('ex_shadow_decal_layer.png',format='png',bbox_inches='tight')

    return canvas2

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
    
