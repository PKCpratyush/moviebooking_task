from rest_framework import serializers
from .models import Users, Movies

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    # def create(self, validated_data):
    #     user = super(UserSerializer, self).create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_password(self,value):

        chars = "~!@#$%^&"
        nums = "1234567890"
        length_check = False
        if len(value) >= 8 and len(value) <= 16:
            length_check = True
        if length_check == True:
            special_char_check = False
            num_check = False
            for i in value:
                if i in chars:
                    special_char_check = True
                if i in nums:
                    num_check = True
                if num_check and special_char_check:
                    return value
        raise serializers.ValidationError('Password must contain a speacial character and a number and length must be greater than 8 and less than 16')
    

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'