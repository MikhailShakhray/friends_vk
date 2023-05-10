from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_from_applications")
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_to_applications")
    status = models.CharField(max_length=50, choices=('Отправлено', 'Приянято', 'Откланено'))
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        unique_together = ('user_from', 'user_to')

    def __str__(self):
        return f"from:{self.user_from} to {self.user_to} status {self.status}"


class Friends(models.Model):
    friend1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends1')
    friend2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends2')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f'{self.user1} - {self.user2}'
