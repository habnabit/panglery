========
Panglery
========

``panglery`` is a library for writing hooks for events in python. Event hooks
can be separated out into plugins with panglery's ``exocet`` [#]_ integration.

Here's a basic example of usage::

    import panglery
    p = panglery.Pangler()

    @p.add_hook(event='example', needs=['spam'])
    def example_hook(p, spam):
        print spam

    p.trigger(event='example', spam='eggs') # prints 'eggs'

And a little bit more involved::

    @p.add_hook(needs=['spam'], modifies=['spam'])
    def modify_spam_hook(p, spam):
        spam *= 2
        return {'spam': spam}

    p.trigger(event='example', spam='eggs') # prints 'eggseggs'

..

  .. [#] https://launchpad.net/exocet

