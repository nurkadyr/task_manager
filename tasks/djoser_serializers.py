from djoser.serializers import UserSerializer as BaseUserSerializer


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'DjoserUser'
