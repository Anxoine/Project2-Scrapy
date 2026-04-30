import sys
import os
import subprocess
from pathlib import Path
import pytest


@pytest.fixture
def mock_scrapy_project(tmp_path):
    """
    Sets up a temporary Scrapy project structure with a custom Add-on.
    """
    project_root = tmp_path / "testproject"
    project_root.mkdir()
    (project_root / "__init__.py").write_text("", encoding="utf-8")

    # 1. Create a mock Add-on that injects settings
    addon_file_content = """
class PluginAddon:
    def update_settings(self, settings):
        settings.set("ADDON_DEBUG_KEY", "addon_active", priority="addon")
        settings.set("ADDON_BOOL_KEY", True, priority="addon")
"""
    (project_root / "my_addon.py").write_text(addon_file_content, encoding="utf-8")

    # 2. Configure the project settings to use the Add-on
    settings_file_content = """
BOT_NAME = 'testproject'
ADDONS = {'testproject.my_addon.PluginAddon': 100}
"""
    (project_root / "settings.py").write_text(settings_file_content, encoding="utf-8")

    # 3. Create a standard scrapy.cfg file
    config_file_content = "[settings]\ndefault = testproject.settings\n"
    (tmp_path / "scrapy.cfg").write_text(config_file_content, encoding="utf-8")

    return tmp_path


def execute_scrapy_settings_command(working_directory, *cli_arguments):
    """
    Helper to execute 'scrapy settings' in a subprocess with the correct PYTHONPATH.
    """
    execution_env = os.environ.copy()

    # Ensure the local Scrapy source code is prioritized in the environment
    scrapy_source_root = str(Path(__file__).resolve().parents[1])
    execution_env["PYTHONPATH"] = os.pathsep.join([str(working_directory), scrapy_source_root])

    full_command = [sys.executable, "-m", "scrapy.cmdline", "settings"] + list(cli_arguments)

    process_result = subprocess.run(
        full_command,
        cwd=working_directory,
        env=execution_env,
        capture_output=True,
        text=True,
        check=True
    )
    return process_result.stdout.strip()


@pytest.mark.parametrize("command_flag, settings_key, expected_output", [
    ("--get", "ADDON_DEBUG_KEY", "addon_active"),
    ("--getbool", "ADDON_BOOL_KEY", "True"),
    ("--get", "BOT_NAME", "testproject"),
])
def test_settings_command_reflects_addon_updates(mock_scrapy_project, command_flag, settings_key, expected_output):
    actual_output = execute_scrapy_settings_command(mock_scrapy_project, command_flag, settings_key)
    assert actual_output == expected_output