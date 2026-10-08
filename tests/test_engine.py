import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from tests.run_tests import main
def test_all_scenarios():
    assert main()==0
