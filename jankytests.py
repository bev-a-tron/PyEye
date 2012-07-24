#! /Users/administrator/pyth/bin/python
#PyEye_jankytests.py

'''
This will test stuff.
'''

import PyEye,numpy

def helper_GetCanvas():
    return PyEye.CreateCanvas(dim=(250,600))

def helper_GetNoiseBlock():
    return PyEye.ReadNoiseBlock()

def helper_GetFullBackground():
    canvas = helper_GetCanvas()
    noise_block = helper_GetNoiseBlock()
    return PyEye.CopyNoiseBlock(canvas,noise_block=noise_block,num_blocks=4)

def helper_GetMask():
    return PyEye.MakeMask('circle.bmp')

def test_CreateCanvas():
    img = helper_GetCanvas()

    img_shape_expected = (250,600,4)
    img_shape_okay = img.shape == img_shape_expected

    img_dtype_expected = 'uint8'
    img_dtype_okay = img.dtype == img_dtype_expected

    return img_shape_okay and img_dtype_okay

def test_CopyNoiseBlock():
    img = helper_GetFullBackground()
    noise_block = helper_GetNoiseBlock()

    panel1 = img[:,0:150,:]
    panel2 = img[:,150:300,:]
    panel3 = img[:,300:450,:]
    panel4 = img[:,450:600,:]

    panel_expected = noise_block
    
    return panel1.all() == panel2.all() == panel3.all() == panel4.all() == panel_expected.all()

def test_GetShape():
    img = helper_GetFullBackground()
    # mask = helper_GetMask()
    position = (0,0)

    noise_block = helper_GetNoiseBlock()

    shape_ones = PyEye.GetShape(img, numpy.ones([250,150,3]), position)
    shape_zeroes = PyEye.GetShape(img, numpy.zeros([250,150,3]), position)

    check_ones = shape_ones.all() == noise_block.all()
    check_zeroes = shape_zeroes.all() == numpy.zeros([250,150]).all()
    
    return check_ones and check_zeroes

def test_ShiftShape():
    
    return False

def test_AssembleLayer():
    return False

def MagicTest(function):
    lulu = eval('test_' + function + '()')    

    if lulu: result = 'Pass'
    else: result = 'Fail'
    print function + ' ' + result

if __name__ == "__main__":

    MagicTest('CreateCanvas')
    #MagicTest('ReadNoiseBlock')
    MagicTest('CopyNoiseBlock')
    #MagicTest('MakeMask')
    MagicTest('GetShape')
    MagicTest('ShiftShape')
    #MagicTest('AssembleLayer')    

'''
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
'''
