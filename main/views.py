from typing import Any
from django.shortcuts import render
from main import models, forms
from django.views.generic import (
    ListView,
    DetailView,
    FormView
)
from django.views.generic.detail import BaseDetailView, SingleObjectMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin

class Index(ListView):
    model = models.Question
    template_name = 'main/index.html'
    # context_object_name = 'question_list'


class Question(PermissionRequiredMixin, SingleObjectMixin, FormView):
    model = models.Question
    template_name = 'main/question.html'
    form_class = forms.AnswerForm
    permission_required = 'add_answer'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['answer'] = models.Answer.objects.get(
            question =self.get_object(),
            user = self.request.user,
        )
        return data
    
    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.question = self.get_object()
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect('/')
    
    def post(self, request, *args, **kwargs: Any):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object = self.object)
        print("************8", context)
        return self.render_to_response(context)
    
