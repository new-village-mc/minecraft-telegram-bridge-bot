import pathlib

import pytest
import yaml

TEST_CONFIG_DATA_PATH = pathlib.Path(__file__).with_name('test_data')


@pytest.fixture
def config():
    test_config = yaml.load(
        (TEST_CONFIG_DATA_PATH.parent.parent.parent / 'invoke.yaml').read_text(encoding='utf-8'),
        Loader=yaml.FullLoader
    )
    return test_config


@pytest.fixture
def logs():
    test_logs = yaml.load(
        (TEST_CONFIG_DATA_PATH / 'logs.yaml').read_text(encoding='utf-8'),
        Loader=yaml.FullLoader
    )
    return test_logs


@pytest.fixture
def issue():
    exporters_config = yaml.load(
        (TEST_CONFIG_DATA_PATH / 'issue.yaml').read_text(encoding='utf-8')
    )
    return exporters_config


@pytest.fixture
def test_grafana_client(test_client):
    pass


@pytest.fixture
def app(config):
    from bot.app import App
    return App(config)


@pytest.fixture
def loop():
    import asyncio
    return asyncio.get_event_loop()
