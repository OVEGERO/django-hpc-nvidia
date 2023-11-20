from .logic import convolutional_filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
import cv2
import numpy as np
from django.http import HttpResponse
import base64

filters = convolutional_filters.ConvolutionalFilters()

@api_view(['POST'])
def filters_view(request):
    try:
        uploadedFile = request.FILES.get('image')
        if not uploadedFile:
            return Response({'result': 'No se proporcionó imagen'}, status=400)

        filter_name = request.data.get('filter_name')
        sigma = request.data.get('sigma')
        kernel_size = request.data.get('kernel_size')

        try:
            sigma = float(sigma) if sigma else None
            kernel_size = int(kernel_size) if kernel_size else None
        except ValueError:
            return Response({'result': 'Sigma o tamaño del kernel inválidos'}, status=400)

        file_bytes = np.frombuffer(uploadedFile.read(), np.uint8)
        filter_function = filters.get_filter(filter_name)

        if filter_name in ['gaussian', 'dog'] and sigma is None:
            return Response({'result': 'No se proporcionó sigma'}, status=400)
        elif filter_name in ['gaussian', 'dog'] and sigma:
            # Ejecutar la función del filtro y obtener datos adicionales
            filter_result = filter_function(file_bytes, kernel_size, sigma)
            output_image, time_taken, threads_per_block, number_of_blocks = (
                filter_result['image'],
                filter_result['time'],
                filter_result['threads_per_block'],
                filter_result['number_of_blocks'],
            )
        else:
            sigma = 'No se utiliza en este filtro'
            filter_result = filter_function(file_bytes, kernel_size)
            output_image, time_taken, threads_per_block, number_of_blocks = (
                filter_result['image'],
                filter_result['time'],
                filter_result['threads_per_block'],
                filter_result['number_of_blocks'],
            )

        is_success, buffer = cv2.imencode(".jpg", output_image)
        if not is_success:
            return Response({'result': 'Error al codificar la imagen'}, status=500)

        # Codificar la imagen en base64 para incluirla en la respuesta JSON
        encoded_image = base64.b64encode(buffer.tobytes()).decode('utf-8')

        # Preparar la respuesta con la imagen y los datos adicionales
        response_data = {
            'image': encoded_image,
            'time_taken': time_taken,
            'threads_per_block': threads_per_block,
            'number_of_blocks': number_of_blocks,
            'method': filter_name,
            'kernel': kernel_size,
            'sigma': sigma,
        }
        return Response(response_data)

    except Exception as e:
        return Response({'result': f'Error en el servidor: {str(e)}'}, status=500)
