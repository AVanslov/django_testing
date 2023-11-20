from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.constants_and_main_class import (
    ADD_NOTE_URL,
    DELETE_URL,
    EDIT_URL,
    NOTE_SLUG,
    SECCESS_CHANGED_NOTE_URL,
    UPDATE_NOTE_TEXT,
    CreateTestObjects,
)


class TestNoteCreateEdit(CreateTestObjects):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(
            create_note=True,
            enter_data_into_note_form=True,
            enter_first_data_into_note_form=True,
            enter_second_data_into_note_form=True,
            update_data_in_note_form=True,
        )

    def test_anonymous_user_cant_create_notes(self):
        notes_in_db_befor_try_to_change = Note.objects.all()
        self.client.post(ADD_NOTE_URL, data=self.form_data)
        notes_in_db_after_try_to_change = Note.objects.all()
        self.assertQuerysetEqual(
            notes_in_db_befor_try_to_change,
            notes_in_db_after_try_to_change,
        )

    def test_user_can_create_note(self):
        notes_befor = set(Note.objects.all())
        response = self.author_client.post(
            ADD_NOTE_URL, data=self.second_form_data
        )
        self.assertRedirects(response, SECCESS_CHANGED_NOTE_URL)
        notes_after = set(Note.objects.all())
        created_notes = notes_after.difference(
            notes_befor
        )
        self.assertEqual(len(created_notes), 1)
        note = created_notes.pop()
        self.assertEqual(
            note.title, self.second_form_data['title']
        )
        self.assertEqual(
            note.text, self.second_form_data['text']
        )
        self.assertEqual(
            note.slug, self.second_form_data['slug']
        )
        self.assertEqual(
            note.author, self.author
        )

    def test_user_cant_use_used_slug(self):
        notes_in_db_befor_try_to_change = Note.objects.all()
        response = self.author_client.post(ADD_NOTE_URL, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=Note.objects.get(slug=NOTE_SLUG).slug + WARNING
        )
        notes_in_db_after_try_to_change = Note.objects.all()
        self.assertQuerysetEqual(
            notes_in_db_befor_try_to_change,
            notes_in_db_after_try_to_change,
        )

    def test_slug_is_translit_title(self):
        notes_befor = set(Note.objects.all())
        response = self.author_client.post(
            ADD_NOTE_URL,
            data=self.first_form_data,
        )
        self.assertRedirects(response, SECCESS_CHANGED_NOTE_URL)
        notes_after = set(Note.objects.all())
        created_notes = notes_after.difference(
            notes_befor
        )
        self.assertEqual(len(created_notes), 1)
        note = created_notes.pop()
        self.assertEqual(note.slug, slugify(note.title))
        self.assertEqual(
            note.title, self.first_form_data['title']
        )
        self.assertEqual(
            note.text, self.first_form_data['text']
        )
        self.assertEqual(
            note.author, self.author
        )

    def test_author_can_delete_note(self):
        notes_befor = set(Note.objects.all())
        response = self.author_client.delete(DELETE_URL)
        self.assertRedirects(response, SECCESS_CHANGED_NOTE_URL)
        notes_after = set(Note.objects.all())
        created_notes = notes_after.difference(
            notes_befor
        )
        self.assertEqual(len(created_notes), 0)

    def test_user_cant_delete_note_of_another_user(self):
        notes_in_db_befor_try_to_change = Note.objects.all()
        response = self.reader_client.delete(DELETE_URL)
        notes_in_db_after_try_to_change = Note.objects.all()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertQuerysetEqual(
            notes_in_db_befor_try_to_change,
            notes_in_db_after_try_to_change,
        )

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            EDIT_URL, data=self.update_form_data
        )
        self.assertRedirects(response, SECCESS_CHANGED_NOTE_URL)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, UPDATE_NOTE_TEXT)
        self.assertEqual(
            self.note.title, self.update_form_data['title'],
        )
        self.assertEqual(
            self.note.text, self.update_form_data['text'],
        )
        self.assertEqual(
            self.note.slug, self.update_form_data['slug'],
        )
        self.assertEqual(
            self.note.author, self.note.author
        )

    def test_user_cant_edit_note_of_another_user(self):
        notes_befor = set(Note.objects.all())
        response = self.reader_client.post(
            EDIT_URL,
            data=self.update_form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        notes_after = set(Note.objects.all())

        created_notes = notes_after.intersection(
            notes_befor
        )
        note = created_notes.pop()
        self.assertEqual(
            note.title, self.form_data['title'],
        )
        self.assertEqual(
            note.text, self.form_data['text'],
        )
        self.assertEqual(
            note.slug, self.form_data['slug'],
        )
        self.assertEqual(
            note.author, self.note.author
        )
