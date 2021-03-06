# vim: set fileencoding=utf-8
from unittest import TestCase

from regparser.layer.key_terms import KeyTerms
from regparser.tree.struct import Node

class LayerKeyTermTest(TestCase):

    def test_find_keyterm(self):
        node = Node(
            '(a) <E T="03">Apples.</E> Apples are grown in New Zealand.', 
            label=['101', '22', 'a'])
        kt = KeyTerms(None)
        results = kt.process(node)
        self.assertNotEqual(results, None)
        self.assertEqual(results[0]['key_term'], 'Apples.')
        self.assertEqual(results[0]['locations'], [0])

    def test_emphasis_later(self):
        """ Don't pick up something that is emphasized later in a paragraph as a key-term. """
        node = Node('(a) This has a list: apples <E T="03">et seq.</E>', 
            label=['101', '22', 'a'])

        kt = KeyTerms(None)
        results = kt.process(node)
        self.assertEqual(results, None)

    def test_keyterm_is_first_not_first(self):
        node = Node('(a) This has a list: apples <E T="03">et seq.</E>', 
            label=['101', '22', 'a'])

        kt = KeyTerms(None)
        self.assertFalse(kt.keyterm_is_first(node, 'et seq.'))

    def test_emphasis_close_to_front(self):
        """ An emphasized word is close to the front, but is not a key term. """
        node = Node('(a) T <E T="03">et seq.</E> has a list: apples', 
            label=['101', '22', 'a'])
        kt = KeyTerms(None)
        self.assertFalse(kt.keyterm_is_first(node, 'et seq.'))

    def test_interpretation_markers(self):
        node = Node('3. <E T="03">et seq.</E> has a list: apples', 
            label=['101', 'c', Node.INTERP_MARK, '3'])
        kt = KeyTerms(None)
        results = kt.process(node)
        self.assertNotEqual(results, None)
        self.assertEqual(results[0]['key_term'], 'et seq.')
        self.assertEqual(results[0]['locations'], [0])

    def test_no_keyterm(self):
        node = Node('(a) Apples are grown in New Zealand.', 
            label=['101', '22', 'a'])
        kt = KeyTerms(None)
        results = kt.process(node)
        self.assertEquals(results, None)

    def test_keyterm_and_emphasis(self):
        node = Node('(a) <E T="03">Apples.</E> Apples are grown in '
            + 'New <E T="03">Zealand.</E>', label=['101', '22', 'a'])
        kt = KeyTerms(None)
        results = kt.process(node)
        self.assertNotEqual(results, None)
        self.assertEqual(results[0]['key_term'], 'Apples.')
        self.assertEqual(results[0]['locations'], [0])

