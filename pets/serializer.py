from rest_framework import serializers, validators
from groups.models import Group
from traits.models import Trait

from .models import Gender, Pet

from groups.serializer import GroupSerializer
from traits.serializer import TraitSerializer

from django.forms.models import model_to_dict

import pdb


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Gender.choices, default=Gender.DEFAULT)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
    traits_count = serializers.SerializerMethodField()

    def get_traits_count(self, obj):
        traits = obj.traits.all()
        traits_count = len(traits)
        return traits_count


    def create(self, validated_data: dict) -> Pet:
        group_dict = validated_data.pop("group")
        traits_dict = validated_data.pop("traits")

        group, _ = Group.objects.get_or_create(**group_dict)

        pet = Pet.objects.create(**validated_data, group=group)

        for trait in traits_dict:
            trait, _ = Trait.objects.get_or_create(**trait)
            pet.traits.add(trait)

        return pet

    def update(self, instance: Pet, validated_data: dict):
        group_dict = validated_data.pop("group", None)
        traits_dict = validated_data.pop("traits", None)

        if group_dict:
            group, _ = Group.objects.get_or_create(**group_dict)
            instance.group = group
    
        if traits_dict:
            traits_list = []
            for trait in traits_dict:
                trait, _ = Trait.objects.get_or_create(**trait)
                traits_list.append(trait)

            instance.traits.set(traits_list)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
