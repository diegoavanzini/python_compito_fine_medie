from src import calcolo_scadenza

def test_calcola_scadenza_should_return_a_day_before():
    assert calcolo_scadenza("12/04/2026") == "11/04/2026"