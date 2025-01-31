import task1, task2, task3, task4, task5, task6, task7

def test_task1(capfd):
    task1.task1()
    out, err = capfd.readouterr()
    assert out == "Hello, World!" or out == "Hello, World!\n"
    

def test_task2_int():
    assert task2.add(1, 2) == 3

def test_task2_float():
    assert task2.add(1.5, 3.25) == 4.75

def test_tesk2_string():
    assert task2.cat_string("Hello, ", "World!") == "Hello, World!"

def test_task2_bool():
    assert task2.weird_bool(False,True) == False


def test_odd_or_even(capfd):
    task3.odd_or_even(0)
    out, err = capfd.readouterr()
    assert out == "Zero\n"

    task3.odd_or_even(1)
    out, err = capfd.readouterr()
    assert out == "Odd\n"

    task3.odd_or_even(2)
    out, err = capfd.readouterr()
    assert out == "Even\n"

def test_get_primes(capfd):
    task3.get_primes()
    out, err = capfd.readouterr()
    assert out == "2\n3\n5\n7\n11\n13\n17\n19\n23\n29\n"

def test_sums():
    assert task3.sums() == 4950

def test_calculate_discount():
    assert task4.calculate_discount(30, 0.5) == 15
    assert task4.calculate_discount(5.82, 25) == 1.455 # handle case where discount is treated as a whole number (this is 25%)


def test_books(capfd):
    task5.books()
    out, err = capfd.readouterr()
    assert out == '["Caliban\'s War, James S.A. Corey", "Heaven\'s River, Dennis E. Taylor", \'Livesuit, James S.A. Corey\']\n'

def test_students():
    db = task5.students()
    assert db["0001"] == "Jeff"
    assert db["0004"] == "Bobbie"

def test_wordcount():
    assert task6.count_words() == 127


def test_task7():
    assert task7.get_ip()[0] == 200