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

    img = CreateCanvas(dim=dim)

    # TODO: should we just start with the noise block and replicate it out?
    #       maybe we don't neeeed a CreateCanvas...

    # TODO: ATM, canvas size has to be a multiple of block size.

    noise_block = CreateNoiseBlock(dim=dim,num_blocks=num_blocks)
    img = CopyNoiseBlock(img,noise_block,num_blocks)
    
    # pdb.set_trace()    
    # TODO: make function to convert depth to shift

    template = MakeMask()
    shape = GetShape(img,mask=template,position=top_corner) # we really need to rename "shape"

    final_img = AssembleLayer(img, template=template, cut_shape=shape, top_corner=top_corner,\
                                  primary_shift=10, shadow_shift=-slice_size) 

    return final_img
    # TODO: write out image to file

def CreateCanvas(dim):
    a=numpy.zeros([dim[0],dim[1],4],dtype='uint8')
    return a

def CreateNoiseBlock(dim, num_blocks):
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

def MakeMask():
    # read the img file
    mask = Image.open('star.bmp') # TODO: extract config.
    mask = numpy.array(mask) > (255/2) # super simple comparator
    return mask

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

# TODO: change "position" to "top_corner"
# SHADOW SHIFT MUST BE NEGATIVE
def AssembleLayer(img, template, cut_shape, top_corner, primary_shift, shadow_shift):

    cut_shape_shadow=cut_shape.copy()
    cut_shape_primary=cut_shape.copy()

    inv_template = numpy.invert(template)    
    inv_template_shadow = inv_template.copy()
    inv_template_primary = inv_template.copy()


    primary_ystart = top_corner[0]
    shadow_ystart  = top_corner[0]

    primary_xstart = top_corner[1] + primary_shift 
    shadow_xstart  = top_corner[1] + shadow_shift + primary_shift

    #if (shadow_xstart <= 0): 
    #    shadow_xstart=0

    if (shadow_xstart < 0):
        cut_shape_shadow = cut_shape[:,-shadow_xstart:]
        inv_template_shadow = inv_template[:,-shadow_xstart:]

    if (primary_xstart + cut_shape.shape[1] > img.shape[1]):
        cut_shape_primary = cut_shape[:,0:img.shape[1]-primary_xstart]
        inv_template_primary = inv_template[:,0:img.shape[1]-primary_xstart]

    cut_shape_ylen = cut_shape.shape[0]
    cut_shape_xlen = cut_shape.shape[1]

    # "dough", "cutter", "cookie" ???

    primary_xend = primary_xstart + cut_shape_xlen
    shadow_xend = shadow_xstart + cut_shape_xlen

    primary_yend = primary_ystart + cut_shape_ylen
    shadow_yend = shadow_ystart + cut_shape_ylen

    # We'll probably have to completely redo this section when we're doing multiple layers
    # Do we cut out the next depth level from the merged image or the original?

    canvas = img.copy()
    #canvas = numpy.ones(img.shape)

    # cheese = vegan_cheese
    #inv_template = numpy.invert(template)

    primary_cheese_slab = GetShape(canvas,inv_template_primary,position=(primary_ystart,primary_xstart))

    canvas[ primary_ystart:min(primary_yend,img.shape[0]),\
            primary_xstart:min(primary_xend,img.shape[1]), 0:3 ] =\
            primary_cheese_slab[:,:,0:3] + cut_shape_primary[:,:,0:3]

    shadow_cheese_slab  = GetShape(canvas,inv_template_shadow,position=(shadow_ystart,shadow_xstart))
    canvas[ max(shadow_ystart,0):shadow_yend,\
            max(shadow_xstart,0):shadow_xend, 0:3 ] =\
            shadow_cheese_slab[:,:,0:3] + cut_shape_shadow[:,:,0:3]

    return canvas

if __name__=="__main__":
   p=main()
   print 'test'
   plt.figure(),plt.imshow(p)
