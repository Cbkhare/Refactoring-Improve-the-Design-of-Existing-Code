import unittest

from TW_Merchants_Guide_To_Galaxy import GalaxyQueryReader


class GuildeToGalaxyTest(unittest.TestCase):

    def test_transactions(self):
        galaxy_obj = GalaxyQueryReader()
        galaxy_obj.query("glob is I")
        galaxy_obj.query("prok is V")
        galaxy_obj.query("pish is X")
        galaxy_obj.query("tegj is L")
        galaxy_obj.query("glob glob Silver is 34 Credits")

        self.assertEqual(galaxy_obj.query("how much is pish tegj glob glob ?"),
                          'pish tegj glob glob is 42')
        self.assertEqual(galaxy_obj.query("how many Credits is glob prok "
                                           "Silver ?"),
                          'glob prok Silver is 68')

if __name__=="__main__":
    unittest.main()