from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from pytils.translit import slugify

from notes.models import Note

NOTE_TITLE = 'Бухтелка'
NOTE_TEXT = (
    'Трам-Па-Па-Пам-Тарам-Пам-Пам'
)
UPDATE_NOTE_TEXT = (
    'Пара-ра-ра-ра-рам. Пуру-ру-ру-рум.'
)
NOTE_SLUG = slugify(NOTE_TITLE)

SECOND_NOTE_TITLE = 'План похода к Кролику'
SECOND_NOTE_TEXT = (
    'Прихвачу корзину для сбора морковки'
)
SECOND_NOTE_SLUG = slugify(SECOND_NOTE_TITLE)

HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
LIST_OF_NOTES_URL = reverse('notes:list')
ADD_NOTE_URL = reverse('notes:add')
SECCESS_CHANGED_NOTE_URL = reverse('notes:success')
EDIT_URL = reverse('notes:edit', args=(NOTE_SLUG,))
DELETE_URL = reverse('notes:delete', args=(NOTE_SLUG,))
DETAIL_URL = reverse('notes:detail', args=(NOTE_SLUG,))

User = get_user_model()


class CreateTestObjects(TestCase):
    @classmethod
    def setUpTestData(
        cls,
        create_author=True,
        create_reader=True,
        create_note=False,
        enter_data_into_note_form=False,
        enter_second_data_into_note_form=False,
        update_data_in_note_form=False,
    ):
        cls.url_add = ADD_NOTE_URL
        cls.url_list = LIST_OF_NOTES_URL
        cls.url_success = SECCESS_CHANGED_NOTE_URL
        cls.edit_url = EDIT_URL
        cls.delete_url = DELETE_URL

        if create_author:
            cls.author = User.objects.create(username='Винни Пух')
            cls.author_client = Client()
            cls.author_client.force_login(cls.author)
        if create_reader:
            cls.reader = User.objects.create(username='Пятачок')
            cls.reader_client = Client()
            cls.reader_client.force_login(cls.reader)
        if create_note:
            cls.note = Note.objects.create(
                title=NOTE_TITLE,
                text=NOTE_TEXT,
                author=cls.author,
            )
        if enter_data_into_note_form:
            cls.form_data = {
                'title': NOTE_TITLE,
                'text': NOTE_TEXT,
                'slug': NOTE_SLUG,
            }
        if enter_second_data_into_note_form:
            cls.second_form_data = {
                'title': SECOND_NOTE_TITLE,
                'text': SECOND_NOTE_TEXT,
                'slug': SECOND_NOTE_SLUG,
            }
        if update_data_in_note_form:
            cls.update_form_data = {
                'title': NOTE_TITLE,
                'text': UPDATE_NOTE_TEXT,
                'slug': NOTE_SLUG,
            }
