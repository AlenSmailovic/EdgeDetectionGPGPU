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

| Implementation | Image size | Convert         | Allocate memory | Image processing                    | Convert from GPU         | Saving    | Total time |
| -------------- | ---------- | --------------- | --------------- | ----------------------------------- | ------------------------ | --------- | ---------- |
| **CPU**        | 640X480    | 0.0200002       | -               | 9.2549998                           | -                        | 0.1200001 | 9.3950002  |
| **GPU**        | 640X480    | 0.0609910       | 0.0066528       | 0.0022110                           | 0.0023078                | 0.1253440 | 0.1975078  |
|                |            |                 |                 |                                     |                          |           |            |
| **CPU**        | 1280X720   | 0.0199999       | -               | 27.481999                           | -                        | 0.1700000 | 27.671999  |
| **GPU**        | 1280X720   | 0.0299420       | 0.0145668       | 0.0002372                           | 0.0056648                | 0.1365141 | 0.1869251  |
|                |            |                 |                 |                                     |                          |           |            |
| **CPU**        | 1920X1080  | 0.0799999       | -               | 63.271000                           | -                        | 0.7500000 | 64.101000  |
| **GPU**        | 1920X1080  | 0.0938701       | 0.0312290       | 0.0003209                           | 0.0103600                | 0.5749020 | 0.7106821  |
|                |            |                 |                 |                                     |                          |           |            |
| **CPU**        | 3840X2160  | 0.3199999       | -               | 250.45799                           | -                        | 2.9400000 | 253.71799  |
| **GPU**        | 3840X2160  | 0.2851300       | 0.0956630       | 0.0002830                           | 0.0324380                | 1.9789669 | 2.3924810  |
|                |            |                 |                 |                                     |                          |           |            |
| **CPU**        | 5120X3200  | 0.5800001       | -               | 532.90599                           | -                        | 5.3599998 | 538.84599  |
| **GPU**        | 5120X3200  | 0.4501910       | 0.1823840       | 0.0002810                           | 0.0589640                | 3.8527259 | 4.5445461  |