from http import HTTPStatus
from pytils.translit import slugify

from django.contrib.auth import get_user_model


from notes.forms import WARNING
from notes.models import Note
from notes.tests.constants import (
    NOTE_SLUG,
    NOTE_TEXT,
    NOTE_TITLE,
    SECOND_NOTE_SLUG,
    SECOND_NOTE_TEXT,
    SECOND_NOTE_TITLE,
    UPDATE_NOTE_TEXT,
    CreateTestObjects,
)

User = get_user_model()


class TestNoteCreateEdit(CreateTestObjects):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(
            create_note=True,
            enter_data_into_note_form=True,
            enter_second_data_into_note_form=True,
            update_data_in_note_form=True,
        )

    def test_anonymous_user_cant_create_notes(self):
        notes_count_in_db_befor_try_to_change = Note.objects.count()
        self.client.post(self.url_add, data=self.form_data)
        notes_count_in_db_after_try_to_change = Note.objects.count()
        self.assertEqual(
            notes_count_in_db_befor_try_to_change,
            notes_count_in_db_after_try_to_change,
        )

    def test_user_can_create_note(self):
        notes_count_in_db_befor_try_to_change = Note.objects.count()
        response = self.author_client.post(
            self.url_add, data=self.second_form_data
        )
        notes_count_in_db_after_try_to_change = Note.objects.count()
        self.assertRedirects(response, self.url_success)
        self.assertNotEqual(
            notes_count_in_db_befor_try_to_change,
            notes_count_in_db_after_try_to_change,
        )
        note = Note.objects.get(slug=SECOND_NOTE_SLUG)
        self.assertEqual(
            note.title, self.second_form_data['title'], SECOND_NOTE_TITLE
        )
        self.assertEqual(
            note.text, self.second_form_data['text'], SECOND_NOTE_TEXT
        )
        self.assertEqual(
            note.slug, self.second_form_data['slug'], SECOND_NOTE_SLUG
        )
        self.assertEqual(
            note.author, self.author
        )

    def test_user_cant_use_used_slug(self):
        notes_in_db_befor_try_to_change = list(Note.objects.all())
        response = self.author_client.post(self.url_add, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=Note.objects.get(slug=NOTE_SLUG).slug + WARNING
        )
        notes_in_db_after_try_to_change = list(Note.objects.all())
        self.assertEqual(
            notes_in_db_befor_try_to_change,
            notes_in_db_after_try_to_change,
        )

    def test_slug_is_translit_title(self):
        self.author_client.post(self.url_add, data=self.form_data)
        note = Note.objects.get()
        self.assertEqual(note.slug, slugify(note.title))
        self.assertEqual(
            note.title, NOTE_TITLE
        )
        self.assertEqual(
            note.text, NOTE_TEXT
        )
        self.assertEqual(
            note.author, self.author
        )

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.url_success)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cant_delete_note_of_another_user(self):
        notes_in_db_befor_try_to_change = list(Note.objects.all())
        response = self.reader_client.delete(self.delete_url)
        notes_in_db_after_try_to_change = list(Note.objects.all())
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(
            notes_in_db_befor_try_to_change,
            notes_in_db_after_try_to_change,
        )

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.edit_url, data=self.update_form_data
        )
        self.assertRedirects(response, self.url_success)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, UPDATE_NOTE_TEXT)
        self.assertEqual(
            self.note.title, self.update_form_data['title'], NOTE_TITLE
        )
        self.assertEqual(
            self.note.text, self.update_form_data['text'], UPDATE_NOTE_TEXT
        )
        self.assertEqual(
            self.note.slug, self.update_form_data['slug'], NOTE_SLUG
        )
        self.assertEqual(
            self.note.author, self.author
        )

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        note = Note.objects.get(slug=NOTE_SLUG)
        self.assertEqual(
            note.title, self.form_data['title'], NOTE_TITLE
        )
        self.assertEqual(
            note.text, self.form_data['text'], NOTE_TEXT
        )
        self.assertEqual(
            note.slug, self.form_data['slug'], NOTE_SLUG
        )
        self.assertEqual(
            note.author, self.author
        )
