import os
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task, Comment, TaskFile
import json


class TaskManagerTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'assigned_to_id': self.user.id,
            'deadline': '2024-06-30T12:00:00Z',
            'reminder': '2024-06-29T12:00:00Z'
        }
        self.task = Task.objects.create(**self.task_data)

    def tearDown(self):
        # Удаление файлов
        for task_file in TaskFile.objects.all():
            if os.path.isfile(task_file.file.path):
                os.remove(task_file.file.path)

    def test_create_task(self):
        response = self.client.post('/api/tasks/', self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(id=2).title, 'Test Task')

    def test_update_task(self):
        updated_data = self.task_data.copy()
        updated_data['title'] = 'Updated Task'
        response = self.client.put(f'/api/tasks/{self.task.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task.id).title, 'Updated Task')

    def test_delete_task(self):
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_comment(self):
        comment_data = {
            'task': self.task.id,
            'text': 'Test Comment',
            'author': self.user.id
        }
        response = self.client.post('/api/comments/', comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get(id=1).text, 'Test Comment')

    def test_create_task_file(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
            temp_file.write(b'Test file content')
            temp_file.seek(0)
            file_data = {
                'task': self.task.id,
                'file': temp_file
            }
            response = self.client.post('/api/files/', file_data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(TaskFile.objects.count(), 1)
            self.assertTrue(TaskFile.objects.get(id=1).file.name.endswith('.txt'))

    def test_user_registration(self):
        user_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            're_password': 'newpassword123',
            'email': 'newuser@example.com'
        }
        response = self.client.post('/api/auth/users/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=2).username, 'newuser')

    def test_jwt_authentication(self):
        auth_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post('/api/auth/jwt/create/', auth_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', json.loads(response.content))
        self.assertIn('refresh', json.loads(response.content))

    def test_task_filtering(self):
        Task.objects.create(title='Another Task', description='Another Description', assigned_to=self.user)
        response = self.client.get('/api/tasks/?assigned_to=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_task_sorting(self):
        Task.objects.create(title='Another Task', description='Another Description', assigned_to=self.user,
                            deadline='2024-07-01T12:00:00Z')
        response = self.client.get('/api/tasks/?ordering=deadline')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tasks = json.loads(response.content)
        self.assertEqual(tasks[0]['title'], 'Test Task')
        self.assertEqual(tasks[1]['title'], 'Another Task')
