from common.paths import LOG_DIR, OUTPUTS_DIR, ROOT_DIR


def test_paths_exist():
    assert ROOT_DIR.exists()
    assert LOG_DIR.exists()
    assert OUTPUTS_DIR.exists()
