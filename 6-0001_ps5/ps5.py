
"""
# Problem Set 5
# Name: Griffin Leonard
# Collaborators: n/a
# Time: 5:00
# Late Days Used: 3
"""

from PIL import Image
import numpy

def generate_matrix(color):
    """
    Generates a transformation matrix for the specified color.
    Inputs:
        color: string with exactly one of the following values:
               'red', 'blue', 'green', or 'none'
    Returns:
        matrix: a transformation matrix corresponding to
                deficiency in that color
    """
    # You do not need to understand exactly how this function works.
    if color == 'red':
        c = [[.567, .433, 0],[.558, .442, 0],[0, .242, .758]]
    elif color == 'green':
        c = [[0.625,0.375, 0],[ 0.7,0.3, 0],[0, 0.142,0.858]]
    elif color == 'blue':
        c = [[.95, 0.05, 0],[0, 0.433, 0.567],[0, 0.475, .525]]
    elif color == 'none':
        c = [[1, 0., 0],[0, 1, 0.],[0, 0., 1]]
    return c


def matrix_multiply(m1,m2):
    """
    Multiplies the input matrices.
    Inputs:
        m1,m2: the input matrices
    Returns:
        result: matrix product of m1 and m2
        in a list of floats
    """

    product = numpy.matmul(m1,m2)
    if type(product) == numpy.int64:
        return float(product)
    else:
        result = list(product)
        return result


def convert_image_to_pixels(image):
    """
    Takes an image (must be inputted as a string
    with proper file attachment ex: .jpg, .png)
    and converts to a list of tuples representing pixels.
    Each pixel is a tuple containing (R,G,B) values.

    Returns the list of tuples.

    Inputs:
        image: string representing an image file, such as 'lenna.jpg'
    Returns: list of pixel values in form (R,G,B) such as
                 [(0,0,0),(255,255,255),(38,29,58)...]
    """
    pic = Image.open(image,'r') 
    return list(pic.getdata()) 


def convert_pixels_to_image(pixels,size):
    """
    Creates an Image object from a inputted set of RGB tuples.

    Inputs:
        pixels: a list of pixels such as the output of
                convert_image_to_pixels.
        size: a tuple of (width,height) representing
              the dimensions of the desired image. Assume
              that size is a valid input such that
              size[0] * size[1] == len(pixels).
    Returns:
        img: Image object made from list of pixels
    """
    pic = Image.new('RGB',size) #creates an empty image
    pic.putdata(pixels)
    return pic


def apply_filter(pixels, color):
    """
    pixels: a list of pixels in RGB form, such as [(0,0,0),(255,255,255),(38,29,58)...]
    color: 'red', 'blue', 'green', or 'none', must be a string representing the color
    deficiency that is being simulated.
    returns: list of pixels in same format as earlier functions,
    transformed by matrix multiplication
    """
    m1 = generate_matrix(color)
    for m2 in range(len(pixels)):
        pixels[m2] = matrix_multiply(m1,pixels[m2])
    
    #matrix_multiply returns lists of floats; this converts them to tuples of ints
    for l in range(len(pixels)):
        for n in range(3):
            (pixels[l])[n] = int((pixels[l])[n])
        pixels[l] = tuple(pixels[l])
    return pixels


def get_BW_lsb(pixels):
    """
    Gets the least significant bit of each pixel in the specified image.
    Inputs:
       pixels: list, a list of pixels in BW form, such as [0, 255, 120, ...]
    returns:
       lsb: a list of least significant bits
    """
    lsb = []
    for pix in pixels:
        if pix%2 == 0:
            lsb.append(0)
        else:
            lsb.append(255)
    return lsb


def get_RGB_lsb(pixels):
    """
    Gets the 2 least significant bits of each pixel in the specified color image.
    Inputs:
        pixels: a list of pixels in RGB form, such as [(0,0,0),(255,255,255),(38,29,58)...]
    Returns:
        lsb: a list of least significant bits
    """
    lsb = []
    for tup in range(len(pixels)):
        temp = []
        for pix in pixels[tup]:
            if pix%4 == 0:
                temp.append(0)
            if pix%4 == 1:
                temp.append(int(255/3))
            elif pix%4 == 2:
                temp.append(int(255*2/3))
            elif pix%4 == 3:
                temp.append(255)
        lsb.append(tuple(temp))
    return lsb
        


def reveal_image(filename, mode):
    """
    Extracts the hidden image, calls get lsb function based on parameter

    Inputs: 
        filename: string, input file to be processed
        mode: 'RGB' or '1' based on whether input file is color ('RGB') or black/white ('1'); see PIL Modes
    Returns:
        result: an Image object containing the hidden image
    """
    pixels = convert_image_to_pixels(filename)
    
    if mode == 'RGB':
        hidden = get_RGB_lsb(pixels)
    elif mode == '1':
        hidden = get_BW_lsb(pixels)
    
    im = Image.open(filename)
    width,height = im.size
    return convert_pixels_to_image(hidden,(width,height))


def main():
    pass

    # UNCOMMENT the following 8 lines to test PART 1

    im = Image.open('img_29.jpg')    
    width, height = im.size
    pixels = convert_image_to_pixels('img_29.jpg')
    im = convert_pixels_to_image(pixels, (width, height))  
    image = apply_filter(pixels,'none')
    im = convert_pixels_to_image(image, (width, height))
    im.show()
    new_image = apply_filter(pixels,'red')
    im2 = convert_pixels_to_image(new_image,(width,height))
    im2.show()


    # PART 2
    # Write your code below to find the hidden images in hidden1.bmp and hidden2.bmp!
    hidden1 = reveal_image('hidden1.bmp','1')
    hidden1.show()
    hidden2 = reveal_image('hidden2.bmp','RGB')
    hidden2.show()


if __name__ == '__main__':
    main()
