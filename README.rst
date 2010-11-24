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

..

  .. |panglery| replace:: ``panglery``
  .. |exocet| replace:: ``exocet``
  .. _exocet: https://launchpad.net/exocet

