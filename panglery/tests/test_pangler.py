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

