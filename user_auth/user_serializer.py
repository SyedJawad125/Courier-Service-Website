from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from user_auth.models import User
# from foodapp.food_serializer import ProductsNumberSerializer
# from hrmapp.models import Products
# from hrmapp.models import Department, Position, Salary


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        label="old_password",
        style={"input_type": "old_password"},
        trim_whitespace=True,
        write_only=True
    )
    new_password = serializers.CharField(
        label="new_password",
        style={"input_type": "new_password"},
        trim_whitespace=True,
        write_only=True
    )
    confirm_password = serializers.CharField(
        label="confirm_password",
        style={"input_type": "confirm_password"},
        trim_whitespace=True,
        write_only=True
    )
    def validate(self, instance):
        user = self.context.get("user")
        if user.check_password(instance["old_password"]):
            if len(instance["new_password"]) < 8:
                raise serializers.ValidationError("Password must be at least 8 characters long.", 400)
            if instance["new_password"] == instance["old_password"]:
                raise serializers.ValidationError("Same Old Password.", 400)
            if instance['new_password'] != instance['confirm_password']:
                raise serializers.ValidationError("Password does not match.", 400)
            return instance
        else:
            raise serializers.ValidationError("Wrong Old Password.", 400)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def validate(self,instance):
        if len(instance["password"]) < 8:
            raise serializers.ValidationError({'password': ['Password must be at least 8 characters long.']}, code=400)
        instance['password'] = make_password(instance['password'])
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="username",
        trim_whitespace=True,
        write_only=True
    )
    password = serializers.CharField(
        label="password",
        style={"input_type": "password"},
        trim_whitespace = True,
        write_only=True
    )
    def validate(self, instance):
        if len(instance["password"]) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.", 400)
        if User.objects.filter(username=instance["username"], is_active=False, is_locked=True).exists():
            raise serializers.ValidationError("Your account has been deactivated.", 400)
        return instance


class UserListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['guid', 'get_full_name', 'phone', 'email', 'role', 'is_superuser']




# class DepartmentNumbersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields='__all__'


# class PositionNumbersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Position
#         fields='__all__'


# class SalaryNumbersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Salary
#         fields='__all__'

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields='__all__'

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['dept_added_by_user1'] = DepartmentNumbersSerializer(instance.dept_added_by_user1.all(), many=True).data if instance.dept_added_by_user1 else None
#         data['pos_added_by_user1'] = PositionNumbersSerializer(instance.pos_added_by_user1.all(), many=True).data if instance.pos_added_by_user1 else None
#         data['sal_added_by_user1'] = SalaryNumbersSerializer(instance.sal_added_by_user1.all(), many=True).data if instance.sal_added_by_user1 else None
#         return data
    





    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['pos_added_by_user1'] = PositionNumbersSerializer(instance.pos_added_by_user1.all(), many=True).data if instance.pos_added_by_user1 else None
    #     return data