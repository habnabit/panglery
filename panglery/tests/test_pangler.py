import unittest
import panglery

class TestPangler(unittest.TestCase):
    def test_basic_event(self):
        p = panglery.Pangler()
        self.fired = False

        @p.add_hook(event='test')
        def test_hook(p):
            self.fired = True

        p.trigger(event='test')
        self.assert_(self.fired)

    def test_basic_event_without_decorator(self):
        p = panglery.Pangler()
        self.fired = False

        def test_hook(p):
            self.fired = True
        p.add_hook(test_hook, event='test')

        p.trigger(event='test')
        self.assert_(self.fired)

    def test_hooking_nothing(self):
        p = panglery.Pangler()
        self.assertRaises(ValueError, p.add_hook, lambda: None)

    def test_receiving_parameters(self):
        p = panglery.Pangler()
        self.fired = False

        @p.add_hook(needs=['test'])
        def test_hook(p, test):
            self.assertEqual(test, 'testval')
            self.fired = True

        p.trigger(test='testval')
        self.assert_(self.fired)

    def test_modifying_parameters(self):
        p = panglery.Pangler()
        self.fired = False

        @p.add_hook(modifies=['foo'])
        def foo_hook(p, foo):
            return {'foo': foo * 2}

        @p.add_hook(needs=['foo'])
        def foo_hook2(p, foo):
            self.assertEqual(foo, 6)
            self.fired = True

        p.trigger(foo=3)
        self.assert_(self.fired)
