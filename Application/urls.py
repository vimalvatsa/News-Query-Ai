from django.urls import path
from Application.views.Document import (
    DocumentClass,
    HealthCheckView,
    CheckDocExistenceClass,
)
from Application.views.Chat import DocChatClass, ResultFileClass
from Application.views.DocAssess import DocAssessClass

urlpatterns = [
    path("documents", DocumentClass.as_view(), name="documents-detail"),
    path("search", DocChatClass.as_view(), name="response-detail"),
    # path("check", CheckDocExistenceClass.as_view(), name="check-doc"),
    # path("doc-assess", DocAssessClass.as_view(), name="doc-assess"),
    # path('result-files', ResultFileClass.as_view(), name='result-files'),
    path("health", HealthCheckView.as_view(), name="health"),
]
