import numpy as np
from PIL import Image
import time
import math

def conv_norm(sobelX, sobelY, pxImg, width, height):

    # Create edge image making a copy of initial image
    edge = pxImg

    # Save the computed magnitude in this array
    lenght = np.zeros((width*height))
    index = -1

    # Convolution of Sobel matrix and current image
    for x in range(1, width-1):
      for y in range(1, height-1):
        # Magnitude for X
        pixel_x = (sobelX[0][0] * pxImg[y-1][x-1][0]) + (sobelX[0][1] * pxImg[y][x-1][0]) + (sobelX[0][2] * pxImg[y+1][x-1][0]) + \
                  (sobelX[1][0] * pxImg[y-1][x][0])   + (sobelX[1][1] * pxImg[y][x][0])   + (sobelX[1][2] * pxImg[y+1][x][0])   + \
                  (sobelX[2][0] * pxImg[y-1][x+1][0]) + (sobelX[2][1] * pxImg[y][x+1][0]) + (sobelX[2][2] * pxImg[y+1][x+1][0])
        # Magnitude for Y
        pixel_y = (sobelY[0][0] * pxImg[y-1][x-1][0]) + (sobelY[0][1] * pxImg[y][x-1][0]) + (sobelY[0][2] * pxImg[y+1][x-1][0]) + \
                  (sobelY[1][0] * pxImg[y-1][x][0])   + (sobelY[1][1] * pxImg[y][x][0])   + (sobelY[1][2] * pxImg[y+1][x][0])   + \
                  (sobelY[2][0] * pxImg[y-1][x+1][0]) + (sobelY[2][1] * pxImg[y][x+1][0]) + (sobelY[2][2] * pxImg[y+1][x+1][0])

        index = index + 1
        # Compute the gradient magnitude
        lenght[index] = (( pixel_x * pixel_x + pixel_y * pixel_y ) ** 0.5)

    # Set pixels value in edge image for edge detection
    index = -1
    for i in range(1, width-1):
        for j in range(1, height-1):
            index = index + 1
            # Make sure of each pixel value is in interval [0, 255]
            if (math.isnan(lenght[index]) | (lenght[index] < 0)):
                lenght[index] = 0
            elif (lenght[index] > 255):
                lenght[index] = 255
            # Set the pixel value in edge image
            edge[j][i] = (lenght[index], lenght[index], lenght[index])
       
    return edge

def sobelOperator( pxImg, width, height ):
    # Sobel matrix for edge detection X & Y
    sobelX = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
    sobelY = np.array([[-1, -2, -1],[0, 0, 0],[1, 2, 1]])

    # Apply sobel convolution for edge detecting
    pxImg = conv_norm(sobelX, sobelY, pxImg, width, height)
            
def grayScale ( pxImg, width, height ):
    for x in range(width):
        for y in range(height):

            # get RGB pixelx value from image
            (r, g, b) = pxImg[y][x]

            # Compute the pixels to obtain a gray scale image
            gray = int (r * 0.2126 + g * 0.7152 + b * 0.0722)

            # Set the pixels with new value
            pxImg[y][x] = (gray, gray, gray)      

def cpu_edgeDetection( pathImg ):
    # print the path for input image
    print pathImg

    timeStart = time.time()

    # Open image from path
    img = Image.open( pathImg )

    # Convert image to RGB matrix
    rgb_img = img.convert('RGB')
    # Save the image matrix in a numpy array
    pxImg = np.array(rgb_img)

    # Get width and height of image
    width, height = rgb_img.size

    timeConvert = time.time()

    # Algorithm for gray scaling an image
    grayScale(pxImg, width, height)

    # Edge detection in current image
    sobelOperator(pxImg, width, height)

    timeProcessing = time.time()

    # Load the image from numpy array
    rgb_img = Image.fromarray(pxImg, mode = "RGB")
    # Save the image at corresponding path
    rgb_img.save( str("CPUEdge") + pathImg )

    timeSave = time.time()

    print "Image size : ", rgb_img.size
    print "Get and convert time : ", timeConvert - timeStart
    print "Image processing time : ", timeProcessing - timeConvert
    print "Saving time : ", timeSave - timeProcessing
    print "Total time : ", timeSave - timeStart
    
    print "----------------\n"


# Call cpu_edgeDetection for each type of image
cpu_edgeDetection("Images/VGA.png")
cpu_edgeDetection("Images/HD.png")
cpu_edgeDetection("Images/FHD.png")
cpu_edgeDetection("Images/QHD.png")
cpu_edgeDetection("Images/4K.png")