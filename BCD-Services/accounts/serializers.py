from rest_framework import serializers
from .models import PersonalDetails
from .validators import MinimumLengthValidator, UppercaseLetterValidator, LowercaseLetterValidator, DigitValidator, SymbolValidator
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = '__all__'
        extra_kwargs = {'Password': {'write_only': True}}

    def validate(self, data): 
        password = data.get('Password')
        if password:
            validators = [
                MinimumLengthValidator(),
                UppercaseLetterValidator(),
                LowercaseLetterValidator(),
                DigitValidator(),
                SymbolValidator(),
            ]
            for validator in validators:
                try:
                    validator.validate(password)
                except ValidationError as e:
                    raise serializers.ValidationError({'Password': str(e)}) 

            data['Password'] = make_password(password) 
        return data
from rest_framework import serializers
from .models import ImageUpload

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['id', 'name', 'image']
