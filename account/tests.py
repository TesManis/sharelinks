from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase

from account.views import daftar, login, logout


class DaftarViewTests(TestCase):
    def setUp(self):
        self.url = reverse('daftar')
        self.response = self.client.get(self.url)

    def test_daftar_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_daftar_resolve(self):
        view = resolve(self.url)
        self.assertEquals(view.func, daftar)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)


class DaftarSuccessTest(TestCase):
    def setUp(self):
        self.url, self.login_url = reverse('daftar'), reverse('login')
        data = {
            'username': "testuser",
            'password1': "testpass77",
            'password2': "testpass77",
        }
        self.response = self.client.post(self.url, data)
        self.home_url = reverse('post:home')

    def test_user_is_registered(self):
        assert User.objects.get(username='testuser') is not None

    def test_redirect(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_logged_in(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class DaftarFailTest(TestCase):
    def setUp(self):
        self.url = reverse('daftar')
        data = {}
        self.response = self.client.post(self.url, data)
        self.home_url = reverse('post:home')

    def test_daftar_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_not_created(self):
        self.assertFalse(User.objects.exists())


class LoginViewTest(TestCase):
    def test_daftar_status_code(self):
        resp = self.client.get(reverse('login'))
        self.assertEquals(resp.status_code, 200)

    def test_daftar_resolve(self):
        view = resolve(reverse('login'))
        self.assertEquals(view.func, login)


class LoginSuccessTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='testuser',
            password='testpass77'
        )
        self.home_url = reverse('post:home')
        self.login_url = reverse('login')
        # login
        self.response = self.client.post(self.login_url, {
            'username': "testuser",
            'password': "testpass77",
        })

    def test_status_code(self):
        """
        Must be redirected
        """
        self.assertNotEqual(self.response.status_code, 200)

    def test_redirect(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_is_logged_in(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        response = self.client.get('logout')
        user = response.context.get('user')
        self.assertFalse(user)
