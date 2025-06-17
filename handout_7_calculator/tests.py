import unittest
import my_calculator

class TestCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(my_calculator.run("1 + 1"), 2)

    def test_sub(self):
        self.assertEqual(my_calculator.run("1 - 1"), 0)

    def test_addnsub(self):
        self.assertEqual(my_calculator.run("5 + 3 + 4 - 1"), 11)

    def test_multiply(self):
        self.assertEqual(my_calculator.run("7 * 7"), 49)

    def test_divide(self):
        self.assertEqual(my_calculator.run("57 / 19"), 3)

    def test_add_multiply(self):
        self.assertEqual(my_calculator.run("2 + 2 * 2"), 8)


if __name__ == "__main__":
    unittest.main()