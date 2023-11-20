from http import HTTPStatus

from notes.tests.constants_and_main_class import (
    ADD_NOTE_URL,
    DELETE_URL,
    DETAIL_URL,
    EDIT_URL,
    HOME_URL,
    LIST_OF_NOTES_URL,
    LOGIN_URL,
    LOGOUT_URL,
    REDIRECT_AFTER_LIST_OF_NOTES_URL,
    REDIRECT_AFTER_TRY_ADD_NOTE_URL,
    REDIRECT_AFTER_TRY_DELETE_URL,
    REDIRECT_AFTER_TRY_DETAIL_URL,
    REDIRECT_AFTER_TRY_EDIT_URL,
    REDIRECT_AFTER_TRY_SECCESS_CHANGED_NOTE_URL,
    SECCESS_CHANGED_NOTE_URL,
    SIGNUP_URL,
    CreateTestObjects,
)


class TestRoutes(CreateTestObjects):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(
            create_note=True,
        )

    def test_pages_availability(self):
        cases = (
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
        ) in cases:
            self.assertEqual(
                parametrized_client.get(url).status_code, expected_status
            )

    def test_redirect_for_anonymous_client(self):
        for url, redirect_url in (
            (
                ADD_NOTE_URL,
                REDIRECT_AFTER_TRY_ADD_NOTE_URL,
            ),
            (
                SECCESS_CHANGED_NOTE_URL,
                REDIRECT_AFTER_TRY_SECCESS_CHANGED_NOTE_URL,
            ),
            (
                LIST_OF_NOTES_URL,
                REDIRECT_AFTER_LIST_OF_NOTES_URL,
            ),
            (
                EDIT_URL,
                REDIRECT_AFTER_TRY_EDIT_URL,
            ),
            (
                DELETE_URL,
                REDIRECT_AFTER_TRY_DELETE_URL,
            ),
            (
                DETAIL_URL,
                REDIRECT_AFTER_TRY_DETAIL_URL,
            ),
        ):
            with self.subTest(name=url):
                self.assertRedirects(self.client.get(url), redirect_url)
