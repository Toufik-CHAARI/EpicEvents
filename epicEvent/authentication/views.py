from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import (
    ManagementOrSuperuserAccess,
    ManagementOnlyAccess,
)


class UserListView(generics.ListAPIView):
    """
    View for listing CustomUser objects.
    This view is designed to display a list of all users
    in the CustomUser model.
    The "ManagementOrSuperuserAccess" permission
    class allows only management users or superusers to update user
    data.
    The 'get_object' method is inherited from the superclass
    and can be used to retrieve individual user instances as needed.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOrSuperuserAccess]

    def get_object(self):
        return super().get_object()


class UserCreateView(generics.CreateAPIView):
    """
    View for the creation of users based on the CustomUser model.
    The "ManagementOrSuperuserAccess" permission class allows only
    management users or superusers to create new users.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOrSuperuserAccess]


class UserDetailView(generics.RetrieveAPIView):
    """
    View for retrieving detailed information of a CustomUser object.
    This view is designed to provide detailed data for individual users
    based on the CustomUser model.
    The "ManagementOrSuperuserAccess" permission
    class allows only management users or superusers to update user
    data.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOrSuperuserAccess]


class UserUpdateView(generics.UpdateAPIView):
    """
    View for updating existing CustomUser objects.
    This view facilitates the modification of user data within the
    CustomUser model. The "ManagementOrSuperuserAccess" permission
    class allows only management users or superusers to update user
    data.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOrSuperuserAccess]


class UserDeleteView(generics.DestroyAPIView):
    """
    View for deleting CustomUser objects.
    The "ManagementOrSuperuserAccess" permission class allows only
    management users or superusers to delete users. this prevents
    unauthorized user deletions.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOrSuperuserAccess]
