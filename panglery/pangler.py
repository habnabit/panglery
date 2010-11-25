"""Pangler objects for panglery.
"""

class Pangler(object):
    def __init__(self):
        self.hooks = []

    def add_hook(self, _func=None, needs=(), returns=(), modifies=(),
            **conditions):
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
        if not event:
            raise ValueError("tried to trigger nothing")
        for hook in self.hooks:
            if hook.matches(event):
                hook.execute(self, event)

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
        result = self.func(pangler, **relevant)
        if result is not None:
            event.update(result)
