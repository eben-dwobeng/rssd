###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: VST.NR5G_K144 test
###              _   ___        __  _____
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
SMW_IP  = '192.168.1.114'
FSW_IP  = '192.168.1.109'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VST.Common import VST                            #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                    #run before each test
        self.VST = VST().jav_OpenTest(SMW_IP,FSW_IP)
        self.VST.jav_ClrErr()

    def tearDown(self):                                 #Run after each test
        self.assertEqual(self.VST.SMW.jav_Error()[0],'0')
        self.assertEqual(self.VST.FSW.jav_Error()[0],'0')
        self.VST.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_VST_Freq(self):
        self.VST.Set_Freq(1e9)

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
#coverage run -a -m unittest -b -v test_HW_VST_WLAN
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
