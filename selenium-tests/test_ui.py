import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# =======================
# CONFIG
# =======================
BASE_URL = "http://127.0.0.1:5000"
STEP_DELAY = 0.8


def pause():
    time.sleep(STEP_DELAY)


# =======================
# DRIVER & RESET
# =======================
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )


def reset_app_state():
    requests.post(f"{BASE_URL}/api/reset")


def wait_task_count(driver, count, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script(
            f"return document.getElementById('total-count').innerText === '{count}';"
        )
    )


# =======================
# 🧪 TC1 – Page Load
# =======================
def test_page_load():
    reset_app_state()
    driver = setup_driver()
    driver.get(BASE_URL)

    pause()
    assert "Smart Task Manager" in driver.page_source

    driver.quit()


# =======================
# 🧪 TC2 – Add Task with Priority
# =======================
def test_add_task_with_priority():
    reset_app_state()
    driver = setup_driver()
    driver.get(BASE_URL)

    pause()
    driver.execute_script("""
        document.getElementById("task-title").value = "Selenium Priority Task";
        document.getElementById("priority-select").value = "High";
        document.getElementById("add-task-btn").click();
    """)

    wait_task_count(driver, 1)
    pause()

    assert driver.execute_script("""
        return document.querySelector("#task-list .task-title")
            .innerText.includes("Selenium Priority Task");
    """)

    assert driver.execute_script("""
        return document.querySelector("#task-list .badge").innerText === "High";
    """)

    driver.quit()


# =======================
# 🧪 TC3 – Complete Task
# =======================
def test_complete_task():
    reset_app_state()
    driver = setup_driver()
    driver.get(BASE_URL)

    pause()
    driver.execute_script("""
        document.getElementById("task-title").value = "Complete Me";
        document.getElementById("add-task-btn").click();
    """)

    wait_task_count(driver, 1)
    pause()

    driver.execute_script("""
        document.querySelector("#task-list input[type='checkbox']").click();
    """)

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return document.getElementById('completed-count').innerText === '1';"
        )
    )

    pause()
    driver.quit()


# =======================
# 🧪 TC4 – Filter Completed Tasks
# =======================
def test_filter_completed_tasks():
    reset_app_state()
    driver = setup_driver()
    driver.get(BASE_URL)

    pause()
    driver.execute_script("""
        document.getElementById("task-title").value = "Filtered Task";
        document.getElementById("add-task-btn").click();
    """)

    wait_task_count(driver, 1)
    pause()

    driver.execute_script("""
        document.querySelector("#task-list input[type='checkbox']").click();
    """)

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return document.getElementById('completed-count').innerText === '1';"
        )
    )

    pause()
    driver.execute_script("""
        document.getElementById("filter-completed").click();
    """)

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return document.querySelectorAll('#task-list li').length === 1;"
        )
    )

    pause()
    driver.quit()


# =======================
# 🧪 TC5 – Delete Task
# =======================
def test_delete_task():
    reset_app_state()
    driver = setup_driver()
    driver.get(BASE_URL)

    pause()
    driver.execute_script("""
        document.getElementById("task-title").value = "Delete Task";
        document.getElementById("add-task-btn").click();
    """)

    wait_task_count(driver, 1)
    pause()

    driver.execute_script("""
        document.querySelector("#task-list .delete-btn").click();
    """)

    wait_task_count(driver, 0)
    pause()

    driver.quit()
