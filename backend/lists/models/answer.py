# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.db import models

from .question import Question
from .response import Response

from django_q.tasks import async_task
from ..tasks import update_mapnode


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Вопрос",
        related_name="answers",
    )
    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        verbose_name="Отчет",
        related_name="answers",
    )
    created = models.DateTimeField("Creation date", auto_now_add=True)
    updated = models.DateTimeField("Update date", auto_now=True)
    body = models.TextField("Ответ", blank=True, null=True)

    def __init__(self, *args, **kwargs):
        try:
            question = Question.objects.get(pk=kwargs["question_id"])
        except KeyError:
            question = kwargs.get("question")
        body = kwargs.get("body")
        if question and body:
            self.check_answer_body(question, body)
        super(Answer, self).__init__(*args, **kwargs)

    @property
    def values(self):
        if len(self.body) < 3 or self.body[0:3] != "[u'":
            return [self.body]
        #  We do not use eval for security reason but it could work with :
        #  eval(self.body)
        #  It would permit to inject code into answer though.
        values = []
        raw_values = self.body.split(f"', u'")
        nb_values = len(raw_values)
        for i, value in enumerate(raw_values):
            if i == 0:
                value = value[3:]
            if i + 1 == nb_values:
                value = value[:-2]
            values.append(value)
        return values

    def check_answer_body(self, question, body):
        if question.type in [Question.RADIO, Question.SELECT, Question.SELECT_MULTIPLE]:
            choices = question.get_clean_choices()
            if body:
                answers = []
                for i, part in enumerate(body.split("'")):
                    if i % 2 == 1:
                        answers.append(part)

            for answer in answers:
                if answer not in choices:
                    msg = "Impossible answer '{}'".format(body)
                    msg += " should be in {} ".format(choices)
                    raise ValidationError(msg)

    def __str__(self):
        return f"{self.__class__.__name__} to '{self.question}'"

    def save(self, force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):

        res = super().save(force_insert=force_insert,
                           force_update=force_update,
                           using=using,
                           update_fields=update_fields)

        if self.question.type == Question.AUTOCOMPLETE_ADDRESS:
            async_task(update_mapnode, self)

        return res
