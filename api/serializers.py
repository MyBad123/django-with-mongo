from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    '''serializer for data in register request'''

    username = serializers.CharField()
    password = serializers.CharField()