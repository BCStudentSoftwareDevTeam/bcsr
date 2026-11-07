import pytest

from app.loadConfig import load_config

pytestmark = pytest.mark.unit


def test_default_config_is_not_replaced_by_secret_override(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'app').mkdir()
    (tmp_path / 'app/config.yaml').write_text('source: application\n')
    override = tmp_path / 'test-secret.yaml'
    override.write_text('source: test-secret\n')
    monkeypatch.setenv('BCSR_SECRET_CONFIG', str(override))

    assert load_config() == {'source': 'application'}


def test_explicit_filename_keeps_existing_behavior(tmp_path, monkeypatch):
    config = tmp_path / 'explicit.yaml'
    config.write_text('source: explicit\n')
    monkeypatch.setenv('BCSR_SECRET_CONFIG', str(tmp_path / 'unused.yaml'))

    assert load_config(str(config)) == {'source': 'explicit'}


def test_requested_environment_override_is_used(tmp_path, monkeypatch):
    override = tmp_path / 'test-secret.yaml'
    override.write_text('source: isolated-test\n')
    monkeypatch.setenv('BCSR_SECRET_CONFIG', str(override))

    assert load_config(tmp_path / 'missing.yaml', env_var='BCSR_SECRET_CONFIG') == {
        'source': 'isolated-test'}


def test_unset_override_falls_back_to_filename(tmp_path, monkeypatch):
    config = tmp_path / 'fallback.yaml'
    config.write_text('source: fallback\n')
    monkeypatch.delenv('BCSR_SECRET_CONFIG', raising=False)

    assert load_config(config, env_var='BCSR_SECRET_CONFIG') == {'source': 'fallback'}


def test_missing_override_fails_instead_of_reading_normal_secrets(tmp_path, monkeypatch):
    fallback = tmp_path / 'normal-secret.yaml'
    fallback.write_text('source: normal-secret\n')
    monkeypatch.setenv('BCSR_SECRET_CONFIG', str(tmp_path / 'missing.yaml'))

    with pytest.raises(FileNotFoundError):
        load_config(fallback, env_var='BCSR_SECRET_CONFIG')
