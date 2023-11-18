from django.urls import reverse
from notes.forms import NoteForm

from notes.models import Note
from notes.tests.constants import CreateTestObjects
from notes.tests.constants import LIST_OF_NOTES_URL


class TestDetailPage(CreateTestObjects):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(
            create_note=True,
        )

    def test_visibility_note_on_list_page(self):
        response = self.author_client.get(LIST_OF_NOTES_URL)
        self.assertIn(self.note, response.context['object_list'])
        notes = Note.objects.get()
        self.assertEqual(notes.title, self.note.title)
        self.assertEqual(notes.text, self.note.text)
        self.assertEqual(notes.slug, self.note.slug)
        self.assertEqual(notes.author, self.note.author)

    def test_visibility_notes_other_author(self):
        response = self.reader_client.get(LIST_OF_NOTES_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_authorized_client_has_form_on_add_and_edit_pages(self):
        urls = (
            ('notes:edit', (self.note.slug,)),
            ('notes:add', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                self.assertIn(
                    isinstance('form', NoteForm),
                    self.author_client.get(url).context
                )
