from django.db import models


class UserModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    about = models.TextField()
    avatar = models.FileField()


class ChatModel(models.Model):
    name = models.CharField(max_length=255)
    subscribers = models.ManyToManyField(
        "UserModel", related_name="chats", through="ChatSubscriptionModel"
    )


class ChatSubscriptionModel(models.Model):
    user = models.ForeignKey(
        "UserModel", related_name="chat_subscriptions", on_delete=models.CASCADE
    )
    chat = models.ForeignKey(
        "ChatModel", related_name="chat_subscriptions", on_delete=models.CASCADE
    )


class MessageModel(models.Model):
    chat = models.ForeignKey(
        "ChatModel", related_name="messages", on_delete=models.CASCADE
    )
    text = models.TextField()
