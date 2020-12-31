import unittest
from old import strobe
from unittest.mock import MagicMock

# print(dir(old.strobe))

class TestStringMethods(unittest.TestCase):
  def test_canRun(self):

    machine = MagicMock()

    pwm = MagicMock()

    time = MagicMock()


    s = strobe.Strobe(machine, pwm, time)
    s.run()
    self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
    self.assertTrue('FOO'.isupper())
    self.assertFalse('Foo'.isupper())

  def test_split(self):
    s = 'hello world'
    self.assertEqual(s.split(), ['hello', 'world'])
    # check that s.split fails when the separator is not a string
    with self.assertRaises(TypeError):
      s.split(2)

if __name__ == '__main__':
  unittest.main()
