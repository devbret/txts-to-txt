from pathlib import Path

import pytest

import app


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    return input_dir


def output_text(input_dir: Path) -> str:
    return (input_dir.parent / app.OUTPUT_FILENAME).read_text(encoding="utf-8")


def test_combines_files_in_sorted_order(workspace):
    (workspace / "b.txt").write_text("second\n", encoding="utf-8")
    (workspace / "a.txt").write_text("first\n", encoding="utf-8")

    result = app.combine_txt_files(workspace)

    assert result.succeeded
    assert result.processed == 2
    assert result.read_errors == 0
    assert output_text(workspace) == ("--- a.txt ---\nfirst\n--- b.txt ---\nsecond\n")


def test_extension_check_is_case_insensitive(workspace):
    (workspace / "UPPER.TXT").write_text("shouting\n", encoding="utf-8")

    assert app.combine_txt_files(workspace).succeeded
    assert "shouting" in output_text(workspace)


def test_missing_trailing_newline_does_not_glue_files(workspace):
    (workspace / "a.txt").write_text("no newline", encoding="utf-8")
    (workspace / "b.txt").write_text("next\n", encoding="utf-8")

    assert app.combine_txt_files(workspace).succeeded
    assert output_text(workspace) == ("--- a.txt ---\nno newline\n--- b.txt ---\nnext\n")


def test_skips_non_txt_files_and_directories(workspace):
    (workspace / "notes.md").write_text("markdown\n", encoding="utf-8")
    (workspace / "folder.txt").mkdir()
    (workspace / "real.txt").write_text("kept\n", encoding="utf-8")

    result = app.combine_txt_files(workspace)

    assert result.succeeded
    assert result.processed == 1
    assert output_text(workspace) == "--- real.txt ---\nkept\n"


def test_skips_existing_output_file(workspace):
    (workspace / app.OUTPUT_FILENAME).write_text("old run\n", encoding="utf-8")
    (workspace / "a.txt").write_text("fresh\n", encoding="utf-8")

    assert app.combine_txt_files(workspace).succeeded
    assert output_text(workspace) == "--- a.txt ---\nfresh\n"


def test_non_utf8_file_is_counted_as_read_error(workspace):
    (workspace / "bad.txt").write_bytes(b"\xff\xfe\x00 not utf-8")
    (workspace / "good.txt").write_text("ok\n", encoding="utf-8")

    result = app.combine_txt_files(workspace)

    assert result.succeeded
    assert result.processed == 1
    assert result.read_errors == 1
    assert output_text(workspace) == "--- good.txt ---\nok\n"


def test_empty_directory_writes_empty_output(workspace):
    result = app.combine_txt_files(workspace)

    assert result.succeeded
    assert result.processed == 0
    assert output_text(workspace) == ""


def test_missing_directory_reports_failure(workspace):
    assert not app.combine_txt_files(workspace / "does-not-exist").succeeded


def test_main_returns_ok_on_clean_run(workspace):
    (workspace / "good.txt").write_text("ok\n", encoding="utf-8")

    assert app.main() == app.EXIT_OK


def test_main_returns_partial_when_a_file_cannot_be_read(workspace):
    (workspace / "good.txt").write_text("ok\n", encoding="utf-8")
    (workspace / "bad.txt").write_bytes(b"\xff\xfe\x00 not utf-8")

    assert app.main() == app.EXIT_PARTIAL


def test_main_returns_failure_when_input_directory_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert app.main() == app.EXIT_FAILURE


class _FailingHandle:
    def __init__(self, handle, writes_allowed: int):
        self._handle = handle
        self._writes_allowed = writes_allowed

    def write(self, text: str) -> int:
        if self._writes_allowed <= 0:
            raise OSError("No space left on device")
        self._writes_allowed -= 1
        return self._handle.write(text)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return self._handle.__exit__(*exc_info)


def temp_files(directory: Path) -> list[Path]:
    return list(directory.glob(f".{app.OUTPUT_FILENAME}.*.tmp"))


def test_write_failure_leaves_previous_output_intact(workspace, monkeypatch):
    output_path = workspace.parent / app.OUTPUT_FILENAME
    output_path.write_text("previous run\n", encoding="utf-8")
    (workspace / "a.txt").write_text("first\n", encoding="utf-8")
    (workspace / "b.txt").write_text("second\n", encoding="utf-8")

    real_open = open

    def failing_open(*args, **kwargs):
        handle = real_open(*args, **kwargs)
        if isinstance(args[0], int):
            return _FailingHandle(handle, writes_allowed=3)
        return handle

    monkeypatch.setattr("builtins.open", failing_open)

    result = app.combine_txt_files(workspace)

    assert not result.succeeded
    assert output_path.read_text(encoding="utf-8") == "previous run\n"
    assert temp_files(workspace.parent) == []


def test_rename_failure_leaves_previous_output_intact(workspace, monkeypatch):
    output_path = workspace.parent / app.OUTPUT_FILENAME
    output_path.write_text("previous run\n", encoding="utf-8")
    (workspace / "a.txt").write_text("first\n", encoding="utf-8")

    def failing_replace(*args, **kwargs):
        raise OSError("Cross-device link")

    monkeypatch.setattr(app.os, "replace", failing_replace)

    assert not app.combine_txt_files(workspace).succeeded
    assert output_path.read_text(encoding="utf-8") == "previous run\n"
    assert temp_files(workspace.parent) == []


def test_successful_run_leaves_no_temp_files(workspace):
    (workspace / "a.txt").write_text("first\n", encoding="utf-8")

    assert app.combine_txt_files(workspace).succeeded
    assert output_text(workspace) == "--- a.txt ---\nfirst\n"
    assert temp_files(workspace.parent) == []


def test_output_is_readable_after_atomic_replace(workspace):
    (workspace / "a.txt").write_text("first\n", encoding="utf-8")

    app.combine_txt_files(workspace)

    mode = (workspace.parent / app.OUTPUT_FILENAME).stat().st_mode & 0o777
    assert mode & 0o400
