# Smart Task Manager

A lightweight task manager (Flask REST API + vanilla JavaScript/Bootstrap UI) with an end-to-end UI test suite written in **Selenium**. The project focuses on test automation: every user flow in the UI is covered by an automated browser test.

## Features

- Add tasks with a priority (Low / Medium / High)
- Mark tasks as completed, delete tasks
- Filter by all / active / completed, with live counters
- Server-side input validation; user input is HTML-escaped before rendering (XSS-safe)

## Tech Stack

| Part | Technologies |
|---|---|
| Backend | Python, Flask (in-memory store) |
| Frontend | HTML, Bootstrap 5, vanilla JavaScript (Fetch API) |
| Testing | Selenium WebDriver, pytest, webdriver-manager |

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks?status=active\|completed` | List tasks (optional filter) |
| POST | `/api/tasks` | Create: `{ "title", "priority" }` |
| PUT | `/api/tasks/<id>` | Update `title`, `completed`, `priority` |
| DELETE | `/api/tasks/<id>` | Delete |
| POST | `/api/reset` | Clear all tasks (used by the test suite) |

## Automated UI Tests

`selenium-tests/test_ui.py` drives a real Chrome browser against the running app:

| Test | Scenario |
|---|---|
| TC1 `test_page_load` | Page loads and renders the application |
| TC2 `test_add_task_with_priority` | A task is added with the selected priority badge |
| TC3 `test_complete_task` | Checking a task marks it completed and updates the completed counter |
| TC4 `test_filter_completed_tasks` | Completed filter shows only completed tasks |
| TC5 `test_delete_task` | Deleting removes the task from the list |

Each test resets the application state through `/api/reset`, so tests are independent of each other.

## Getting Started

```bash
# 1) Run the app
cd flask-app
pip install -r requirements.txt
python app.py                      # http://127.0.0.1:5000

# 2) In another terminal, run the UI tests (requires Google Chrome)
cd selenium-tests
pip install -r requirements.txt
pytest test_ui.py -v
```

Set `FLASK_DEBUG=1` to enable the Flask debugger during development (disabled by default).
