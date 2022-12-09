from django.shortcuts import render
from .serializer import PetSerializer
from .models import Pet
from rest_framework.response import Response
from rest_framework.views import APIView, status
from django.shortcuts import get_object_or_404

import pdb

class PetView(APIView):
    def get(self, request):
        pets = Pet.objects.all()
        pets = PetSerializer(data=pets, many=True)
        pets.is_valid()

        return Response(pets.data)    


    def post(self, request):
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

class PetDatailView(APIView):
    def get(self, request, pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        pet = PetSerializer(pet)

        return Response(pet.data)

    def patch(self, request, pet_id) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(pet, request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pet_id):
        pet: Pet = get_object_or_404(Pet, id=pet_id)

        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
