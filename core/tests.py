from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import Expert, Event
from django.urls import reverse
from uuid import uuid4
# Create your tests here.

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com'
        )
        token = uuid4()
        self.expert = Expert.objects.create(
            name='John Doe',
            email='jdoe@gmail.com',
            description='John Doe is a music artist',
            contact='+27712334567',
            token=token
        )

        self.client.login(username='testuser', password='testpass')

    def test_add_expert(self):
        url = reverse('core:add_expert')
        # Post data
        token = uuid4()
        response = self.client.post(url, {
            'name': 'John Doe',
            'email': 'jdoe@gmail.com',
            'description': 'John Doe is a music artist',
            'contact': '+27712334567',
            'token': token
        })
        # A redirect should occur if the person is successfully added
        self.assertEquals(response.status_code, 302)


    def test_select_expert(self):
        """
          If an expert is successfully selected a redirect is made.
          User will be redirected to select 3 dates and times
          So test if a redirect has been made.
        """
        token = uuid4()
        expert = Expert.objects.create(
            name='John Doe',
            email='jdoe@gmail.com',
            description='John Doe is a music artist',
            contact='+27712334567',
            token=token
        )
        url = reverse("core:select_expert")

        response = self.client.post(url, {
            'expert_id': 1
        })

        self.assertEquals(response.status_code, 302)

    def test_pick_dates(self):
        """
        When a user picks dates then an email is sent to the expert with
        three links to confirm which date they are happy with.
        """
        event = Event.objects.create(
            user=self.user,
            expert=self.expert,
            slug=uuid4()
        )
        url = reverse("core:pick_dates", kwargs={'event_slug': event.slug})

        response = self.client.post(url,{
            'date_1': 'Aug 19, 2021',
            'time_1': '12:00 PM',
            'date_2': 'Aug 19, 2021',
            'time_2': '12:00 PM',
            'date_3': 'Aug 19, 2021',
            'time_3': '12:00 PM',
        })

        self.assertEquals(response.status_code, 302)