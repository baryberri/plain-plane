from user.models import Photo
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image', 'is_reported', 'color')

    def create(self, validated_data):
        image = validated_data['image']
        color = validated_data['color']

        photo = Photo(image=image, is_reported=False, color=color)
        photo.save()

        return photo
