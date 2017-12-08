import pycuda.driver as cuda
import pycuda.autoinit
import sys
import os
import numpy as numpy
from PIL import Image
import time

BLOCK_SIZE = 1024

# Prepare the kernel functions to be used in Python
cuda_module = cuda.module_from_file('kernel.cubin')

gray_scale = cuda_module.get_function('gray_scale')
gray_scale.prepare(['P', 'P', 'I', 'I'])

sobel_filter = cuda_module.get_function('sobel_filter')
sobel_filter.prepare(['P', 'P', 'I', 'I'])

shared_sobel_filter = cuda_module.get_function('shared_sobel_filter')
shared_sobel_filter.prepare(['P', 'P', 'I', 'I'])


def gpu_edgeDetection( pathImg ):
	
	# print the path for input image
    print pathImg
    
    timeStart = time.time()
    
    # Open image from path
    img = Image.open( pathImg )
    
    # Convert image to RGB matrix
    rgb_img = img.convert('RGB')
    # Save the image matrix in a numpy array	
    pxImg = numpy.array(rgb_img)
    
    # Get width and height of image
    width, height = rgb_img.size
    # Compute them to have the total size
    size = width * height
    
    # Create new numpy arrays exactly the same like input image
    # Store the image result iside them
    gray_px = numpy.empty_like(pxImg)
    sobel_px = numpy.empty_like(pxImg)
    
    timeConvert = time.time()
    
    #----------- Gray Scale ---------
    # Convert the input image into float matrix
    pxImg = pxImg.astype(numpy.float32)
    # Memory allocation inside the GPU for input image
    px_gpu = cuda.mem_alloc(pxImg.nbytes)
    
    # Copy the input image inside the gpu (host -> device)
    cuda.memcpy_htod(px_gpu, pxImg)
    
    # Make sure that the output image is float format
    # Is an empty array
    gray_px = gray_px.astype(numpy.float32)
    # Memory allocation inside the gpu for output image
    gray_px_gpu = cuda.mem_alloc(gray_px.nbytes)
    
    # Copy the empty array inside the gpu (host -> device)
    # The image result will be saved here
    cuda.memcpy_htod(gray_px_gpu, gray_px)
    
    timeAllocMem1 = time.time()
	
	# Convert RGB image to gray scale image
	# px_gpu      : input image - RGB image
	# gray_px_gpu : output image - gray scale image
	# width       : width of input image 
	# height      : height of input image
	# block        : kernel block size
	# grid         : kernel grid size
    gray_scale(px_gpu, gray_px_gpu,
         numpy.int32(width),
         numpy.int32(height),
         block = (BLOCK_SIZE, 1, 1),
         grid  = ((size + BLOCK_SIZE - 1) / BLOCK_SIZE, 1, 1))
    
    timeKernelExec1 = time.time()
	
    #----------- Sobel Filter ---------
    # Make sure that the output image is float format
    # Is an empty array
    sobel_px = sobel_px.astype(numpy.float32)
    # Memory allocation inside the gpu for output image
    sobel_px_gpu = cuda.mem_alloc(sobel_px.nbytes)
	
    # Copy the empty array inside the gpu (host -> device)
    # The image result will be saved here
    cuda.memcpy_htod(sobel_px_gpu, sobel_px)
	
    timeAllocMem2 = time.time()
	
	# Apply sobel filter to gray scale image
	# gray_px_gpu  : input image - gray scale image
	# sobel_px_gpu : output image - edge detetions
	# width        : width of input image 
	# height       : height of input image
	# block        : kernel block size
	# grid         : kernel grid size
    
    print "Normal Sobel Filter GPU"
    sobel_filter(gray_px_gpu, sobel_px_gpu,
          numpy.int32(width),
          numpy.int32(height),
          block = (BLOCK_SIZE, 1, 1),
          grid  = ((size + BLOCK_SIZE - 1)/BLOCK_SIZE, 1))
    
    
	# Apply sobel filter to gray scale image
	# gray_px_gpu  : input image - gray scale image
	# sobel_px_gpu : output image - edge detetions
	# width        : width of input image 
	# height       : height of input image
	# block        : kernel block size
	# grid         : kernel grid size
    '''
    print "Shared Memory Sobel Filter GPU"
    shared_sobel_filter(gray_px_gpu, sobel_px_gpu,
          numpy.int32(width),
          numpy.int32(height),
          block = (BLOCK_SIZE, 1, 1),
          grid  = ((size + BLOCK_SIZE - 1)/BLOCK_SIZE, 1))
    '''
	
    timeKernelExec2 = time.time()
	
    # Copy the resultet image from device to host
    # The resulted image can be used now in Python    
    cuda.memcpy_dtoh(sobel_px, sobel_px_gpu)
	
	# Convert the image to uint8 format
    sobel_px = numpy.uint8(sobel_px)
    
    timeConvertGPU = time.time()
	
    # Load the image from numpy array
    rgb_img = Image.fromarray(sobel_px, mode = "RGB")
    # Save the image at corresponding path
    rgb_img.save( str("GPUEdge") + pathImg )
	
    timeSave = time.time()

    print "Image size : ", rgb_img.size
    print "Get and convert time : ", timeConvert - timeStart
    print "Allocate memory time : ", timeAllocMem1 - timeConvert + timeAllocMem2 - timeKernelExec1
    print "Kernel execution time : ", timeKernelExec1 - timeAllocMem1 + timeKernelExec2 - timeAllocMem2
    print "Get from GPU and convert time : ", timeConvertGPU - timeKernelExec2
    print "Saving time : ", timeSave - timeConvertGPU
    print "Total time : ", timeSave - timeStart
    
    print "----------------\n"


# Call gpu_edgeDetection for each type of image
gpu_edgeDetection("Images/VGA.png")
gpu_edgeDetection("Images/HD.png")
gpu_edgeDetection("Images/FHD.png")
gpu_edgeDetection("Images/QHD.png")
gpu_edgeDetection("Images/4K.png")