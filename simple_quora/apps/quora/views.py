from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

from apps.quora.models import Question, Answer, Like
from apps.quora.forms import QuestionForm, AnswerForm

class QuestionsListView(ListView):
    model = Question
    paginate_by = 5
    ordering = ["-created_at"]
    context_object_name = "questions"
    template_name = "questions.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_form"] = QuestionForm()
        context["is_paginated"] = True
        return context

class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail.html"
    context_object_name = "question"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = Answer.objects.filter(question__id=self.get_object().id).order_by("-created_at")
        paginator = Paginator(answers, 4)
        page = self.request.GET.get("page")
        context["answers_page"] = paginator.get_page(page)
        context["can_add_answer"] = self.get_object().user != self.request.user
        return context

class AddQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    context_object_name = "question_form"
    template_name = "questions.html"
    success_url = reverse_lazy("questions-list-view")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    context_object_name = "question_form"
    template_name = "questions.html"
    success_url = reverse_lazy("questions-list-view")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return HttpResponseForbidden("You are not allowed to edit this question.")

        return super().dispatch(request, *args, **kwargs)
    

class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name = "question_form"
    template_name = "questions.html"
    success_url = reverse_lazy("questions-list-view")
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return HttpResponseForbidden("You are not allowed to edit this question.")

        return super().dispatch(request, *args, **kwargs)

class AddAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    context_object_name = "answer_form"
    template_name = "question_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=self.kwargs["question_id"])
        if self.question.user == request.user:
            return HttpResponseForbidden("You are not allowed to add answer to this question.")
        return super().dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question = self.question
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("question-detail-view", args=[self.question.id])

class UpdateAnswerView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    context_object_name = "answer_form"
    template_name = "question_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return HttpResponseForbidden("You are not allowed to edit this answer.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("question-detail-view", args=[self.get_object().question.id])
    
class DeleteAnswerView(LoginRequiredMixin, DeleteView):
    model = Answer
    context_object_name = "answer_form"
    template_name = "question_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return HttpResponseForbidden("You are not allowed to delete this answer.")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("question-detail-view", args=[self.get_object().question.id])
    
class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        answer = get_object_or_404(Answer, id=kwargs.get("answer_id"))
        if Like.objects.filter(user=request.user, answer=answer).exists():
            Like.objects.filter(user=request.user, answer=answer).delete()
            answer.likes -= 1
            liked = False
        else:
            Like.objects.create(answer = answer, user = request.user)
            answer.likes += 1
            liked = True
        answer.save()

        return JsonResponse({
            "liked": liked,
            "like_count": answer.likes,
        })