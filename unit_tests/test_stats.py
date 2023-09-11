from stats import Stats
from unittest.mock import patch
from datetime import date

# def test_read_from_memory():
    # pass 
    # activity_name = "stats_fixture"
    # stats = Stat(activity_name)
    # test_file_path = f"unit_tests/fixtures/{activity_name}"
    # with patch.object(Tracker, "file_path", test_file_path):
       # pass

    #! TODO 
    # assert 1 == 1
    
def test_get_streak_true():
    # Arrange
    clean_data = [
            {"date": date.fromisoformat("2023-09-10"), "work": 190, "relax": 60},
            {"date": date.fromisoformat("2023-09-11"), "work": 150, "relax": 60},
            {"date": date.fromisoformat("2023-09-12"), "work": 120, "relax": 60},
            {"date": date.fromisoformat("2023-09-13"), "work": 130, "relax": 60},
            {"date": date.fromisoformat("2023-09-14"), "work": 150, "relax": 60},
            ]
    
    with patch.object(Stats, "clean_data", clean_data):
        stats = Stats("test", clean_data) 
        assert stats.get_streak() == 5

def test_get_streak_break():
    clean_data = [
            {"date": date.fromisoformat("2023-09-10"), "work": 190, "relax": 60},
            {"date": date.fromisoformat("2023-09-11"), "work": 150, "relax": 60},
            {"date": date.fromisoformat("2023-09-13"), "work": 130, "relax": 60},
            {"date": date.fromisoformat("2023-09-14"), "work": 150, "relax": 60},
            {"date": date.fromisoformat("2023-09-15"), "work": 150, "relax": 60},
            {"date": date.fromisoformat("2023-09-16"), "work": 150, "relax": 60},
            ]
    with patch.object(Stats, "clean_data", clean_data):
        stats = Stats("test", clean_data) 
        assert stats.get_streak() == 4

def test_get_streak_single_day():
    clean_data = [
            {"date": date.fromisoformat("2023-09-10"), "work": 190, "relax": 60},
            ]

    with patch.object(Stats, "clean_data", clean_data):
        stats = Stats("test", clean_data) 
        assert stats.get_streak() == 1

    
def test_get_streak_zero():
    clean_data = []
   
    with patch.object(Stats, "clean_data", clean_data):
        stats = Stats("test", clean_data) 
        assert stats.get_streak() == 0

def test_get_total_work():
    clean_data = [
            {"date": date.fromisoformat("2023-09-10"), "work": 5, "relax": 2},
            {"date": date.fromisoformat("2023-09-11"), "work": 4, "relax": 4},
            {"date": date.fromisoformat("2023-09-12"), "work": 1, "relax": 6},
            {"date": date.fromisoformat("2023-09-13"), "work": 3, "relax": 3},
            {"date": date.fromisoformat("2023-09-14"), "work": 2, "relax": 5},
            ]
    total_work = 15
    total_relax = 20

    with patch.object(Stats, "clean_data", clean_data):
        stats = Stats("test", clean_data) 
        assert stats.get_total_work_and_relax() == (total_work, total_relax)


def test_get_total_work_one_input():
    clean_data = [
            {"date": date.fromisoformat("2023-09-10"), "work": 5, "relax": 2},
            ]
    total_work = 5
    total_relax = 2

    with patch.object(Stats, "clean_data", clean_data):
        stats = Stats("test", clean_data) 
        assert stats.get_total_work_and_relax() == (total_work, total_relax)
