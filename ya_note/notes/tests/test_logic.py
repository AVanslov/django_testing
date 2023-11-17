from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreator(TestCase):
    NOTE_TITLE = 'План похода к Кролику'
    NOTE_TEXT = (
        'Подарю ка я ему корзину, чтобы ему было удобно собирать морковку'
    )

    @classmethod
    def setUpTestData(cls):
        cls.url_add = reverse('notes:add')
        cls.url_list = reverse('notes:list')
        cls.url_success = reverse('notes:success')
        cls.user = User.objects.create(username='Тигруля')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
        }

    def test_anonymous_user_cant_create_notes(self):
        self.client.post(self.url_add, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url_add, data=self.form_data)
        self.assertRedirects(response, self.url_success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.author, self.user)

    def test_user_cant_use_used_slug(self):
        self.auth_client.post(self.url_add, data=self.form_data)
        response = self.auth_client.post(self.url_add, data=self.form_data)
        note = Note.objects.get()
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=note.slug + WARNING
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_slug_is_translit_title(self):
        self.auth_client.post(self.url_add, data=self.form_data)
        note = Note.objects.get()
        self.assertEqual(note.slug, slugify(note.title))


class TestNoteEditDelete(TestCase):

    NOTE_TEXT = (
        'Трам-Па-Па-Пам-Тарам-Пам-Пам'
    )
    NEW_NOTE_TEXT = (
        'Пара-ра-ра-ра-рам. Пуру-ру-ру-рум. Тар-ра-ра-рам. Пум-пум. Пум-пум.'
    )

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Винни Пух')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Пятачок')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Бухтелка',
            text=cls.NOTE_TEXT,
            author=cls.author,
        )
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.done_url = reverse('notes:success')
        cls.form_data = {
            'title': 'Бухтелка',
            'text': cls.NEW_NOTE_TEXT,
        }

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.done_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_note_of_another_uther(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.done_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)
