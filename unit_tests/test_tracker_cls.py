from tracker_cls import Tracker
import pytest

def test_activity_setter_and_getter():
    tracker = Tracker("Study")
    assert tracker.activity == "study"

    with pytest.raises(ValueError):
        tracker3 = Tracker("")
