from tracker_cls import Tracker, TrackingMode
from datetime import date
import pytest
import tempfile
from unittest.mock import patch
import os
import csv

def test_activity_setter_and_getter():
    tracker = Tracker("Study")
    assert tracker.activity == "study"

    with pytest.raises(ValueError):
        tracker3 = Tracker("")


def test_read_from_memory():

    ### Test Case 1: File doesn't exist
    activity_name = "test"
    test_file_path = f"unit_tests/fixtures/{activity_name}"
    with patch.object(Tracker, "file_path", test_file_path):
        tracker1 = Tracker(activity_name)
        tracker1.read_from_memory()
        assert os.path.isfile(test_file_path) == True
        os.remove(test_file_path)

    ### Test Case 2: File exists
    activity_name_2 = "prewritten_data"
    test_path_2 = f"unit_tests/fixtures/{activity_name_2}.csv"

    # Arrange
    expected_data = []
    with open (test_path_2, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            day = date.fromisoformat(row["date"])
            start = int(row["start"])
            end = int(row["end"])
            expected_data.append({"date": day, "start": start, "end": end})

    with patch.object(Tracker, "file_path", test_path_2):
        tracker2 = Tracker(activity_name_2)

        # Act
        data = tracker2.read_from_memory()

        # Assert
        assert data == expected_data

def test_get_mode(): 
    with patch('builtins.input', return_value='1'):
        mode = Tracker.get_mode()
        assert mode == TrackingMode.AUTOMATIC

    with patch('builtins.input', return_value='2'):
        mode = Tracker.get_mode()
        assert mode == TrackingMode.MANUAL   
    
    




