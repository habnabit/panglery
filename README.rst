========
Panglery
========

|panglery| is a library for writing hooks for events in python. Event hooks
can be separated out into plugins with |panglery|'s |exocet|_ integration.

Here's a basic example of usage::

    import panglery
    p = panglery.Pangler()

    @p.add_hook(event='example', needs=['spam'])
    def example_hook(p, spam):
        print spam

    p.trigger(event='example', spam='eggs')
    # prints 'eggs'

And a little bit more involved::

    @p.add_hook(needs=['spam'], returns=['spam'])
    def modify_spam_hook(p, spam):
        spam = spam + ' spam'
        return {'spam': spam}

    p.trigger(event='example', spam='eggs')
    # prints 'eggs spam'

Hooks can also add parameters to an event which then trigger other hooks::

    p = panglery.Pangler()

    @p.add_hook(needs=['spam'], returns=['eggs'])
    def make_eggs_hook(p, spam):
        eggs = spam + ' eggs'
        return {'eggs': eggs}

    @p.add_hook(event='example', needs=['eggs']):
    def eggs_hook(p, eggs):
        print eggs

    p.trigger(event='example', spam='eggs')
    # prints 'eggs eggs'

PanglerAggregates can be used to aggregate together multiple Panglers across
all superclasses::

    class ExampleBase(object):
        p = panglery.PanglerAggregate('hooks')
        hooks = panglery.Pangler()

        @hooks.add_hook(event='example')
        def example_hook_base(self, p):
            print 'spam'

    class ExampleDerived(ExampleBase):
        hooks = panglery.Pangler()

        @hooks.add_hook(event='example')
        def example_hook_derived(self, p):
            print 'eggs'

    inst = ExampleDerived()
    inst.p.trigger(event='example')
    # prints 'spam' and 'eggs' in some order.

..

  .. |panglery| replace:: ``panglery``
  .. |exocet| replace:: ``exocet``
  .. _exocet: https://launchpad.net/exocet

