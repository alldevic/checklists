from rest_framework import serializers
from . import models
from user_profile import models as umodels


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('id', 'text', 'order', 'required', 'type', 'choices')


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = models.Survey
        fields = ('id', 'name', 'description', 'questions')


class SurveyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Survey
        fields = ('id', 'name', 'description')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = ('id', 'name', 'date_from', 'date_to', 'checklists')


class ResponseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Response
        fields = ('id', 'created', 'updated', 'survey')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'question', 'body')


# Update ?
class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.Response
        # 'interview_uuid'
        fields = ('id', 'created', 'updated', 'survey', "answers")

    def create(self, validated_data):
        profile_data = validated_data.pop('answers')
        response = models.Response.objects.create(**validated_data)

        for i in profile_data:
            models.Answer.objects.create(response=response, **i)
        return response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = umodels.UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'position')


# Begin report generation
class ReportQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('id', 'text', 'order', 'required', 'type', 'choices', 'key_choices')


class ReportResponseSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    def get_answers(self, obj):
        answers = models.Answer.objects.all()
        return AnswerSerializer(answers, many=True).data

    def get_questions(self, obj):
        questions = models.Question.objects.all()
        return ReportQuestionSerializer(questions, many=True).data

    class Meta:
        model = models.Response
        fields = ('id', 'created', 'updated', "answers", 'questions')


class ReportGetEntitySerializer(serializers.ModelSerializer):
    responses = serializers.SerializerMethodField()
    checklists = SurveyListSerializer(many=True)

    def get_responses(self, obj):
        responses = models.Response.objects.all()
        return ReportResponseSerializer(responses, many=True).data

    class Meta:
        model = models.Report
        fields = ('id', 'name', 'date_from', 'date_to', 'checklists', 'responses')

# End report generation
