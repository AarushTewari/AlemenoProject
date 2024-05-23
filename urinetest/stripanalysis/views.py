from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
import cv2
import numpy as np
from django.shortcuts import render

def index(request):
    return render(request, 'upload.html')

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            colors = self.process_image(image)
            return Response(colors, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_image(self, image):
        image_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        height, width, _ = img.shape
        segment_width = width // 10
        colors = []

        for i in range(10):
            segment = img[:, i * segment_width:(i + 1) * segment_width]
            avg_color_per_row = np.average(segment, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            colors.append({
                "r": int(avg_color[2]),
                "g": int(avg_color[1]),
                "b": int(avg_color[0])
            })

        return colors

