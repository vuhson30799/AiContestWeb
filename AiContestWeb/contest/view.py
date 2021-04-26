from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from AiContestWeb.common import BaseViewSet
from AiContestWeb.contest.model import Contest
from AiContestWeb.contest.serializer import ContestSerializer
from AiContestWeb.uaa.permissions import IsCreatorUser


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
class ContestViewSet(BaseViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    lookup_field = 'id'
    permission_classes_by_action = {'create': [IsCreatorUser],
                                    'destroy': [IsAdminUser, IsCreatorUser],
                                    'update': [IsAdminUser, IsCreatorUser]}


retrieve_contest = ContestViewSet.as_view({
    'get': 'retrieve'
})

list_contest = ContestViewSet.as_view({
    'get': 'list'
})

create_contest = ContestViewSet.as_view({
    'post': 'create'
})

update_contest = ContestViewSet.as_view({
    'put': 'update'
})

delete_contest = ContestViewSet.as_view({
    'delete': 'destroy'
})
