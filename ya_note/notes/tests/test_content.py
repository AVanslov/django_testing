from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

COUNT_OF_NOTES_PER_PAGE = 11


class TestDetailPage(TestCase):
    LIST_OF_NOTES_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Винни Пух')
        cls.reader = User.objects.create(username='Пятачок')
        cls.note = Note.objects.create(
            title='Бухтелка',
            text='Трам-Па-Па-Пам-Тарам-Пам-Пам',
            author=cls.author,
        )

    def test_visibility_notes_on_list_page(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_OF_NOTES_URL)
        self.assertIn(self.note, response.context['object_list'])

    def test_visibility_notes_other_author(self):
        self.client.force_login(self.reader)
        response = self.client.get(self.LIST_OF_NOTES_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_authorized_client_has_form_on_add_and_edit_pages(self):
        self.client.force_login(self.author)
        urls = (
            ('notes:edit', (self.note.slug,)),
            ('notes:add', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
