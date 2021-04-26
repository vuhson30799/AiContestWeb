from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from AiContestWeb.common import BaseViewSet
from AiContestWeb.uaa.model import MyUser
from AiContestWeb.uaa.serializer import UserSerializer


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
class UserViewSet(BaseViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes_by_action = {'create': [AllowAny],
                                    'destroy': [IsAdminUser]}


retrieve_user = UserViewSet.as_view({
    'get': 'retrieve'
})

list_user = UserViewSet.as_view({
    'get': 'list'
})

create_user = UserViewSet.as_view({
    'post': 'create'
})

update_user = UserViewSet.as_view({
    'put': 'update'
})
