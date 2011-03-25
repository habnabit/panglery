"""Pangler objects for panglery.
"""

import inspect
import weakref

_DEFAULT_ID = object()

class Pangler(object):
    """A pangler.

    Panglers store hooks for events and dispatch to these hooks when an event
    is triggered. Event parameters can be modified or added.

    """

    _bound_pangler_cache = weakref.WeakKeyDictionary()

    def __init__(self, id=_DEFAULT_ID):
        super(Pangler, self).__init__()
        self.id = id
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

    def clone(self):
        p = type(self)(self.id)
        p.hooks = list(self.hooks)
        p.instance = self.instance
        return p

    def combine(self, *others):
        p = self.clone()
        for other in others:
            p.hooks.extend(other.hooks)
        return p

    def bind(self, instance):
        p = self.clone()
        p.instance = instance
        return p

    def cached_bind(self, instance):
        cache = self._bound_pangler_cache.get(instance)
        if cache is None:
            # If we don't use a weak value dictionary here, the strong
            # reference to the cached bound pangler will create an
            # uncollectable cycle.
            cache = self._bound_pangler_cache[instance] = (
                weakref.WeakValueDictionary())
        p = cache.get(self.id)
        if p is None:
            p = cache[self.id] = self.bind(instance)
        return p

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.cached_bind(instance)

    @classmethod
    def from_cache(cls, instance, id=_DEFAULT_ID):
        return cls._bound_pangler_cache[instance][id]

_DEFAULT_AGGREGATE_ID = object()

class PanglerAggregate(object):
    def __init__(self, attr_name=None, id=_DEFAULT_AGGREGATE_ID):
        super(PanglerAggregate, self).__init__()
        self.attr_name = attr_name
        self.id = id

    def __get__(self, instance, owner):
        if instance is None or self.attr_name is None:
            return self
        # Make the descriptor return a callable instead of just spewing out a
        # new pangler.
        return lambda: self.aggregate(instance, owner)

    pangler_factory = Pangler
    def aggregate(self, instance, owner):
        """Given an instance and a class, aggregate together some panglers.

        Walks every class in the MRO of the `owner` class, including `owner`,
        collecting panglers exposed as `self.attr_name`. The resulting pangler
        will be bound to the provided `instance`.

        """

        try:
            p = self.pangler_factory.from_cache(instance, self.id)
        except KeyError:
            pass
        else:
            return p
        p = self.pangler_factory(self.id)
        mro = inspect.getmro(owner)
        others = []
        for cls in mro:
            sub_p = getattr(cls, self.attr_name, None)
            if sub_p is None:
                continue
            others.append(sub_p)
        return p.combine(*others).cached_bind(instance)

class _Hook(object):
    def __init__(self, func, needs, parameters, returns, conditions):
        super(_Hook, self).__init__()
        self.func = func
        self.needs = needs
        self.parameters = parameters
        self.returns = returns
        self.conditions = conditions

    def matches(self, event):
        if not all(key in event for key in self.needs):
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
