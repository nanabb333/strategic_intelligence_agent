import launch


def test_launcher_defaults_to_loopback_only() -> None:
    assert launch.HOST == "127.0.0.1"
