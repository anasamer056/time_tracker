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
            start = int(row["work"])
            end = int(row["relax"])
            expected_data.append({"date": day, "work": start, "relax": end})

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
    
    
def test_sort():
    tracker = Tracker("Test")
    # Arrange
    test_data = [
        {
            "date": date.fromisoformat("2023-09-09"),
            "work": 2,
            "relax": 2, 
        },
        {
            "date": date.fromisoformat("2023-09-04"),
            "work": 0,
            "relax": 0, 
        },
        {
            "date": date.fromisoformat("2023-09-07"),
            "work": 1,
            "relax": 1, 
        },
        {
            "date": date.fromisoformat("2023-09-15"),
            "work": 4,
            "relax": 4, 
        },
        {
            "date": date.fromisoformat("2023-09-11"),
            "work": 3,
            "relax": 3, 
        },

    ]
    correct_output = [
        {
            "date": date.fromisoformat("2023-09-04"),
            "work": 0,
            "relax": 0, 
        },
        {
            "date": date.fromisoformat("2023-09-07"),
            "work": 1,
            "relax": 1, 
        },
        {
            "date": date.fromisoformat("2023-09-09"),
            "work": 2,
            "relax": 2, 
        },
        {
            "date": date.fromisoformat("2023-09-11"),
            "work": 3,
            "relax": 3, 
        },
         {
            "date": date.fromisoformat("2023-09-15"),
            "work": 4,
            "relax": 4, 
        },
    ]
    # Act 
    test_output = tracker.sort(test_data)
    # Assert 
    assert test_output == correct_output