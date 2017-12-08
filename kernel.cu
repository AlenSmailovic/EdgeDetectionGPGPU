#include <math.h>

#define MIN_RGB_VALUE 0
#define MAX_RGB_VALUE 255

#define     TILE_WIDTH      32
#define     SOBEL_WIDTH     3
#define     W           	(TILE_WIDTH + SOBEL_WIDTH)

extern "C" __global__ void shared_sobel_filter(const float * pixin, float * pixout, const int width, const int height)
{	
	__shared__ float cacheImg[W][W];
	
	// Index in actual image
	int idx = (threadIdx.x) + blockDim.x * blockIdx.x;
	
	float sobelMatrix[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
	
	// Destination for pixels in shared memory
    int dest = threadIdx.y * blockDim.y + threadIdx.x;
    int destY = dest / W;
    int destX = dest % W;
    
    // Insert pixels from input image into shared memory
	if(idx < width * height)
        cacheImg[destY][destX] = pixin[idx * 3];
    
    __syncthreads();

    // Perform Sobel convolution
    float px_x = 0;
    float px_y = 0;
    
    for(int y = 0; y < SOBEL_WIDTH; ++y) {
        for(int x = 0; x < SOBEL_WIDTH; ++x) {
			// Magnitude for X
            px_x += cacheImg[threadIdx.y][threadIdx.x + y] * sobelMatrix[x + (y * SOBEL_WIDTH)];
            // Magnitude for Y
            px_y += cacheImg[threadIdx.y][threadIdx.x + y] * sobelMatrix[SOBEL_WIDTH - 1 - y + (x * SOBEL_WIDTH)];
		}
	}
	
	// Compute the gradient magnitude
	float px = (float)(sqrt(px_x * px_x + px_y * px_y));

	// Edge cases of MIN or MAX RGB after the Sobel operator is applied
	if (px < MIN_RGB_VALUE)
		px = MIN_RGB_VALUE;
	else if (px > MAX_RGB_VALUE)
		px = MAX_RGB_VALUE;
	
	// Set the pixel value into the edge image (RGB matrix)
	if(idx < width * height) {
		pixout[idx * 3 + 0] = px;
		pixout[idx * 3 + 1] = px;
		pixout[idx * 3 + 2] = px;
	}
	
    __syncthreads();
}

extern "C" __global__ void sobel_filter(const float * pixin, float * pixout, const int width, const int height)
{	
	int idx = (threadIdx.x) + blockDim.x * blockIdx.x;
    int idy = (threadIdx.y) + blockDim.y * blockIdx.y;
	
	if(idx < width * height) {
		
		// To detect horizontal lines. This is effectively the dy.
		const int sobelX[3][3] = { {-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1} };
		// To detect vertical lines. This is effectively the dy.
		const int sobelY[3][3] = { {-1, -2, -1}, {0, 0, 0}, {1, 2, 1} };

		float px_x = 0;
		float px_y = 0;

		for (int j = 0; j < 3; ++j) {
			for (int i = 0; i < 3; ++i) {
				
				// Index in rows
				const int x = i + idx * 3;
				// Index in colomns
				const int y = j + idy * 3;
				
				const int index = x + y;
				// Magnitude for X
				px_x += pixin[index] * sobelX[i][j];
				// Magnitude for Y
				px_y += pixin[index] * sobelY[i][j];
			}
		}
		
		// Compute the gradient magnitude
		float px = (float)(sqrt(px_x * px_x + px_y * px_y));
		
		// Edge cases of MIN or MAX RGB after the Sobel operator is applied
		if (px < MIN_RGB_VALUE)
			px = MIN_RGB_VALUE;
		else if (px > MAX_RGB_VALUE)
			px = MAX_RGB_VALUE;
		
		// Set the pixel value into the edge image (RGB matrix)
		pixout[idx * 3 + 0] = px;
		pixout[idx * 3 + 1] = px;
		pixout[idx * 3 + 2] = px;
	}
}
    
extern "C" __global__ void gray_scale(const float * pixin, float * pixout, const int width, const int height)
{
    int idx = (threadIdx.x) + blockDim.x * blockIdx.x;
 
	if(idx < width * height) {
		
		// Compute pixels to obtain a grayscale image
		float px = 0.2126 * pixin[idx * 3 + 0] + 
				   0.7152 * pixin[idx * 3 + 1] + 
				   0.0722 * pixin[idx * 3 + 2];
		
		// Save pixel into the output image (RGB matrix)
		pixout[idx * 3 + 0] = px;
		pixout[idx * 3 + 1] = px;
		pixout[idx * 3 + 2] = px;
	}
}

int main(void) {
	return 0;
}