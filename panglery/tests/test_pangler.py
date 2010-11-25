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

    def test_triggering_nothing(self):
        p = panglery.Pangler()
        self.assertRaises(ValueError, p.trigger)

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

    def test_binding(self):
        self.fired = False
        class TestClass(object):
            p = panglery.Pangler()
            datum = 'foo'

            @p.add_hook(event='test')
            def test_hook(self2, p):
                self.assertEqual(self2.datum, 'foo')
                self.fired = True

        inst = TestClass()
        inst.p.trigger(event='test')
        self.assert_(self.fired)

    def test_clone(self):
        p = panglery.Pangler()
        self.fired = False

        @p.add_hook(event='test')
        def test_hook(p):
            self.fired = True

        p2 = p.clone()
        p2.trigger(event='test')
        self.assert_(self.fired)

    def test_clone_subclassing(self):
        class TestPangler(panglery.Pangler):
            pass

        p = TestPangler()
        p2 = p.clone()
        self.assert_(isinstance(p2, TestPangler))

class TestPanglerAggregate(unittest.TestCase):
    def test_subclass_binding(self):
        self.fired = 0

        class TestClassA(object):
            hooks = panglery.Pangler()
            p = panglery.PanglerAggregate('hooks')

            @hooks.add_hook(event='test')
            def test_hookA(_, p):
                self.fired |= 1

        class TestClassB(TestClassA):
            hooks = panglery.Pangler()

            @hooks.add_hook(event='test')
            def test_hookB(_, p):
                self.fired |= 2

        class TestClassC(TestClassA):
            hooks = panglery.Pangler()

            @hooks.add_hook(event='test')
            def test_hookC(_, p):
                self.fired |= 4

        class TestClassD(TestClassB, TestClassC):
            hooks = panglery.Pangler()

            @hooks.add_hook(event='test')
            def test_hookD(_, p):
                self.fired |= 8

        inst = TestClassD()
        inst.p.trigger(event='test')
        self.assertEqual(self.fired, 15)

        self.fired = 0
        inst = TestClassB()
        inst.p.trigger(event='test')
        self.assertEqual(self.fired, 3)
