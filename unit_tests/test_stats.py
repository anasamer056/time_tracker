from stats import Stats
# from unittest import patch
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
    stats = Stats("test")
    # Arrange
    clean_data = [
            {"date": date.fromisoformat("2023-09-10"), "work": 190, "relax": 60},
            {"date": date.fromisoformat("2023-09-11"), "work": 150, "relax": 60},
            {"date": date.fromisoformat("2023-09-12"), "work": 120, "relax": 60},
            {"date": date.fromisoformat("2023-09-13"), "work": 130, "relax": 60},
            {"date": date.fromisoformat("2023-09-14"), "work": 150, "relax": 60},
            ]
    assert stats.get_streak(clean_data) == 5

def test_get_streak_break():
    stats = Stats("test")
    clean_data = [
            {"date": date.fromisoformat("2023-09-10"), "work": 190, "relax": 60},
            {"date": date.fromisoformat("2023-09-11"), "work": 150, "relax": 60},
            {"date": date.fromisoformat("2023-09-13"), "work": 130, "relax": 60},
            {"date": date.fromisoformat("2023-09-14"), "work": 150, "relax": 60},
            {"date": date.fromisoformat("2023-09-15"), "work": 150, "relax": 60},
            {"date": date.fromisoformat("2023-09-16"), "work": 150, "relax": 60},
            ]
    assert stats.get_streak(clean_data) == 4

def test_get_streak_single_day():
    stats = Stats("test")
    clean_data = [
            {"date": date.fromisoformat("2023-09-10"), "work": 190, "relax": 60},
            ]
    assert stats.get_streak(clean_data) == 1
    
def test_get_streak_zero():
    stats = Stats("test")
    clean_data = []
    assert stats.get_streak(clean_data) == 0
    
