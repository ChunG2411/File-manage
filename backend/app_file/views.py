from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from django.http import FileResponse

from .models import Folder, File, Saved
from .serializers import FolderSerializers, FileSerializers, FolderDetailSerializer
from manage_file.function import check_validate, get_path_file, check_token_blacklisted
from app_user.models import Profile, LimitAction

# Create your views here.


@permission_classes([permissions.IsAuthenticated])
@check_token_blacklisted
class FolderView(APIView):
    def get(self, request, id):
        folder = Folder.objects.get(id=id)
        if folder.created_by == request.user or folder.permissions == '1':
            serializer = FolderSerializers(folder)
            return Response(serializer.data, status=200)
        else:
            return Response("You don't have permission", status=400)

    def post(self, request):
        parent_id = request.data.get('parent')
        name = request.data.get('name')

        if check_validate(name):
            return Response("Enter a valid name", status=400)
        if parent_id:
            parent = Folder.objects.get(id=parent_id)
            if parent.created_by != request.user:
                return Response("You don't have permission", status=400)
            folder = Folder.objects.create(
                name=name, parent=parent, created_by=request.user)
        else:
            folder = Folder.objects.create(name=name, created_by=request.user)

        return Response({
            'id': str(folder.id),
            'name': folder.name,
            'permissions': folder.permissions
        }, status=200)

    def delete(self, request, id):
        folder = Folder.objects.get(id=id)

        if folder.created_by != request.user:
            return Response("You don't have permission", status=400)

        if folder.deleted:
            folder.delete()
            return Response("Deleted", status=200)
        else:
            saved = Saved.objects.get(user=request.user)
            if folder in saved.folder.all():
                saved.folder.remove(folder)
            folder.deleted = True
            folder.save()
            return Response("Move to trash can", status=200)

    def patch(self, request, id):
        folder = Folder.objects.get(id=id)

        if folder.created_by != request.user:
            return Response("You don't have permission", status=400)

        folder.deleted = False
        folder.save()
        return Response("Restore successful", status=200)


@permission_classes([permissions.IsAuthenticated])
@check_token_blacklisted
class FolderDetailView(APIView):
    def get(self, request, id):
        folder = Folder.objects.get(id=id)
        serializer = FolderDetailSerializer(
            folder, context={'request': request})
        return Response(serializer.data, status=200)

    def put(self, request, id):
        name = request.data.get('name')
        description = request.data.get('description')
        parent = request.data.get('parent')
        permissions = request.data.get('permissions')

        folder = Folder.objects.get(id=id)
        if folder.created_by != request.user:
            return Response("You don't have permission", status=400)
        if name:
            if check_validate(name):
                return Response("Name not valid", status=400)
            folder.name = name
        if description and not check_validate(description):
            folder.description = description
        if parent:
            if parent == 'home':
                folder.parent = None
            else:
                folder.parent = Folder.objects.get(id=parent)
        if permissions:
            folder.permissions = permissions
        folder.save()

        return Response(FolderDetailSerializer(folder, context={'request': request}).data, status=200)

    def patch(self, request, id):
        status = request.query_params.get('status')

        folder = Folder.objects.get(id=id)
        saved = Saved.objects.get(user=request.user)

        if folder.deleted:
            return Response("Restore first", status=400)

        if status == 'unsave':
            if folder in saved.folder.all():
                saved.folder.remove(folder)
                return Response("Unsaved", status=200)
            else:
                return Response("Unsaved", status=200)
        else:
            saved.folder.add(folder)
            return Response("Saved", status=200)


@permission_classes([permissions.IsAuthenticated])
@check_token_blacklisted
class FileView(APIView):
    def post(self, request):
        parent = request.data.get('parent')
        file_upload = request.FILES.get('file')

        if parent:
            folder = Folder.objects.get(id=parent)
            if folder.created_by != request.user:
                return Response("You don't have permission", status=400)
        else:
            folder = None

        size = file_upload.size // 1024
        profile = Profile.objects.get(user=request.user)
        limit = LimitAction.objects.get(user=request.user)

        if limit.upload >= profile.limit_upload:
            return Response("Limit upload", status=200)
        if limit.store + size > profile.store:
            return Response("Not enough store", status=400)

        limit.store += size
        limit.upload += 1
        file = File.objects.create(name=file_upload.name,
                                   file=file_upload, size=size,
                                   parent=folder, created_by=request.user)
        limit.save()
        return Response(FileSerializers(file, context={'request': request}).data, status=200)

    def delete(self, request, id):
        file = File.objects.get(id=id)

        if file.created_by != request.user:
            return Response("You don't have permission", status=400)

        if file.deleted:
            file.delete()
            limit = LimitAction.objects.get(user=request.user)
            limit.store -= file.size
            limit.save()
            return Response("Deleted", status=200)
        else:
            saved = Saved.objects.get(user=request.user)
            if file in saved.file.all():
                saved.file.remove(file)
            file.deleted = True
            file.save()
            return Response("Move to trash can", status=200)

    def patch(self, request, id):
        file = File.objects.get(id=id)

        if file.created_by != request.user:
            return Response("You don't have permission", status=400)

        file.deleted = False
        file.save()
        return Response("Restore successful", status=200)


@permission_classes([permissions.IsAuthenticated])
@check_token_blacklisted
class FileDetailView(APIView):
    def get(self, request, id):
        file = File.objects.get(id=id)
        serializer = FileSerializers(
            file, context={'request': request})
        return Response(serializer.data, status=200)

    def put(self, request, id):
        name = request.data.get('name')
        description = request.data.get('description')
        parent = request.data.get('parent')
        permissions = request.data.get('permissions')

        file = File.objects.get(id=id)
        if file.created_by != request.user:
            return Response("You don't have permission", status=400)
        if name:
            if check_validate(name):
                return Response("Name not valid", status=400)
            ext = file.name.split('.')[-1]
            file.name = name + '.' + ext
        if description and not check_validate(description):
            file.description = description
        if parent:
            if parent == 'home':
                file.parent = None
            else:
                file.parent = Folder.objects.get(id=parent)
        if permissions:
            file.permissions = permissions
        file.save()

        return Response(FileSerializers(file, context={'request': request}).data, status=200)

    def patch(self, request, id):
        status = request.query_params.get('status')

        file = File.objects.get(id=id)
        saved = Saved.objects.get(user=request.user)

        if file.deleted:
            return Response("Restore first", status=400)

        if status == 'unsave':
            if file in saved.file.all():
                saved.file.remove(file)
                return Response("Unsaved", status=200)
            else:
                return Response("Unsaved", status=200)
        else:
            saved.file.add(file)
            return Response("Saved", status=200)   


@api_view(['GET'])
def downloadFile(request, id):
    file = File.objects.get(id=id)
    if file.permissions == '1' or file.created_by == request.user:
        file_read = open(get_path_file(file.file.url), 'rb')
        response = FileResponse(file_read)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.name)
        return response
    else:
        return Response("You don't have permission", status=400)


@permission_classes([permissions.IsAuthenticated])
@check_token_blacklisted
class HomeView(APIView):
    def get(self, request):
        type = request.query_params.get('type')

        if type == 'trash':
            folder = Folder.objects.filter(
                deleted=True, created_by=request.user)
            file = File.objects.filter(
                deleted=True, created_by=request.user)
        elif type == 'saved':
            saved = Saved.objects.get(user=request.user)
            folder, file = saved.folder.all(), saved.file.all()
        else:
            folder = Folder.objects.filter(
                deleted=False, created_by=request.user, parent=None)
            file = File.objects.filter(
                deleted=False, created_by=request.user, parent=None)

        return Response({
            'path': '',
            'folder': [{
                        'id': str(i.id),
                        'name': i.name,
                        'permissions': i.permissions,
                        'delete': i.deleted,
                        'update_at': i.updated_at
                        } for i in folder],
            'file': [{
                'id': str(i.id),
                'name': i.name,
                'permissions': i.permissions,
                'file': i.file.url,
                'delete': i.deleted,
                'update_at': i.updated_at
            } for i in file]
        }, status=200)


@permission_classes([permissions.IsAuthenticated])
@check_token_blacklisted
class SearchView(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        folder = Folder.objects.filter(name__contains = search.lower())

        return Response({
            'folder': [{
                    'id': str(i.id),
                    'name': i.name,
                    'permissions': i.permissions,
                    'delete': i.deleted,
                    'update_at': i.updated_at
                    } for i in folder]
        }, status=200)
