#PyEye.py

import matplotlib.pyplot as plt
from pylab import *
import numpy
from PIL import Image


#import pdb # TODO: remove me

def moving():
    for i in range(40):
        main(dist_from_middle = i)

def main(dim=(250,600), dist_from_middle = 50, bg_file='noisy_pattern2.png', mask_file='circle.bmp', out_file_name='animated', out_file_type='png'):
# NOTE: strange how it makes you put it in y,x

    canvas = CreateBackground(noisefile=bg_file)
    
    # TODO: make function to convert depth to shift
    mask_panel = MakeMask(mask_file) # default is circle.bmp


    # TODO: this uses the mask for the panel. they're the same for now, but no guarantee
    # TODO: when this goes OO, we can easily grab the panel's size prop
    # TODO: figure out a way to not need this...
    panel_size = mask_panel.shape
    slice_size = panel_size[1]

    top_corner = ( 0, (dim[1] - slice_size)/2 - dist_from_middle )
    #top_corner = ( 0, (dim[1] - slice_size)/2 - 50 )
    decal_panel = GetShape(canvas, mask_panel, top_corner) # TODO: we really need to rename "shape"
    final_img = AssembleLayer(canvas, decal_panel, top_corner, primary_shift=10, shadow_shift=-slice_size) 

    figure(),imshow(final_img)
    #savefig(out_file_name+'1.'+out_file_type,format=out_file_type,bbox_inches='tight')
    savefig(out_file_name + '_%u'%(dist_from_middle)+'.'+out_file_type,format=out_file_type,bbox_inches='tight')

    '''
    #can I make a second picture on the thing?
    mask_panel = MakeMask('star.bmp')
    top_corner = ( 0, (dim[1] - slice_size)/2 -30 )
    decal_panel = GetShape(final_img, mask_panel, top_corner) # TODO: we really need to rename "shape"
    final_img = AssembleLayer(final_img, decal_panel, top_corner, primary_shift=10, shadow_shift=-slice_size)         
    figure(),imshow(final_img)
    savefig(out_file_name+'2.'+out_file_type,format=out_file_type,bbox_inches='tight')
    '''    

    return final_img


def CreateBackground(noisefile, num_blocks = 4):
    background_panel = ReadNoiseBlock(noisefile)
    
    bgs = background_panel.shape
    dim = (bgs[0], bgs[1] * num_blocks)
    
    canvas = CreateCanvas(dim)
    canvas = CopyNoiseBlock(canvas, background_panel, num_blocks)

    return canvas


def CreateCanvas(dim):
    # a=numpy.zeros([dim[0],dim[1],4],dtype='uint8')
    a=numpy.zeros([dim[0],dim[1],3],dtype='uint8') # gs no aplpha
    return a

def ReadNoiseBlock(noisefile):
    img = Image.open(noisefile)
    img = numpy.array(img,dtype='uint8')
    img = img[:,:,0:3] # gs no alpha

    return img

def CopyNoiseBlock(img, background_panel, num_blocks): # maybe call this ReplicateNoiseBlock ?
    final = img.copy()
    for i in range(num_blocks):
        size = 150
        start = i * size
        final[:,start:size+start,:]=background_panel
    return final

def MakeMask(maskfile='circle.bmp'):
    mask = Image.open(maskfile)

    #figure(),imshow(mask)
    #savefig('mm_mask.png',format='png',bbox_inches='tight')

    mask = numpy.array(mask) > (255/2) # super simple comparator
    mask = mask!=0
    #print 'mm: masktype is ',mask.dtype
    ### 27 JULY 2012 6:37am (probably CDT): THIS BOOL FIXED IT!  BL

    #figure(),imshow(mask)
    #savefig('mm_mask2.png',format='png',bbox_inches='tight')

    return mask

# more like "fill template"
def GetShape(canvas, mask, position):

    #print mask
    #print mask.dtype
    #figure(),imshow(mask)
    #savefig('gs_mask.png',format='png',bbox_inches='tight')

    ylen=mask.shape[0]
    xlen=mask.shape[1]

    # position is the canvas location of top corner of decal_panel
    ystart = position[0]
    xstart = position[1]

    yend = ystart + ylen
    xend = xstart + xlen

    cut_slice = numpy.zeros([ylen,xlen,3],dtype='uint8')
    cut_slice = canvas[ ystart:yend, xstart:xend, 0:3 ] * mask

    return cut_slice

# put filled template on empty canvas-sized layer at the right place
def ShiftShape(img_size, cut_shape, insert_position, shift):

    # canvas_with_shifted_shape = numpy.zeros([img_size[0],img_size[1],4],dtype='uint8')
    canvas_with_shifted_shape = numpy.zeros([img_size[0],img_size[1],3],dtype='uint8') # gs no alpha
    # paste the cut shape on the array of zeros, at the shifted position

    ystart = insert_position[0]
    xstart = insert_position[1] + shift
    
    '''
    ########################
    # 24 JULY 2012: testing, because ShiftShape produces inverted colors in cutout when
    # shape is added to canvas.
    #
   cut_shape_ylen = cut_shape.shape[0]
    cut_shape_xlen = cut_shape.shape[1]

    xend = xstart + cut_shape_xlen
    yend = ystart + cut_shape_ylen

    print 'ss canvas_with_shifted_shape.shape: ', canvas_with_shifted_shape.shape # size is 4
    print 'ss cut_shape.shape: ', cut_shape.shape #size is 3

    print ystart, yend
    print xstart, xend
    canvas_with_shifted_shape[ ystart:yend, xstart:xend, 0:3 ] = cut_shape
    print canvas_with_shifted_shape[:,:,3]

    #Bev added the following on 25 July 2012 on an airplane between Baltimore and Houston
    #It fixes one problem (the canvas-being-blank problem)
    canvas_with_shifted_shape[:,:,3] = 255 


    figure(),imshow(cut_shape)
    savefig('ss_cut_shape2.png',format='png',bbox_inches='tight')
    numpy.save('cut_shape.npy',cut_shape) 

    figure(),imshow(canvas_with_shifted_shape[ ystart:yend, xstart:xend, 0:3 ])
    savefig('ss_canvas_with_shifted_shape_panel.png',format='png',bbox_inches='tight')

    figure(),imshow(canvas_with_shifted_shape)
    savefig('ss_canvas_with_shifted_shape.png',format='png',bbox_inches='tight')
    savefig('BALALALALLALAL.png',format='png',bbox_inches='tight')
    numpy.save('canvas_with_shifted_shape.npy',canvas_with_shifted_shape)
    #
    ########################
    '''

    if (xstart < 0): # shadow
        cut_shape = cut_shape[:,-xstart:]
        #inv_template = inv_template[:,-xstart:]

    if (xstart + cut_shape.shape[1] > img_size[1]): # primary
        cut_shape = cut_shape[:,0:img_size[1]-xstart]
        #inv_template = inv_template[:,0:img_size[1]-xstart]
    # TODO: Need to do the same for y-axis

    cut_shape_ylen = cut_shape.shape[0]
    cut_shape_xlen = cut_shape.shape[1]

    xend = xstart + cut_shape_xlen
    yend = ystart + cut_shape_ylen

    canvas_with_shifted_shape[ max(ystart,0):min(yend,img_size[0]),\
            max(xstart,0):min(xend,img_size[1]), 0:3 ] = cut_shape
    # canvas_with_shifted_shape[:,:,3] = 255  # gs no alpha

    figure(),imshow(canvas_with_shifted_shape)
    savefig('ss_canv_w_shift_shape.png',format='png',bbox_inches='tight')

    return canvas_with_shifted_shape

# 'canvas' is indian food on canvas-sized layer
# we need a word for filled template, panel-sized - decalpanel
# also for filled template, canvas-sized - decallayer, "layer means 'canvas-sized'"
# what's a word for filled template?
def ApplyDecalLayerToCanvas(canvas, decal_layer):
    # This will return the canvas with decal applied at the shift location
    p = decal_layer!=0 # bunch of true/false values
    #p = numpy.nonzero(decal_layer==0)

    print p.shape,canvas.shape,decal_layer.shape
    for i in range(canvas.shape[0]):
        for j in range(canvas.shape[1]):
            if p[i,j,0]: canvas[i,j,:] = decal_layer[i,j,:]

    #figure(500),imshow(p)
    #canvas = canvas * p
    #pdb.set_trace()
    #canvas[p] = decal_layer[p]
    return canvas

# SHADOW SHIFT MUST BE NEGATIVE
def AssembleLayer(canvas, decal_panel, insert_position, primary_shift, shadow_shift):
    # xstart for shadow: (shift = shadow_shift + primary_shift)
    # for shadow_shift: shift is relative to primary shift
        
    img_size = canvas.shape
    primary_decal_layer = ShiftShape(img_size, decal_panel,\
                                         insert_position,\
                                         primary_shift)
    canvas1 = ApplyDecalLayerToCanvas(canvas, primary_decal_layer)


    shadow_decal_layer = ShiftShape(img_size, decal_panel,\
                                        insert_position,\
                                        shadow_shift + primary_shift)
    canvas2 = ApplyDecalLayerToCanvas(canvas1, shadow_decal_layer)
    return canvas2

if __name__=="__main__":
    #p=main(bg_file='grid.png')
    p=main(bg_file='noisy_pattern.png')
    moving()
    #p=main(mask_file='star.bmp',bg_file='noisy_pattern.png')
    print 'test'
    #plt.figure(),plt.imshow(p)
    
    fig = plt.figure()
    ax = plt.subplot(111)
    plt.imshow(p)
    
