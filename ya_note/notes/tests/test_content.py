from notes.forms import NoteForm
from notes.tests.constants_and_main_class import (
    ADD_NOTE_URL, EDIT_URL, CreateTestObjects
)
from notes.tests.constants_and_main_class import LIST_OF_NOTES_URL


class TestDetailPage(CreateTestObjects):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(
            create_note=True,
        )

    def test_visibility_note_on_list_page(self):
        response = self.author_client.get(LIST_OF_NOTES_URL)
        self.assertIn(self.note, response.context['object_list'])
        notes = response.context['object_list']
        self.assertEqual(notes[0].title, self.note.title)
        self.assertEqual(notes[0].text, self.note.text)
        self.assertEqual(notes[0].slug, self.note.slug)
        self.assertEqual(notes[0].author, self.note.author)

    def test_visibility_notes_other_author(self):
        self.assertNotIn(
            self.note, self.reader_client.get(
                LIST_OF_NOTES_URL
            ).context['object_list']
        )

    def test_authorized_client_has_form_on_add_and_edit_pages(self):
        urls = (
            EDIT_URL,
            ADD_NOTE_URL,
        )
        for url in urls:
            with self.subTest(name=url):
                self.assertIn(
                    'form',
                    self.author_client.get(url).context
                )
                self.assertIsInstance(
                    self.author_client.get(url).context['form'],
                    NoteForm
                )
