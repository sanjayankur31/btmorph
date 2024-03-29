'''
Test routines for the btstructs2.py file
'''

import numpy
import random as rndm
from  nose.tools import raises
import math
from nose.tools import with_setup

import btmorph
from btmorph import STree2

def test_soma_type_3ps():
    """
    Test if SWC 3-point soma  description is correctly recognized
    """
    swc_tree1 = STree2()
    soma_type = swc_tree1._determine_soma_type("tests/v_e_moto1.CNG.swc")
    assert(soma_type == 1)

def test_soma_type_mc():
    """
    Test if SWC multiple cylinder soma  description is correctly recognized
    """
    swc_tree1 = STree2()
    soma_type = swc_tree1._determine_soma_type("tests/soma_types/l22.CNG.swc")
    assert(soma_type == 2)

def test_load_swc():
    '''
    Test whether SWC files are correctly loaded
    '''
    swc_tree = btmorph.STree2()
    swc_tree.read_SWC_tree_from_file('tests/v_e_moto1.CNG.swc')
    all_nodes1 = swc_tree.get_nodes()

    print '\nlen(swc_tree1)', len(all_nodes1) 

    assert(len(all_nodes1) == 562)
    
def test_load_and_write_swc():
    '''
    Test whether SWC trees are correctly written to file
    '''
    swc_tree = STree2()
    swc_tree.read_SWC_tree_from_file('tests/v_e_moto1.CNG.swc')
    swc_tree.write_SWC_tree_to_file('tests/moto_1_outputted.swc')
    swc_tree2 = STree2()
    swc_tree2.read_SWC_tree_from_file('tests/moto_1_outputted.swc')
    print 'len(swc_tree2)', len(swc_tree2.get_nodes()) 
    
    assert(len(swc_tree2.get_nodes()) == 562)
        
def test_load_swc_mcs1():
    '''
    Test whether SWC files with multiple-cylinder soma format are read correctly (l22)
    '''
    print "\n"
    swc_tree = btmorph.STree2()
    swc_tree.read_SWC_tree_from_file('tests/soma_types/l22.CNG.swc')
    all_nodes1 = swc_tree.get_nodes()
    print '\nlen(swc_tree1)', len(all_nodes1) 
    assert(len(all_nodes1) == 1595)
    assert(1416 < btmorph.BTStats(swc_tree).approx_soma() < 1417)

def test_load_swc_mcs2():
    '''
    Test whether SWC files with multiple-cylinder soma format are read correctly (ri05)
    '''
    print "\n"
    swc_tree = btmorph.STree2()
    swc_tree.read_SWC_tree_from_file('tests/soma_types/ri05.CNG.swc')
    all_nodes1 = swc_tree.get_nodes()
    print '\nlen(swc_tree1)', len(all_nodes1) 
    assert(len(all_nodes1) == 8970)
    assert(503 < btmorph.BTStats(swc_tree).approx_soma() < 504)
    
