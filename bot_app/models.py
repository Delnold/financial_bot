from django.db import models
import json


class User(models.Model):
    user_id = models.IntegerField(null=False, unique=True)
    username = models.TextField(null=True, unique=True)
    first_name = models.TextField(null=True, unique=False)
    last_name = models.TextField(null=True, unique=False)


class Savings(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, unique=False, null=False)
    savings_type = models.TextField(unique=False)
    quantity = models.IntegerField(unique=False, null=True)


class UserStateManager(models.Manager):
    def create_state(self, user, command, current_state):
        try:
            user_state = self.model(user=user, command=command, current_state=current_state)
            user_state.save()
        except Exception as e:
            print(f"Retard: {e}")

    def update_state(self, user, new_state):
        try:
            user_state = self.get(user=user)
            user_state.current_state = new_state
            user_state.save()
        except Exception as e:
            print(e)

    def delete_state(self, user):
        try:
            user_state = self.get(user=user)
            user_state.delete()
        except UserState.DoesNotExist:
            pass

    def get_state(self, user):
        try:
            user_state = self.get(user=user)
            return user_state
        except UserState.DoesNotExist:
            return None


class UserState(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, unique=True, null=False)
    command = models.CharField(max_length=50, null=False)
    current_state = models.IntegerField(null=True)
    data_state = models.TextField(null=True)

    objects = UserStateManager()

    def __str__(self):
        return f"User ID: {self.user.user_id}, Command: {self.command}, Current State: {self.current_state}"

    def get_data_state(self):
        if self.data_state:
            return json.loads(self.data_state)
        return {}

    def set_data_state(self, value):
        self.data_state = json.dumps(value)
        self.save()

    def update_data_state(self, update_value):
        current_data_state = self.get_data_state()
        current_data_state.update(update_value)
        self.set_data_state(current_data_state)