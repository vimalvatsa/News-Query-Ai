from django.db import models
from django.utils import timezone

class Tenant(models.Model):
    modelID = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=60)
    tenant_key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.modelID + self.model_name
    
    
class Document(models.Model):
    documentID =models.IntegerField(primary_key=True)
    documentName = models.CharField(max_length=200)
    doc_key = models.CharField(max_length=200)

    def __str__(self):
        return self.documentID


class Session(models.Model):
    sessionID = models.AutoField(primary_key=True)
    startDateTime = models.DateTimeField(auto_now_add=True)
    endDateTime = models.DateTimeField(auto_now_add=True)
    document_fk=models.ForeignKey(Document, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sessionID


class ChatBox(models.Model):
    chatID = models.AutoField(primary_key=True)
    user_query = models.TextField()
    answer = models.TextField()
    result_content = models.TextField(blank=True)
    starttime = models.DateTimeField(auto_now_add=True)
    session_fk2 = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    top_k = models.IntegerField(default=10)
    threshold = models.FloatField(default=0.5)

    def __str__(self):
        return self.chatID
    
#writing the models for creating an api for converting the answer or result obtained from the chatbot to an excel file 
class ResultFile(models.Model):
    resultID = models.AutoField(primary_key=True)
    documentID = models.ForeignKey(Document, on_delete=models.CASCADE)
    answer = models.ForeignKey(ChatBox, on_delete=models.CASCADE)
    word_file = models.FileField(upload_to='word_files/')
    session_fk3 = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.resultID

class UserAPICall(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    call_count = models.IntegerField(default=0)
    last_call = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user_id} - {self.call_count} calls"