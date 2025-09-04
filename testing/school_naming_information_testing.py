import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from school_naming_information import *



def test_get_school_naming_infomation_mississippi_state():
    # Change to the root directory to ensure database path is correct
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        result = get_school_naming_infomation("Mississippi State")
        expected = ("Mississippi St.", ["Mississippi State", " Mississippi St", " Miss State"], "S01134")
        assert result == expected, f"Expected {expected}, but got {result}"
        print("✓ Test passed: Mississippi State -> Mississippi St.")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def test_get_school_naming_infomation_ole_miss():
    # Change to the root directory to ensure database path is correct
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        result = get_school_naming_infomation("Ole Miss")
        expected = ("Mississippi", ["Ole Miss"], "S01135")
        assert result == expected, f"Expected {expected}, but got {result}"
        print("✓ Test passed: Ole Miss -> Mississippi")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def test_get_school_naming_infomation_florida():
    # Change to the root directory to ensure database path is correct
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        result = get_school_naming_infomation("Florida")
        expected = ("Florida", [], "S00629")
        assert result == expected, f"Expected {expected}, but got {result}"
        print("✓ Test passed: Florida -> Florida")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def test_get_school_naming_infomation_florida_state():
    # Change to the root directory to ensure database path is correct
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        result = get_school_naming_infomation("Florida State")
        expected = ("Florida St.", ["Florida State", " Florida St"], "S00627")
        assert result == expected, f"Expected {expected}, but got {result}"
        print("✓ Test passed: Florida State -> Florida St.")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def test_get_school_naming_infomation_florida_international_one():
    # Change to the root directory to ensure database path is correct
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        result = get_school_naming_infomation("Florida International")
        expected = ("Florida Int.", ["Florida International", " Florida Intl", " Fla. International", " FIU", ], "S00624")
        assert result == expected, f"Expected {expected} \n but got {result}"
        print("✓ Test passed: Florida International -> Florida Int.")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def test_get_school_naming_infomation_florida_international_two():
    # Change to the root directory to ensure database path is correct
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        result = get_school_naming_infomation("FIU")
        expected = ("Florida Int.", ["Florida International", " Florida Intl", " Fla. International", " FIU", ], "S00624")
        assert result == expected, f"Expected {expected} \n but got {result}"
        print("✓ Test passed: FIU -> Florida Int.")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def test_get_school_naming_infomation_florida_international_three():
    # Change to the root directory to ensure database path is correct
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        result = get_school_naming_infomation("Florida Int.")
        expected = ("Florida Int.", ["Florida International", " Florida Intl", " Fla. International", " FIU", ], "S00624")
        assert result == expected, f"Expected {expected} \n but got {result}"
        print("✓ Test passed: Florida Int. -> Florida Int.")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def test_get_school_naming_information_indiana():
    # Change to the root directory to ensure database path is correct
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        result = get_school_naming_infomation("Indiana")
        expected = ("Indiana", [], "S00827")
        assert result == expected, f"Expected {expected} \n but got {result}"
        print("✓ Test passed: Indiana -> Indiana")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def test_get_school_naming_information_indiana_state():
    # Change to the root directory to ensure database path is correct
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    try:
        result = get_school_naming_infomation("Indiana State")
        expected = ("Indiana St.", ["IN State", " Indiana State", " Indiana St"], "S00821")
        
        assert result == expected, f"Expected {expected} \n but got {result}"
        print("✓ Test passed: Indiana State -> Indiana St.")

    finally:
        # Change back to original directory
        os.chdir(original_dir)

def main():
    print("------------------------------------------------------------------------")
    print("TESTING STARTED")
    print("------------------------------------------------------------------------")
    print("SCHOOLS IN THE STATE OF MISSISSIPPI")
    print("------------------------------------------------------------------------")
    test_get_school_naming_infomation_mississippi_state()
    test_get_school_naming_infomation_ole_miss()
    print("------------------------------------------------------------------------")
    print("SCHOOLS IN THE STATE OF FLORIDA")
    print("------------------------------------------------------------------------")
    test_get_school_naming_infomation_florida()
    test_get_school_naming_infomation_florida_state()
    test_get_school_naming_infomation_florida_international_one()
    test_get_school_naming_infomation_florida_international_two()
    test_get_school_naming_infomation_florida_international_three()
    print("------------------------------------------------------------------------")
    print("SCHOOLS IN THE STATE OF INDIANA")
    print("------------------------------------------------------------------------")
    test_get_school_naming_information_indiana()
    test_get_school_naming_information_indiana_state()
    print("------------------------------------------------------------------------")

    




if __name__ == "__main__":
    main()