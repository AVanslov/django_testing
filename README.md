# Django testing  
## Languages and tools
![Python](https://img.shields.io/badge/-Python-black?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/-Django-black?style=for-the-badge&logo=Django)

![Pytest](https://img.shields.io/badge/-Pytest-black?style=for-the-badge&logo=pytest)
![Unittest](https://img.shields.io/badge/-Unittest-black?style=for-the-badge&logo=unittest)
## About the project

- The main page of the project displays the 10 latest news. The main page is accessible to any user. The news is displayed in an abbreviated form (only the first 15 words are visible).
- Each news has its own page, with the full text of the news; user comments are also displayed there.
- Any user can register on the site independently.
- Logged in (authorized) user can leave comments, edit and delete their comments.
- If there are comments on the news, their number is displayed on the main page under the news.
- There is a list of forbidden words in the project code that cannot be used in comments, for example, "radish" and "scoundrel".

## What are the tests written for?
This project, or rather two projects, were created primarily for training in writing tests, so in each application you can see tests on pytest and on unittest.

### Unittest tests for the YaNote project

**In the file test_routes.py :**
- The main page is accessible to an anonymous user.
- An authenticated user can access the page with a list of notes/, the page for successfully adding a note done/, the page for adding a new note add/.
- The pages of a separate note, deletion and editing of a note are available only to the author of the note. If another user tries to access these pages, error 404 will be returned.
— When trying to go to the page of the list of notes, the page of successfully adding an entry, the page of adding a note, a separate note, editing or deleting a note, the anonymous user is redirected to the login page.
- The user registration, account login and logout pages are available to all users.

**In the file test_content.py :**
- a separate note is passed to a page with a list of notes in the object_list list in the context dictionary;
- the notes of one user are not included in the list of notes of another user;
- forms are sent to the pages for creating and editing notes.

**In the file test_logic.py:**
- A logged—in user can create a note, but an anonymous user cannot.
- It is not possible to create two notes with the same slug.
- If the slug is not filled in when creating a note, then it is generated automatically using the pytils.translate.slugify function.
- The user can edit and delete their own notes, but cannot edit or delete someone else's.

### Pytest tests for the YaNews project.

**In the file test_routes.py :**
- The main page is accessible to an anonymous user.
- A separate news page is available to an anonymous user.
- The comment deletion and editing pages are available to the comment author.
- When trying to go to the edit or delete comment page, an anonymous user is redirected to the authorization page.
- An authorized user cannot access the pages for editing or deleting other people's comments (error 404 is returned).
- The user registration, account login and logout pages are available to anonymous users.

**In the file test_content.py:**
- The number of news on the main page is no more than 10.
- The news is sorted from the most recent to the oldest. The latest news is at the top of the list.
- Comments on a separate news page are sorted chronologically: old at the beginning of the list, new at the end.
- The form for sending a comment on a separate news page is not available to an anonymous user, but it is available to an authorized user.

**In the file test_logic.py:**
- An anonymous user cannot send a comment.
- An authorized user can send a comment.
- If a comment contains forbidden words, it will not be published, and the form will return an error.
- An authorized user can edit or delete their comments.
- An authorized user cannot edit or delete other people's comments.

## О проекте

- На главной странице проекта отображаются 10 последних новостей. Главная страница доступна любому пользователю. Новости отображаются в сокращённом виде (видно только первые 15 слов).
- У каждой новости есть своя страница, с полным текстом новости; там же отображаются и комментарии пользователей.
- Любой пользователь может самостоятельно зарегистрироваться на сайте.
- Залогиненный (авторизованный) пользователь может оставлять комментарии, редактировать и удалять свои комментарии.
- Если к новости есть комментарии — их количество отображается на главной странице под новостью.
- В коде проекта есть список запрещённых слов, которые нельзя использовать в комментариях, например, «редиска» и «негодяй».

## Для чего написаны тесты
Данный проект, точнее два проекта, созданы прежде всего для тренировки в написании тестов, поэтому в каждой приложении можно увидеть тесты на pytest и на unittest.

### Тесты на unittest для проекта YaNote

**В файле test_routes.py:**
- Главная страница доступна анонимному пользователю.
- Аутентифицированному пользователю доступна страница со списком заметок notes/, страница успешного добавления заметки done/, страница добавления новой заметки add/.
- Страницы отдельной заметки, удаления и редактирования заметки доступны только автору заметки. Если на эти страницы попытается зайти другой пользователь — вернётся ошибка 404.
- При попытке перейти на страницу списка заметок, страницу успешного добавления записи, страницу добавления заметки, отдельной заметки, редактирования или удаления заметки анонимный пользователь перенаправляется на страницу логина.
- Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям.

**В файле test_content.py:**
- отдельная заметка передаётся на страницу со списком заметок в списке object_list в словаре context;
- в список заметок одного пользователя не попадают заметки другого пользователя;
- на страницы создания и редактирования заметки передаются формы.

**В файле test_logic.py:**
- Залогиненный пользователь может создать заметку, а анонимный — не может.
- Невозможно создать две заметки с одинаковым slug.
- Если при создании заметки не заполнен slug, то он формируется автоматически, с помощью функции pytils.translit.slugify.
- Пользователь может редактировать и удалять свои заметки, но не может редактировать или удалять чужие.

### Тесты на pytest для проекта YaNews.

**В файле test_routes.py:**
- Главная страница доступна анонимному пользователю.
- Страница отдельной новости доступна анонимному пользователю.
- Страницы удаления и редактирования комментария доступны автору комментария.
- При попытке перейти на страницу редактирования или удаления комментария анонимный пользователь перенаправляется на страницу авторизации.
- Авторизованный пользователь не может зайти на страницы редактирования или удаления чужих комментариев (возвращается ошибка 404).
- Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны анонимным пользователям.

**В файле test_content.py:**
- Количество новостей на главной странице — не более 10.
- Новости отсортированы от самой свежей к самой старой. Свежие новости в начале списка.
- Комментарии на странице отдельной новости отсортированы в хронологическом порядке: старые в начале списка, новые — в конце.
- Анонимному пользователю недоступна форма для отправки комментария на странице отдельной новости, а авторизованному доступна.

**В файле test_logic.py:**
- Анонимный пользователь не может отправить комментарий.
- Авторизованный пользователь может отправить комментарий.
- Если комментарий содержит запрещённые слова, он не будет опубликован, а форма вернёт ошибку.
- Авторизованный пользователь может редактировать или удалять свои комментарии.
- Авторизованный пользователь не может редактировать или удалять чужие комментарии.
