from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Task, Category, Priority


class UserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff_user = TaskViewTest.create_user(is_staff=True, username='staff')
        self.non_staff_user = TaskViewTest.create_user(is_staff=False, username='non_staff')

        self.staff_token = TaskViewTest.create_token(self.staff_user)
        self.non_staff_token = TaskViewTest.create_token(self.non_staff_user)

    def test_staff_user_can_change_any_user_password(self):
        # админ может изменить пароль любого пользователя.
        self.client.force_authenticate(user=self.staff_user)

        response1 = self.client.patch(f'/api/users/{self.staff_user.pk}/',
                                     user=self.staff_user,
                                     data={'password': 'new_password'})
        self.assertEqual(response1.status_code, 200)
        self.assertEqual('new_password', response1.data.get('password'))

        response2 = self.client.patch(f'/api/users/{self.non_staff_user.pk}/',
                                      user=self.staff_user,
                                      data={'password': 'new_password'})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual('new_password', response2.data.get('password'))

    def test_non_staff_user_can_change_own_password(self):
        # пользователь может изменить свой пароль.
        self.client.force_authenticate(user=self.non_staff_user)

        response1 = self.client.patch(f'/api/users/{self.non_staff_user.pk}/',
                                      user=self.non_staff_user,
                                      data={'password': 'new_password'})
        self.assertEqual(response1.status_code, 200)
        self.assertEqual('new_password', response1.data.get('password'))

        response2 = self.client.patch(f'/api/users/{self.staff_user.pk}/',
                                      user=self.non_staff_user,
                                      data={'password': 'new_password'})
        self.assertEqual(response2.status_code, 403)

        non_staff_user2 = TaskViewTest.create_user(is_staff=False, username='non_staff2')
        response3 = self.client.patch(f'/api/users/{non_staff_user2.pk}/',
                                      user=self.non_staff_user,
                                      data={'password': 'new_password'})
        self.assertEqual(response3.status_code, 403)


class TaskViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff_user = self.create_user(is_staff=True, username='staff')
        self.non_staff_user = self.create_user(is_staff=False, username='non_staff')
        self.staff_token = self.create_token(self.staff_user)
        self.non_staff_token = self.create_token(self.non_staff_user)

        self.task1 = self.create_task(created_by=self.staff_user.username)
        self.task2 = self.create_task(created_by=self.non_staff_user.username)

    def test_staff_user_can_get_all_tasks(self):
        # админ может получить все задачи.
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(f'/api/tasks/', user=self.staff_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response.data))

    def test_non_staff_user_can_get_own_tasks(self):
        # пользователь может получить только свои задачи.
        self.client.force_authenticate(user=self.non_staff_user)
        response = self.client.get(f'/api/tasks/', user=self.non_staff_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.task2.pk, response.data[0].get('id'))

    def test_staff_user_can_get_any_tasks_by_id(self):
        # админ может получить любую задачу по айди.
        self.client.force_authenticate(user=self.staff_user)

        response1 = self.client.get(f'/api/tasks/{self.task2.pk}/', user=self.staff_user)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(self.task2.pk, response1.data.get('id'))

        # в том числе удаленную.
        task3 = self.create_task(created_by=self.non_staff_user.username, deleted=True)
        response2 = self.client.get(f'/api/tasks/{task3.pk}/', user=self.staff_user)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(task3.pk, response2.data.get('id'))

    def test_non_staff_user_can_get_only_own_not_deleted_task_by_id(self):
        # пользователь может получить только свою неудаленную задачу по айди.
        self.client.force_authenticate(user=self.non_staff_user)

        response1 = self.client.get(f'/api/tasks/{self.task2.pk}/', user=self.non_staff_user)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(self.task2.pk, response1.data.get('id'))

        response2 = self.client.get(f'/api/tasks/{self.task1.pk}/', user=self.non_staff_user)
        self.assertEqual(response2.status_code, 404)

        task3 = self.create_task(created_by=self.non_staff_user.username, deleted=True)
        response2 = self.client.get(f'/api/tasks/{task3.pk}/', user=self.non_staff_user)
        self.assertEqual(response2.status_code, 404)

    def test_staff_user_can_update_any_task(self):
        # админ может изменить любую задачу по айди.
        self.client.force_authenticate(user=self.staff_user)

        response1 = self.client.patch(f'/api/tasks/{self.task1.pk}/', user=self.staff_user)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(self.task1.pk, response1.data.get('id'))

        response2 = self.client.patch(f'/api/tasks/{self.task2.pk}/', user=self.staff_user)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(self.task2.pk, response2.data.get('id'))

    def test_non_staff_user_can_update_only_own_not_deleted_task(self):
        # пользователь может изменить только свою неудаленную задачу по айди.
        self.client.force_authenticate(user=self.non_staff_user)

        response1 = self.client.patch(f'/api/tasks/{self.task2.pk}/', user=self.non_staff_user)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(self.task2.pk, response1.data.get('id'))

        response2 = self.client.patch(f'/api/tasks/{self.task1.pk}/', user=self.non_staff_user)
        self.assertEqual(response2.status_code, 403)

        task3 = self.create_task(created_by=self.non_staff_user.username, deleted=True)
        response2 = self.client.patch(f'/api/tasks/{task3.pk}/', user=self.non_staff_user)
        self.assertEqual(response2.status_code, 404)

    def test_staff_user_can_delete(self):
        # админ может окончательно удалить любую задачу.
        instance = self.create_task(created_by=self.staff_user.username)
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.delete(f'/api/tasks/{instance.pk}/', user=self.staff_user)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=instance.pk).exists())

    def test_non_staff_user_can_delete_own_object(self):
        # пользователь может удалить (изменить статус) свою задачу.
        instance = self.create_task(created_by=self.non_staff_user.username)
        self.client.force_authenticate(user=self.non_staff_user)
        response = self.client.delete(f'/api/tasks/{instance.pk}/', user=self.non_staff_user)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Task.objects.filter(pk=instance.pk, deleted=True).exists())

    def test_non_staff_user_cannot_delete_others_object(self):
        # пользователь не может удалить чужую задачу
        instance = self.create_task(created_by=self.staff_user.username)
        self.client.force_authenticate(user=self.non_staff_user)
        response = self.client.delete(f'/api/tasks/{instance.pk}/', user=self.non_staff_user)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(pk=instance.pk, deleted=False).exists())

    def user_cannot_delete_already_deleted_object(self):
        # пользователь не может удалить уже удаленный объект
        instance = self.create_task(created_by=self.non_staff_user.username, deleted=True)
        self.client.force_authenticate(user=self.non_staff_user)
        response = self.client.delete(f'/api/tasks/{instance.pk}/', user=self.non_staff_user)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=instance.pk, deleted=True).exists())

    @staticmethod
    def create_user(username, is_staff=False):
        # тестовый пользователь
        from django.contrib.auth.models import User
        user = User.objects.create_user(username=username, password='test_password', is_staff=is_staff)
        return user

    @staticmethod
    def create_token(user):
        token = Token.objects.create(user=user)
        return token

    def create_task(self, created_by, deleted=False):
        category = Category.objects.create(name='category_name')
        priority = Priority.objects.create(name='priority_name')
        task = Task.objects.create(
            created_by=created_by,
            title='title',
            description='description',
            category=category,
            priority=priority,
            deleted=deleted
        )
        return task
