## EdgeDetectionGPGPU

### About
- The project compare the implementation of edge detecting done in CPU and GPU to see how fast, cost and work-efficient it is. This implements a Sobel filter: for CPU implementation is a Python script and for GPU implementation is a kernel with a Python wrapper.

### Compile kernel
- The command for compiling the kernel
> nvcc kernel.cu -std=c++11 --gpu-architecture=compute_30 --gpu-code=sm_30,sm_30 -cubin -o kernel.cubin

- The [resulted file](https://github.com/AlenSmailovic/EdgeDetectionGPGPU/raw/master/kernel.cubin) is added too.

### Performance comparison between CPU and GPU
- The comparison is done on five type of images with different resolution: 4K (5120X3200), QHD (3840X2160), FHD (1920X1080), HD (1280X720), VGA (640X480).
- For image results, run the scripts.

| Implementation | Image size | Get and Convert | Allocate memory | Image processing / Kernel execution | Get from GPU and Convert | Saving    | Total time |
| -------------- | ---------- | --------------- | --------------- | ----------------------------------- | ------------------------ | --------- | ---------- |
| **CPU**        | 640X480    | 0.0200002       | -               | 9.2549998                           | -                        | 0.1200001 | 9.3950002  |
| **GPU**        | 640X480    | 0.0609910       | 0.0066528       | 0.0022110                           | 0.0023078                | 0.1253440 | 0.1975078  |
