from notes.forms import NoteForm
from notes.models import Note
from notes.tests.constants_and_main_class import (
    ADD_NOTE_URL, EDIT_URL, TestObjects
)
from notes.tests.constants_and_main_class import LIST_OF_NOTES_URL


class TestDetailPage(TestObjects):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(
            create_note=True,
        )

    def test_visibility_note_on_list_page(self):
        notes = self.author.get(
            LIST_OF_NOTES_URL
        ).context['object_list']
        self.assertIn(self.note, notes)
        self.assertEqual(len(notes), Note.objects.count())
        self.assertEqual(
            len(
                set(notes).intersection(
                    set(Note.objects.all().filter(id=self.note.id))
                )
            ), 1
        )
        note = notes.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_visibility_notes_other_author(self):
        self.assertNotIn(
            self.note, self.reader.get(
                LIST_OF_NOTES_URL
            ).context['object_list']
        )

    def test_authorized_client_has_form_on_add_and_edit_pages(self):
        urls = (
            EDIT_URL,
            ADD_NOTE_URL,
        )
        for url in urls:
            request = self.author.get(url)
            with self.subTest(url=url):
                self.assertIn(
                    'form',
                    request.context
                )
                self.assertIsInstance(
                    request.context['form'],
                    NoteForm
                )
