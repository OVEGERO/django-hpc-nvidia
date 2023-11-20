# Usa una imagen base de NVIDIA CUDA
FROM nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

# Actualiza el sistema y añade las dependencias necesarias
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-setuptools && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y libglib2.0-0 && \
    apt-get install -y libjpeg-dev libpng-dev libtiff-dev && \
    apt-get install -y libavcodec-dev libavformat-dev libswscale-dev && \
    apt-get install -y libtbb-dev && \
    apt-get install -y libv4l-dev && \
    apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

# Limpia el caché de APT para reducir el tamaño de la imagen
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Crea y cambia al directorio de trabajo de la aplicación
WORKDIR /app

# Copia los archivos necesarios a la imagen de Docker
COPY requirements.txt /app/
COPY . /app/

# Instala las dependencias de la aplicación
RUN pip3 install -r requirements.txt

# Expone el puerto 8000 para acceder a la aplicación
EXPOSE 8000

# Define el comando para ejecutar la aplicación
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
