from .cuda_context import CudaContext
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import numpy as np
import cv2
import time


class ConvolutionalFilters():

    def gaussian_kernel(self, size, sigma=3.0):
        kernel_size = size // 2
        x, y = np.mgrid[-kernel_size:kernel_size+1, -kernel_size:kernel_size+1]
        g = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        return g / g.sum()

    def gaussian_blur(self, file_bytes, kernel_size, sigma):

        if CudaContext.initialized:
            CudaContext.pop_context()

        CudaContext.get_context()

        try:
            kernel_code = """
                __global__ void gaussian_filter(float *input, float *output, float *kernel, int width, int height, int kernel_size) {
                    int x = blockIdx.x * blockDim.x + threadIdx.x;
                    int y = blockIdx.y * blockDim.y + threadIdx.y;
                    int half_kernel = kernel_size / 2;
                    
                    if (x >= width || y >= height) return;
                    
                    float sum = 0;
                    for (int dx = -half_kernel; dx <= half_kernel; dx++) {
                        for (int dy = -half_kernel; dy <= half_kernel; dy++) {
                            int ix = x + dx;
                            int iy = y + dy;
                            if (ix >= 0 && ix < width && iy >= 0 && iy < height) {
                                sum += input[iy * width + ix] * kernel[(dy + half_kernel) * kernel_size + (dx + half_kernel)];
                            }
                        }
                    }
                    
                    output[y * width + x] = sum;
                }
            """

            # Compilar el kernel de CUDA
            mod = SourceModule(kernel_code)
            gaussian_filter = mod.get_function("gaussian_filter")

            input_image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE).astype(np.float32)

            # Crear la imagen de salida
            output_image = np.zeros_like(input_image)

            # Generar el kernel gaussiano de 17x17
            gaussian_kernel_array = self.gaussian_kernel(kernel_size, sigma).astype(np.float32)

            # Aplanar el kernel gaussiano para pasarlo al kernel de CUDA
            gaussian_kernel_flat = gaussian_kernel_array.flatten()

            # Lanzar el kernel en la GPU
            block_size = (32, 32, 1)
            grid_size = (int(np.ceil(input_image.shape[1] / block_size[0])), int(np.ceil(input_image.shape[0] / block_size[1])))

            start_time = time.time()  # Inicia la medición del tiempo

            gaussian_filter(
                drv.In(input_image),
                drv.Out(output_image),
                drv.In(gaussian_kernel_flat),
                np.int32(input_image.shape[1]),
                np.int32(input_image.shape[0]),
                np.int32(kernel_size),
                block=block_size,
                grid=grid_size,
            )

            time_taken = time.time() - start_time  # Calcula el tiempo transcurrido
            
            output_image = np.clip(output_image, 0, 255).astype(np.uint8)


        finally:
            CudaContext.pop_context()

        return {
            'image': output_image,
            'time': time_taken,
            'threads_per_block': block_size[0] * block_size[1],
            'number_of_blocks': grid_size[0] * grid_size[1]
        }

    def median_blur(self, file_bytes, kernel_size):

        if CudaContext.initialized:
            CudaContext.pop_context()

        CudaContext.get_context()

        try:
            kernel_code = '''
                __global__ void filtroMediana(unsigned char *original, unsigned char *resultado, int kernel_size, int width, int height) {
                    const int MAX_KERNEL_SIZE = 31;  // Tamaño máximo definido
                    unsigned char ventana[MAX_KERNEL_SIZE * MAX_KERNEL_SIZE];  // Array de tamaño máximo
                    const int half_kernel_size = kernel_size / 2;

                    int tid_x = threadIdx.x + blockIdx.x * blockDim.x;
                    int tid_y = threadIdx.y + blockIdx.y * blockDim.y;

                    if (tid_x < width && tid_y < height) {
                        int count = 0;

                        // Llenar solo la parte relevante de la ventana basada en kernel_size
                        for (int j = -half_kernel_size; j <= half_kernel_size; j++) {
                            for (int i = -half_kernel_size; i <= half_kernel_size; i++) {
                                int x = tid_x + i;
                                int y = tid_y + j;

                                if (x >= 0 && x < width && y >= 0 && y < height) {
                                    ventana[count++] = original[y * width + x];
                                }
                            }
                        }

                        // Ordenar la ventana para encontrar el valor mediano
                        for (int i = 0; i < count - 1; i++) {
                            for (int j = 0; j < count - i - 1; j++) {
                                if (ventana[j] > ventana[j + 1]) {
                                    unsigned char temp = ventana[j];
                                    ventana[j] = ventana[j + 1];
                                    ventana[j + 1] = temp;
                                }
                            }
                        }

                        // Asignar el valor mediano al píxel central
                        resultado[tid_y * width + tid_x] = ventana[count / 2];
                    }
                }
            '''


            mod = SourceModule(kernel_code)
            filtro_mediana = mod.get_function("filtroMediana")

            # Cargar imagen en blanco y negro y convertirla en una matriz numpy
            input_image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE).astype(np.uint8)

            # Crear la imagen de salida
            output_image = np.zeros_like(input_image)

            # Definir dimensiones de bloque y cuadrícula
            block_dims = (32, 32, 1)
            grid_dims = (int(np.ceil(input_image.shape[1] / block_dims[0])), int(np.ceil(input_image.shape[0] / block_dims[1])))

            start_time = time.time()

            filtro_mediana(
                drv.In(input_image),
                drv.Out(output_image),
                np.int32(kernel_size),
                np.int32(input_image.shape[1]),
                np.int32(input_image.shape[0]),
                block=block_dims,
                grid=grid_dims,
            )

            time_taken = time.time() - start_time

            output_image = np.clip(output_image, 0, 255).astype(np.uint8)

        finally:
            CudaContext.pop_context()

        return {
            'image': output_image,
            'time': time_taken,
            'threads_per_block': block_dims[0] * block_dims[1],
            'number_of_blocks': grid_dims[0] * grid_dims[1]
        }

    def dog_blur(self, file_bytes, kernel_size, sigma):

        if CudaContext.initialized:
            CudaContext.pop_context()

        CudaContext.get_context()

        try:
            gaussian_kernel_code = '''
            __global__ void gaussian_blur(const float *input, float *output, int width, int height, const float *kernel, int kernel_size) {
                int x = blockIdx.x * blockDim.x + threadIdx.x;
                int y = blockIdx.y * blockDim.y + threadIdx.y;
                int half_kernel = kernel_size / 2;

                if (x >= width || y >= height) return;

                float sum = 0.0f;
                for (int ky = -half_kernel; ky <= half_kernel; ky++) {
                    for (int kx = -half_kernel; kx <= half_kernel; kx++) {
                        int pixel_x = min(max(x + kx, 0), width - 1);
                        int pixel_y = min(max(y + ky, 0), height - 1);
                        float value = input[pixel_y * width + pixel_x];
                        float weight = kernel[(ky + half_kernel) * kernel_size + (kx + half_kernel)];
                        sum += value * weight;
                    }
                }
                output[y * width + x] = sum;
            }
            '''

            # Compilar el kernel de CUDA para el suavizado gaussiano
            mod = SourceModule(gaussian_kernel_code)
            gaussian_blur = mod.get_function("gaussian_blur")

            # Cargar imagen en blanco y negro y convertirla en una matriz numpy
            input_image = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE).astype(np.float32)

            # Crear las imágenes de salida
            smoothed_image1 = np.zeros_like(input_image)
            smoothed_image2 = np.zeros_like(input_image)

            # Definir los sigmas para los filtros gaussianos
            sigma1 = 1.0

            # Crear los kernels gaussianos
            gaussian_kernel1 =  self.gaussian_kernel(sigma1, kernel_size).astype(np.float32)
            gaussian_kernel2 = self.gaussian_kernel(sigma, kernel_size).astype(np.float32)

            # Definir dimensiones de bloque y cuadrícula
            block_dims = (32, 32, 1)
            grid_dims = (int(np.ceil(input_image.shape[1] / block_dims[0])), int(np.ceil(input_image.shape[0] / block_dims[1])))

            start_time = time.time()

            # Aplicar el primer filtro gaussiano
            gaussian_blur(
                drv.In(input_image),
                drv.Out(smoothed_image1),
                np.int32(input_image.shape[1]),
                np.int32(input_image.shape[0]),
                drv.In(gaussian_kernel1),
                np.int32(kernel_size),
                block=block_dims,
                grid=grid_dims,
            )

            # Aplicar el segundo filtro gaussiano
            gaussian_blur(
                drv.In(input_image),
                drv.Out(smoothed_image2),
                np.int32(input_image.shape[1]),
                np.int32(input_image.shape[0]),
                drv.In(gaussian_kernel2),
                np.int32(kernel_size),
                block=block_dims,
                grid=grid_dims,
            )

            # Realizar la Diferencia de Gaussianas (DoG)
            dog_image = smoothed_image1 - smoothed_image2

            taken_time = time.time() - start_time

            # Convertir de vuelta a uint8 si es necesario y guardar la imagen DoG
            dog_image_uint8 = np.clip(dog_image, 0, 255).astype(np.uint8)

        finally:
            CudaContext.pop_context()
    
        return {
            'image': dog_image_uint8,
            'time': taken_time,
            'threads_per_block': block_dims[0] * block_dims[1],
            'number_of_blocks': grid_dims[0] * grid_dims[1]
        }

    def get_filter(self, filter_name):
        if filter_name == 'gaussian':
            return self.gaussian_blur
        elif filter_name == 'median':
            return self.median_blur
        elif filter_name == 'dog':
            return self.dog_blur
        else:
            raise ValueError('Filtro inválido')