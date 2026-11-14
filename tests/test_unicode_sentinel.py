import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from unicode_sentinel import scan
class Tests(unittest.TestCase):
 def test_clean(self): self.assertEqual([],scan("hello\nworld"))
 def test_bidi(self): self.assertEqual("bidi-control",scan("abc\u202edef")[0]["kind"])
 def test_zero_width(self): self.assertEqual("zero-width",scan("a\u200bb")[0]["kind"])
 def test_tab_allowed(self): self.assertEqual([],scan("a\tb"))
if __name__=="__main__": unittest.main()
