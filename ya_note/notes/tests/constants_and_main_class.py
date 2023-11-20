from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

NOTE_TITLE = 'Бухтелка'
NOTE_TEXT = (
    'Трам-Па-Па-Пам-Тарам-Пам-Пам'
)
UPDATE_NOTE_TEXT = (
    'Пара-ра-ра-ра-рам. Пуру-ру-ру-рум.'
)
NOTE_SLUG = 'buhtelka'

FIRST_NOTE_TITLE = 'План похода к Тигруле'
FIRST_NOTE_TEXT = (
    'Прихвачу санки'
)
FIRST_NOTE_SLUG = 'plan-pohoda-k-tigrule'

SECOND_NOTE_TITLE = 'План похода к Кролику'
SECOND_NOTE_TEXT = (
    'Прихвачу корзину для сбора морковки'
)
SECOND_NOTE_SLUG = 'plan-pohoda-k-kroliku'

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

REDIRECT_AFTER_TRY_ADD_NOTE_URL = (
    f'{LOGIN_URL}?next={ADD_NOTE_URL}'
)
REDIRECT_AFTER_TRY_SECCESS_CHANGED_NOTE_URL = (
    f'{LOGIN_URL}?next={SECCESS_CHANGED_NOTE_URL}'
)
REDIRECT_AFTER_LIST_OF_NOTES_URL = (
    f'{LOGIN_URL}?next={LIST_OF_NOTES_URL}'
)
REDIRECT_AFTER_TRY_EDIT_URL = (
    f'{LOGIN_URL}?next={EDIT_URL}'
)
REDIRECT_AFTER_TRY_DELETE_URL = (
    f'{LOGIN_URL}?next={DELETE_URL}'
)
REDIRECT_AFTER_TRY_DETAIL_URL = (
    f'{LOGIN_URL}?next={DETAIL_URL}'
)

User = get_user_model()


class CreateTestObjects(TestCase):
    @classmethod
    def setUpTestData(
        cls,
        create_reader=True,
        create_note=False,
        enter_data_into_note_form=False,
        enter_first_data_into_note_form=False,
        enter_second_data_into_note_form=False,
        update_data_in_note_form=False,
    ):
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
        if enter_first_data_into_note_form:
            cls.first_form_data = {
                'title': FIRST_NOTE_TITLE,
                'text': FIRST_NOTE_TEXT,
                'slug': FIRST_NOTE_SLUG,
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
