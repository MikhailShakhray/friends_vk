from .models import Friends, Users
from django.contrib.auth.models import User
from rest_framework.response import Response


class FriendshipStatusHandler:
    result_messages = {
        "friendship": "friendship",
        "outcoming_application": "outcoming_application",
        "incoming_application": "incoming_application",
        "no_friendship": "no_friendship"
    }

    def friendship_status(self, username1: str, username2: str) -> str:
        username1 = User.objects.get(username=username1)
        username2 = User.objects.get(username=username2)
        # Если есть дружба - возвращаем статус "Дружба"
        if self.is_friendship(username1, username2):
            return self.result_messages["friendship"]
        # Иначе если ищем заявки
        elif self.is_application(username1, username2):
            return self.application_status(username1, username2)
        # Иначе возвращаем, что дружбы нет
        else:
            return self.result_messages["no_friendship"]

    @staticmethod
    def is_friendship(username1: User, username2: User) -> bool:
        return Friendship.objects.filter(user1=username1, user2=username2).exists() or Friends.objects.filter(
            user1=username2, user2=username1).exists()

    @staticmethod
    def is_application(username1: User, username2: User) -> bool:
        return Users.objects.filter(user_from=username1, user_to=username2,
                                              status="Отправлено").exists() or Users.objects.filter(
            user_from=username2, user_to=username1, status="Отправлено").exists()

    def application_status(self, username1: User, username2: User) -> str:
        outcoming_model = Users.objects.filter(user_from=username1, user_to=username2, status="Отправлено")
        incoming_model = Users.objects.filter(user_from=username2, user_to=username1, status="Отправлено")
        if outcoming_model.exists():
            return self.result_messages["outcoming_application"]
        elif incoming_model.exists():
            return self.result_messages["incoming_application"]
        else:
            return self.result_messages["no_friendship"]


def is_there_incoming_application(username1, username2):
    user1 = User.objects.get(username=username1)
    user2 = User.objects.get(username=username2)
    return Users.objects.filter(user_from=user2, user_to=user1,
                                          status="Отправлена").exists()


def create_friendship(username1, username2):
    username1 = User.objects.get(username=username1)
    username2 = User.objects.get(username=username2)
    Friends.objects.create(user1=username1, user2=username2)


def set_application_status(username1, username2, status):
    user1 = User.objects.get(username=username1)
    user2 = User.objects.get(username=username2)
    application = UserApplication.objects.get(user_from=user2, user_to=user1)
    application.status = status
    application.save()


def set_decision(request, to_username, decision):
    if decision == "accepted":
        set_application_status(request.user.username, to_username, "Принято")
        create_friendship(request.user.username, to_username)
    elif decision == "rejected":
        set_application_status(request.user.username, to_username, "Отклонено")
