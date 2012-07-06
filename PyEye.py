#PyEye.py

"""
1. Create canvas (600 x 250)
2. Create noise block (default pattern, can take input) (150 x 250)
3. Copy noise block and fill canvas
4. Copy and paste a shape (<= width of noise block)
5. Move shape 10 pixels to the right
6. Copy shape, move width of noise block to the left.
"""

def main(dim=(600,250)):
    center=(dim[0]/2,dim[1]/2)
    num_blocks = 4

    img = CreateCanvas(dim=dim)
    noise_block = CreateNoiseBlock(dim=dim,num_blocks=num_blocks)
    img = CopyNoiseBlock(img,noise_block)
    shape = GetShape(img,mode='circle',size=140,position=center)
    processed_shape = MoveShape(shape,depth=10,,position=center)
    neg_shape = MoveShape(shape,depth=-dim[0]/num_blocks)
    new_img = SumImages(img,processed_shape,neg_shape)

def CreateCanvas(dim):
    
