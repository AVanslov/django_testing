from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.tests.constants import (
    ADD_NOTE_URL,
    DELETE_URL,
    DETAIL_URL,
    EDIT_URL,
    HOME_URL,
    LIST_OF_NOTES_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SECCESS_CHANGED_NOTE_URL,
    SIGNUP_URL,
    CreateTestObjects,
)

User = get_user_model()


class TestRoutes(CreateTestObjects):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(
            create_note=True,
        )

    def test_pages_availability(self):
        variations_of_access_checks = (
            (HOME_URL, self.client, HTTPStatus.OK),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (LOGOUT_URL, self.client, HTTPStatus.OK),
            (SIGNUP_URL, self.client, HTTPStatus.OK),
            (EDIT_URL, self.author_client, HTTPStatus.OK),
            (EDIT_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (DELETE_URL, self.author_client, HTTPStatus.OK),
            (DELETE_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (DETAIL_URL, self.author_client, HTTPStatus.OK),
            (DETAIL_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (ADD_NOTE_URL, self.author_client, HTTPStatus.OK),
            (ADD_NOTE_URL, self.reader_client, HTTPStatus.OK),
            (SECCESS_CHANGED_NOTE_URL, self.author_client, HTTPStatus.OK),
            (SECCESS_CHANGED_NOTE_URL, self.reader_client, HTTPStatus.OK),
            (LIST_OF_NOTES_URL, self.author_client, HTTPStatus.OK),
            (LIST_OF_NOTES_URL, self.reader_client, HTTPStatus.OK),
        )
        for (
            url,
            parametrized_client,
            expected_status,
        ) in variations_of_access_checks:
            self.assertEqual(
                parametrized_client.get(url).status_code, expected_status
            )

    def test_redirect_for_anonymous_client(self):
        for url in (
            ADD_NOTE_URL,
            SECCESS_CHANGED_NOTE_URL,
            LIST_OF_NOTES_URL,
            EDIT_URL,
            DELETE_URL,
            DETAIL_URL,
        ):
            with self.subTest(name=url):
                redirect_url = f'{LOGIN_URL}?next={url}'
                self.assertRedirects(self.client.get(url), redirect_url)
