#PyEye.py

"""
1. Create canvas (600 x 250)
2. Create noise block (default pattern, can take input) (150 x 250)
3. Copy noise block and fill canvas
4. Copy and paste a shape (<= width of noise block)
5. Move shape 10 pixels to the right
6. Copy shape, move width of noise block to the left.
"""

import numpy
from PIL import Image

def main(dim=(250,600)): # strange how it makes you put it in y,x
    center=(dim[0]/2,dim[1]/2)
    num_blocks = 4

    img = CreateCanvas(dim=dim)

# TODO: should we just start with the noise block and replicate it out?
#       maybe we don't neeeed a CreateCanvas...

# TODO: ATM, canvas size has to be a multiple of block size.

    noise_block = CreateNoiseBlock(dim=dim,num_blocks=num_blocks)
    img = CopyNoiseBlock(img,noise_block,num_blocks)
   # shape = GetShape(img,mode='circle',size=140,position=center)
   # processed_shape = MoveShape(shape,depth=10,,position=center)
   # neg_shape = MoveShape(shape,depth=-dim[0]/num_blocks)
   # new_img = SumImages(img,processed_shape,neg_shape)

def CreateCanvas(dim):
    a=numpy.zeros([dim[0],dim[1],4],dtype='uint8')
    return a

def CreateNoiseBlock(dim, num_blocks):
    img = Image.open('pattern.png')
    img = numpy.array(img)
    return img

def CopyNoiseBlock(img, noise_block, num_blocks): # maybe call this ReplicateNoiseBlock ?
    final = img.copy()
    # final = img
    for i in range(num_blocks):
        size = 150
        start = i * size
        final[:,start:size+start,:]=noise_block
    return final

if __name__=="__main__":
    main()
