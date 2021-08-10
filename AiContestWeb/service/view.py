import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

import pytz
from rest_framework import views, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from AiContestWeb.attendee.model import Attendee
from AiContestWeb.contest.model import Contest
from AiContestWeb.service import utils


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
class FileUploadView(views.APIView):
    parser_classes = [MultiPartParser]
    file_upload_dir = Path(__file__).resolve().parent.parent.joinpath('upload-files')

    def post(self, request, *args, **kwargs):
        try:
            contest_id = kwargs['contest_id']
            user = request.user.myuser
            user_id = user.id
            try:
                contest = Contest.objects.get(id=contest_id)
            except Exception:
                return Response(data={'detail': 'This contest is not exist.'}, status=status.HTTP_404_NOT_FOUND)

            if not (user.is_creator or user.is_staff):
                try:
                    attendee = Attendee.objects.get(contest_id=contest_id, user_id=user_id)
                except Exception:
                    return Response(data={'detail': 'User has not been applied for this contest.'},
                                    status=status.HTTP_404_NOT_FOUND)

            if contest.begin > pytz.utc.localize(datetime.now()) or pytz.utc.localize(datetime.now()) > contest.end:
                return Response(data={'detail': 'This contest has already closed.'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            # extract all zip files into attendee or creator folder defined by contest_id and user_id
            path_to_create = Path.joinpath(self.file_upload_dir, str(contest_id))
            os.makedirs(name=path_to_create, exist_ok=True)
            shutil.rmtree(path=path_to_create.joinpath(str(user_id)), ignore_errors=True)
            file_obj = zipfile.ZipFile(request.data['file'])
            file_obj.extractall(path=path_to_create)
            os.rename(src=path_to_create.joinpath(file_obj.filename.split('.')[0]),
                      dst=path_to_create.joinpath(str(user_id)))

            # Do nothing else if creator upload code
            if user.is_creator or user.is_staff:
                return Response(status=status.HTTP_204_NO_CONTENT)

            # Calculate result for attendee
            if user.is_student:
                creator_dir = self.get_creator_file_path(contest_id, contest.creator.id)

                file_to_run = self.get_file_to_run(contest, user_id)
                try:
                    result = float(utils.run_code_file(file_to_run, creator_dir))
                except Exception:
                    attendee.result = 0
                    attendee.save()
                    return Response(data={'detail': 'Error while calculating result from source code.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # save result to attendee
                attendee.result = result
                attendee.save()
                return Response(data={'result': result}, status=status.HTTP_200_OK)
        except Exception:
            return Response(data={'detail': 'Something went wrong when uploading files. '
                                            'Please contact admin for more information.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        contest_id = kwargs['contest_id']
        user_id = request.user.id
        file_path = Path.joinpath(self.file_upload_dir, str(contest_id), str(user_id))
        files = {}
        if file_path.is_dir():
            files['files'] = os.listdir(file_path)
            return Response(data=files, status=status.HTTP_200_OK)
        else:
            raise APIException('File is not exist.')

    def get_creator_file_path(self, contest_id, creator_id):
        for contest_dir in self.file_upload_dir.iterdir():
            if contest_dir.is_dir() and contest_dir.name.__eq__(str(contest_id)):
                for creator_dir in contest_dir.iterdir():
                    if creator_dir.is_dir() and creator_dir.name.__eq__(str(creator_id)):
                        return creator_dir

    def get_file_to_run(self, contest, user_id):
        contest_id = contest.id
        extensions = self.get_available_extensions(contest)
        for contest_dir in self.file_upload_dir.iterdir():
            if contest_dir.is_dir() and contest_dir.name.__eq__(str(contest_id)):
                for attendee_dir in contest_dir.iterdir():
                    if attendee_dir.is_dir() and attendee_dir.name.__eq__(str(user_id)):
                        for file in attendee_dir.iterdir():
                            if utils.check_right_extension(file=file, extensions=extensions):
                                return file

    def get_available_extensions(self, contest):
        extensions = []
        if contest.is_java_available:
            extensions.append('java')
        if contest.is_cpp_available:
            extensions.append('cpp')
        if contest.is_python_available:
            extensions.append('py')
        return extensions


upload_file = FileUploadView.as_view()
