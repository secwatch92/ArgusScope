# مسیر فایل: tests/unit/test_workspace.py
# این فایل شامل تست‌های واحد برای مدل‌ها، مدیر پایگاه داده و دستورات CLI مربوط به Workspace است.

import pytest
from typer.testing import CliRunner
from pymongo import MongoClient
import os
from typing import Optional, List  # <--- وارد کردن تایپ‌های ضروری

# وارد کردن کلاس‌ها و اپلیکیشن اصلی از پروژه
from argus_scope.core.models import WorkspaceModel, TargetModel, WorkspaceState
from argus_scope.database.db_manager import DatabaseManager
from argus_scope.cli import app


# --- Fixtures: ابزارهای کمکی برای تست‌ها ---

@pytest.fixture(scope="module")
def test_db_manager():
    """
    یک fixture برای ایجاد اتصال به یک دیتابیس تست مجزا
    و پاک‌سازی کامل آن پس از اتمام تمام تست‌های این ماژول.
    این کار تضمین می‌کند که تست‌ها روی دیتابیس اصلی شما اجرا نمی‌شوند.
    """
    # از یک رشته اتصال متفاوت برای دیتابیس تست استفاده می‌کنیم.
    test_mongo_uri = os.getenv("TEST_DATABASE_URL", "mongodb://mongodb:27017/argus_db_test")
    db_manager = DatabaseManager(connection_uri=test_mongo_uri)

    # اطمینان از خالی بودن دیتابیس قبل از شروع تست‌ها
    db_manager.client.drop_database('argus_db_test')

    yield db_manager  # در این نقطه، تست‌ها اجرا می‌شوند

    # پاک‌سازی دیتابیس پس از اتمام تمام تست‌ها
    print("\nCleaning up test database...")
    db_manager.client.drop_database('argus_db_test')
    db_manager.client.close()


@pytest.fixture
def cli_runner():
    """یک fixture برای ایجاد یک نمونه از اجراکننده CLI."""
    return CliRunner()


@pytest.fixture(autouse=True)
def override_db_manager_for_tests(monkeypatch, test_db_manager):
    """
    این fixture به صورت خودکار تابع get_db_manager را در کل پروژه بازنویسی (override) می‌کند.
    این کار تضمین می‌کند که تمام دستورات CLI که در تست‌ها اجرا می‌شوند،
    به جای دیتابیس اصلی، از دیتابیس تست ما استفاده کنند.
    """
    import argus_scope.utils.db
    monkeypatch.setattr(argus_scope.utils.db, 'get_db_manager', lambda: test_db_manager)


# --- کلاس تست‌ها ---

class TestWorkspaceFunctionality:
    """یک کلاس برای گروه‌بندی تمام تست‌های مربوط به Workspace."""

    def test_workspace_model_creation(self):
        """تست ایجاد یک نمونه از WorkspaceModel با مقادیر پیش‌فرض."""
        ws = WorkspaceModel(name="Test-WS-Model")
        assert ws.name == "Test-WS-Model"
        assert ws.state == WorkspaceState.ACTIVE
        assert ws.id is not None
        assert ws.targets == []

    def test_create_and_get_workspace_in_db(self, test_db_manager):
        """تست ایجاد و بازیابی موفقیت‌آمیز یک Workspace در دیتابیس."""
        ws_model = WorkspaceModel(name="DB-Test-WS-1")
        test_db_manager.create_workspace(ws_model)

        retrieved_ws = test_db_manager.get_workspace_by_name("DB-Test-WS-1")

        assert retrieved_ws is not None
        assert retrieved_ws.name == "DB-Test-WS-1"
        assert retrieved_ws.id == ws_model.id

    def test_get_nonexistent_workspace(self, test_db_manager):
        """تست اینکه جستجوی یک Workspace ناموجود نتیجه None برمی‌گرداند."""
        retrieved_ws = test_db_manager.get_workspace_by_name("nonexistent-ws")
        assert retrieved_ws is None

    def test_create_duplicate_workspace_fails_in_db(self, test_db_manager):
        """تست اینکه ایجاد Workspace با نام تکراری باعث خطا می‌شود (به دلیل ایندکس unique)."""
        ws_model = WorkspaceModel(name="DB-Test-WS-Duplicate")
        test_db_manager.create_workspace(ws_model)

        # تلاش برای ایجاد مجدد با همان نام
        duplicate_ws_model = WorkspaceModel(name="DB-Test-WS-Duplicate")

        # ما انتظار داریم که این عملیات به دلیل محدودیت unique در دیتابیس با خطا مواجه شود.
        with pytest.raises(Exception) as excinfo:
            test_db_manager.create_workspace(duplicate_ws_model)

        assert "duplicate key error" in str(excinfo.value).lower()

    def test_cli_workspace_create_success(self, cli_runner):
        """تست ایجاد موفقیت‌آمیز Workspace از طریق CLI."""
        result = cli_runner.invoke(app, [
            "workspace",
            "create",
            "--name", "CLI-WS-Success",
            "--description", "A test workspace from CLI"
        ])

        assert result.exit_code == 0
        assert "✅ Workspace 'CLI-WS-Success' created successfully!" in result.stdout
        assert "Description: A test workspace from CLI" in result.stdout

    def test_cli_workspace_create_duplicate_name(self, cli_runner):
        """تست اینکه ایجاد Workspace با نام تکراری از طریق CLI با خطا مواجه می‌شود."""
        # اولین ایجاد موفقیت‌آمیز است
        cli_runner.invoke(app, ["workspace", "create", "--name", "CLI-WS-Duplicate"])

        # تلاش دوم باید با خطا مواجه شود
        result = cli_runner.invoke(app, ["workspace", "create", "--name", "CLI-WS-Duplicate"])

        assert result.exit_code == 1
        assert "Error: A workspace with the name 'CLI-WS-Duplicate' already exists." in result.stdout
