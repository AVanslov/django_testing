from http.client import NOT_FOUND, OK

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
    TestObjects,
)


class TestRoutes(TestObjects):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(
            create_note=True,
        )

    def test_pages_availability(self):
        cases = (
            (HOME_URL, self.client, OK),
            (LOGIN_URL, self.client, OK),
            (LOGOUT_URL, self.client, OK),
            (SIGNUP_URL, self.client, OK),
            (EDIT_URL, self.author, OK),
            (EDIT_URL, self.reader, NOT_FOUND),
            (DELETE_URL, self.author, OK),
            (DELETE_URL, self.reader, NOT_FOUND),
            (DETAIL_URL, self.author, OK),
            (DETAIL_URL, self.reader, NOT_FOUND),
            (ADD_NOTE_URL, self.author, OK),
            (ADD_NOTE_URL, self.reader, OK),
            (SECCESS_CHANGED_NOTE_URL, self.author, OK),
            (SECCESS_CHANGED_NOTE_URL, self.reader, OK),
            (LIST_OF_NOTES_URL, self.author, OK),
            (LIST_OF_NOTES_URL, self.reader, OK),
        )
        for (
            url,
            client,
            expected,
        ) in cases:
            with self.subTest():
                self.assertEqual(
                    client.get(url).status_code,
                    expected,
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
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), redirect_url)
