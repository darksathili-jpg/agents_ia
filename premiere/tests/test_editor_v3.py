import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class EditorV3(unittest.TestCase):
 def test_no_teacher_only_phrase(self):
  self.assertNotIn('personnage de la planche fournie',(R/'index.html').read_text())
 def test_editor_is_real_editable_textarea(self):
  h=(R/'index.html').read_text()
  self.assertIn('textarea id="code"',h)
  self.assertIn('id="syntax-code"',h)
  self.assertIn('class="language-python"',h)
 def test_local_prism(self):
  for name in ('prism-core.min.js','prism-clike.min.js','prism-python.min.js'):
   self.assertTrue((R/'vendor'/name).exists())
 def test_worker_not_modified(self):
  js=(R/'app.js').read_text()
  self.assertIn("source:code.value",js)
  self.assertIn("code.addEventListener('input',()=>{setEditorLines();saveDraft();})",js)
  self.assertIn("code.addEventListener('scroll',syncEditorScroll",js)
 def test_readable_fallback(self):
  css=(R/'styles.css').read_text()
  self.assertIn('.code-shell.syntax-ready textarea{color:transparent',css)
  self.assertIn('background:#fbfdff',css)
if __name__=='__main__':unittest.main()
