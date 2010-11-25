"""Pangler objects for panglery.
"""

class Pangler(object):
    """A pangler.

    Panglers store hooks for events and dispatch to these hooks when an event
    is triggered. Event parameters can be modified or added.

    """

    def __init__(self):
        self.hooks = []
        self.instance = None

    def add_hook(self, _func=None, needs=(), returns=(), modifies=(),
            **conditions):
        """Add a hook to a pangler.

        This method can either be used as a decorator for a function or method,
        or standalone on a callable.

         * `needs` is an iterable of parameters that this hook operates on.
         * `returns` is an iterable of parameters that this hook will modify
           and then pass back to the pangler.
         * `modifies` is a convenient way to specify that this hook both needs
           and returns a parameter.
         * The rest of the keyword arguments are parameter predicates.

        """

        modifies = set(modifies)
        parameters = set(needs) | modifies
        needs = parameters | set(conditions)
        if not needs:
            raise ValueError("tried to hook nothing")
        returns = set(returns) | modifies
        def deco(func):
            self.hooks.append(_Hook(
                func, needs, parameters, returns, conditions))
            return func

        # If we were passed a function as a positional parameter, then we
        # shouldn't behave like a decorator.
        if _func is not None:
            deco(_func)
        else:
            return deco

    def trigger(self, **event):
        """Trigger an event.

        Event parameters are passed as keyword arguments. Passing an `event`
        argument isn't required, but generally recommended.

        """

        if not event:
            raise ValueError("tried to trigger nothing")
        for hook in self.hooks:
            if hook.matches(event):
                hook.execute(self, event)

    # XXX maybe this should be done some other way. A classmethod?
    def bind_object(self, instance):
        p = type(self)()
        p.hooks = list(self.hooks)
        p.instance = instance
        return p

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.bind_object(instance)

class _Hook(object):
    def __init__(self, func, needs, parameters, returns, conditions):
        self.func = func
        self.needs = needs
        self.parameters = parameters
        self.returns = returns
        self.conditions = conditions

    def matches(self, event):
        if not all(key in self.needs for key in event):
            return False
        if not all(
                event[key] == self.conditions[key]
                for key in self.conditions):
            return False
        return True

    def execute(self, pangler, event):
        relevant = dict(
            (key, value)
            for key, value in event.iteritems()
            if key in self.parameters)
        # Pass the bound instance as the first argument, i.e. self.
        if pangler.instance is not None:
            args = pangler.instance, pangler
        else:
            args = pangler,
        result = self.func(*args, **relevant)
        if result is not None:
            event.update(result)
