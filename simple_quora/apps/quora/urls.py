from django.urls import path

from apps.quora.views import (
    QuestionsListView,
    QuestionDetailView,
    AddQuestionView,
    UpdateQuestionView,
    DeleteQuestionView,
    AddAnswerView,
    UpdateAnswerView,
    DeleteAnswerView,
    ToggleLikeView
)

urlpatterns = [
    path("", QuestionsListView.as_view(), name="questions-list-view"),
    path("add-question/", AddQuestionView.as_view(), name="add_question"),
    path("edit-question/<int:pk>/", UpdateQuestionView.as_view(), name="question-edit-view"),
    path("question-details/<int:pk>/", QuestionDetailView.as_view(), name="question-detail-view"),
    path("add-answer/<int:question_id>/", AddAnswerView.as_view(), name="add_answer"),
    path("delete-question/<int:pk>/", DeleteQuestionView.as_view(), name="question-delete-view"),   
    path("edit-answer/<int:pk>/", UpdateAnswerView.as_view(), name="answer-edit-view"),
    path("delete-answer/<int:pk>/", DeleteAnswerView.as_view(), name="answer-delete-view"),
    path("toggle-answer-like/<int:answer_id>/", ToggleLikeView.as_view(), name="toggle-answer-like")
]
