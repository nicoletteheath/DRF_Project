from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, PledgeDetailSerializer
from .permissions import IsOwnerOrReadOnly, IsNotOwner

class ProjectList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
        ]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )    
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )    

class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
        ]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )  

    def delete(self, request, pk):
            project = self.get_object(pk)
            self.check_object_permissions(request, project)
            try:
                project.delete()
                return Response(status=status.HTTP_200_OK)
            except Project.DoesNotExist:
                raise Http404
         

class PledgeList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsNotOwner
        ]
    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )    
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )    

class PledgeDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
        ]
    def get_object(self, pk):
        try:
            return Pledge.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        self.check_object_permissions(request, pledge)
        data = request.data
        serializer = PledgeDetailSerializer(
            instance=pledge,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )  

    def delete(self, request, pk):
            pledge = self.get_object(pk)
            self.check_object_permissions(request, pledge)
            try:
                pledge.delete()
                return Response(status=status.HTTP_200_OK)
            except Pledge.DoesNotExist:
                raise Http404

