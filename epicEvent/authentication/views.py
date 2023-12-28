from rest_framework import generics, permissions
from .models import CustomUser
from .serializer import CustomUserSerializer
from .permissions import ManagementOrSuperuserAccess,ManagementOnlyAccess
 
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOnlyAccess]
    
    def get_object(self):        
        return super().get_object()
    

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOrSuperuserAccess]

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOnlyAccess]

class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOrSuperuserAccess]

class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [ManagementOrSuperuserAccess]

