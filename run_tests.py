import pytest
import sys

def run_tests():
    """
    Run TinySol Turing Completeness and BDD Tests
    """
    result = pytest.main([
        'tests/test_turing_completeness.py', 
        'tests/test_tinysol_bdd.py',
        '-v'  # Verbose output
    ])
    sys.exit(result)

if __name__ == '__main__':
    run_tests()
