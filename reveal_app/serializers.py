from rest_framework import serializers
from reveal_app.models import CustomUser
import re

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta():
        model = CustomUser
        fields = ['email','password']
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate_password(self,value):
        if len(value)<8:
            raise serializers.ValidationError('Password must be 8 characters long')
        if not re.search(r'[A-Z]',value):
            raise serializers.ValidationError('Password must contain atleast one upper case letter')
        if not re.search(r'[a-z]',value):
            raise serializers.ValidationError('Password must contain atleast one lower case letter')
        if not re.search(r'[@$!%*?&#]',value):
            raise serializers.ValidationError('Password must contain atleast one special character')
        return value
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data