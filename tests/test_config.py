from src.config import load_config

def test_config_loads():
    config = load_config()
    assert config is not None

def test_config_has_sources():
    config = load_config()
    assert 'sources' in config

def test_config_source_has_path():
    config = load_config()
    assert 'path' in config['sources'][0]

def test_config_source_has_table():
    config = load_config()
    assert 'target_table' in config['sources'][0]