#! /Users/administrator/pyth/bin/python
#PyEye_jankytests.py

'''
This will test stuff.
'''

import PyEye

def test_CreateCanvas():
    img = PyEye.CreateCanvas(dim=(200,600))

    img_shape_expected = (200,600,4)
    img_shape_okay = img.shape == img_shape_expected

    img_dtype_expected = 'uint8'
    img_dtype_okay = img.dtype == img_dtype_expected

    return img_shape_okay and img_dtype_okay

def test_ReadNoiseBlock():
    noise_block = PyEye.ReadNoiseBlock()
    return False

'''
def test_CopyNoiseBlock():

def test_MakeMask():

def test_GetShape():

def test_AssembleLayer():
'''    

def MagicTest(function):
    lulu = eval('test_' + function + '()')    

    if lulu: result = 'Pass'
    else: result = 'Fail'
    print function + ' ' + result

if __name__ == "__main__":

    MagicTest('CreateCanvas')
    MagicTest('ReadNoiseBlock')
    MagicTest('CopyNoiseBlock')
    MagicTest('MakeMask')
    MagicTest('GetShape')
    MagicTest('AssembleLayer')


    '''
    if CreateCanvas(): result = 'Pass'
    else: result = 'Fail'
    print 'CreateCanvas ' + result

    print 'CopyNoiseBlock?'
    if test_CopyNoiseBlock(): print 'Pass'
    else: print 'Fail'

    print 'MakeMask?'
    if test_MakeMask(): print 'Pass'
    else: print 'Fail'

    print 'GetShape?'
    if test_GetShape(): print 'Pass'
    else: print 'Fail'

    print 'AssembleLayer?'
    if test_AssembleLayer(): print 'Pass'
    else: print 'Fail'
    '''
    

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
