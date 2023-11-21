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
    TestObjects,
)


class TestNoteCreateEdit(TestObjects):

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

    def create_one_note(self, form_data, slug):
        notes = set(Note.objects.all())
        response = self.author.post(
            ADD_NOTE_URL, data=form_data,
        )
        self.assertRedirects(response, SECCESS_CHANGED_NOTE_URL)
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.title, form_data['title'])
        self.assertEqual(note.text, form_data['text'])
        self.assertEqual(note.slug, slug)
        self.assertEqual(note.author, self.auth)

    def test_user_can_create_note(self):
        self.create_one_note(
            form_data=self.second_form_data,
            slug=self.second_form_data['slug']
        )

    def test_user_cant_use_used_slug(self):
        notes_in_db_befor_try_to_change = Note.objects.all()
        response = self.author.post(ADD_NOTE_URL, data=self.form_data)
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
        self.create_one_note(
            form_data=self.second_form_data,
            slug=slugify(self.second_form_data['title']),
        )

    def test_author_can_delete_note(self):
        response = self.author.delete(DELETE_URL)
        self.assertRedirects(response, SECCESS_CHANGED_NOTE_URL)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_user_cant_delete_note_of_another_user(self):
        notes_in_db_befor_try_to_change = Note.objects.all()
        response = self.reader.delete(DELETE_URL)
        notes_in_db_after_try_to_change = Note.objects.all()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertQuerysetEqual(
            notes_in_db_befor_try_to_change,
            notes_in_db_after_try_to_change,
        )

    def test_author_can_edit_note(self):
        response = self.author.post(
            EDIT_URL, data=self.update_form_data
        )
        self.assertRedirects(response, SECCESS_CHANGED_NOTE_URL)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(
            note.title, self.update_form_data['title'],
        )
        self.assertEqual(
            note.text, self.update_form_data['text'],
        )
        self.assertEqual(
            note.slug, self.update_form_data['slug'],
        )
        self.assertEqual(
            note.author, self.note.author
        )

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader.post(
            EDIT_URL,
            data=self.update_form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(
            self.note,
            note,
        )
        self.assertEqual(
            self.note.title, note.title,
        )
        self.assertEqual(
            self.note.text, note.text,
        )
        self.assertEqual(
            self.note.slug, note.slug,
        )
