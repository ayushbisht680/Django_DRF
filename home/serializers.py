from rest_framework import serializers
from .models import Person,Color
from django.contrib.auth.models import User

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields=['color_name','id']
        


class PeopleSerializer(serializers.ModelSerializer):
    # color=ColorSerializer()
    # color_info=serializers.SerializerMethodField()

    class Meta:
        model = Person
        # fields = ['name','age']
        # exclude=['name']
        fields = '__all__'
        # depth=1
    
    # def get_color_info(self,obj):
    #     color_obj=Color.objects.get(id=obj.color.id)
    #     return {'color_name':color_obj.color_name,'hexcode':'#0000'}

        
    def validate(self, data):
        special_characters='-\'"!@#$%^&*()_+=<>?/\\,.;:{}\[\]]+$'
        if any (c in  special_characters for c in data['name']):
            raise serializers.ValidationError("Name contains special characters")

        if data['age'] < 18:
            raise serializers.ValidationError("Age should be greater than 18")
        return data

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def check(self,data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('Username already taken')
        
        if data['email']:
            if User.objects.filter(username=data['email']).exists():
                raise serializers.ValidationError('Email already taken')
            
        return data
    
    def create(self,validate_data):
        user=User.objects.create(username=validate_data['username'],email=validate_data['email'])
        user.set_password(validate_data['password'])
        return validate_data




 
