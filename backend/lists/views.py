from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, \
    CreateModelMixin, UpdateModelMixin,     DestroyModelMixin
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user_profile import models as umodels
from . import models, serializers
import datetime


class SurveyListViewset(GenericViewSet, ListModelMixin):
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveyListSerializer


class ResponseListViewset(GenericViewSet, ListModelMixin):
    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseListSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return models.Response.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = models.Response.objects.all()

        fr = request.query_params.get("from", None)
        if (fr):
            queryset = queryset.filter(created__gte=datetime.date(fr))

        to = request.query_params.get("to", None)
        if (to):
            queryset = queryset.filter(created__lte=datetime.date(to))

        lsts = request.query_params.get("lists", None)
        if lsts:
            lists = [int(x) for x in lsts.split(',')]
            queryset = queryset.filter(survey__in=lists)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SurveyViewset(GenericViewSet, RetrieveModelMixin):
    questions = models.Question.objects.all()
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveySerializer


class ResponseViewset(GenericViewSet, CreateModelMixin,
                      RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    answers = models.Answer.objects.all()
    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.update(user=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return models.Response.objects.all()

# Report viewsets


class ReportListViewset(GenericViewSet, ListModelMixin,
                        CreateModelMixin, DestroyModelMixin):
    queryset = models.Report.objects.prefetch_related('checklists').all()
    serializer_class = serializers.ReportSerializer
    permission_classes = (IsAdminUser,)


class ReportViewset(GenericViewSet, RetrieveModelMixin):
    queryset = models.Report.objects.all()
    serializer_class = serializers.ReportGetEntitySerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
