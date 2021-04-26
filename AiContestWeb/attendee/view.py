from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from AiContestWeb.attendee.model import Attendee
from AiContestWeb.attendee.serializer import AttendeeSerializer
from AiContestWeb.uaa.permissions import IsStudentUser, IsCreatorUser


@authentication_classes([BasicAuthentication])
@permission_classes([IsStudentUser, IsAuthenticated])
class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    lookup_field = 'id'
    lookup_fields = ['contest_id', 'user_id']

    def list(self, request, *args, **kwargs):
        queryset = Attendee.objects.filter(**self.apply_filter_for_search())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def apply_filter_for_search(self):
        my_filter = {}
        for field in self.lookup_fields:
            try:
                my_filter[field] = self.request.query_params[field]
            except KeyError:
                continue
        return my_filter


retrieve_attendee = AttendeeViewSet.as_view({
    'get': 'retrieve'
})

list_attendee = AttendeeViewSet.as_view({
    'get': 'list'
})

create_attendee = AttendeeViewSet.as_view({
    'post': 'create'
})

update_attendee = AttendeeViewSet.as_view({
    'put': 'update'
})

delete_attendee = AttendeeViewSet.as_view({
    'delete': 'destroy'
})
