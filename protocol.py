import types
from collections import defaultdict


class ProtocolNotImplementedError(Exception): pass
class ProtocolDefinitionError(Exception): pass


class Protocol(object):
    def __init__(self, name, fn_arity_pairs):
        self.name = name
        self.fns = {}
        for pair in fn_arity_pairs:
            self.fns[pair] = {}

    def __repr__(self):
        return "<Protocol: {}>".format(self.name)

    def __str__(self):
        return repr(self)

    def dispatch_for(self, fn_name):
        def dispatch(obj, *args):
            typ = type(obj)
            arity = len(args) + 1
            try:
                func = self.fns[(fn_name, arity)]
                try:
                    impl = func[typ]
                except KeyError:
                    raise ProtocolNotImplementedError(
                            "{} {}/{} not implemented for type {}.".format(self, fn_name, arity, typ)
                            )
            except KeyError:
                raise ProtocolDefinitionError("{} {}/{} not defined.".format(self, fn_name, arity))
            return impl(obj, *args)
        dispatch.__name__ = "{} {}".format(str(self), fn_name)
        return dispatch

    def extend_to(self, typ, fn_name, arity=1):
        def extend(fn):
            self.fns[(fn_name, arity)][typ] = fn
            return fn
        return extend


def name_and_arity(s):
    """
    'foo/1' => ('foo', 1)
    """
    name, arity = s.split("/")
    return (name, int(arity))


def defprotocol(name, fns):
    """
    defprotocol('IFoo', ['foo/1', 'foo/2'])
    """
    return Protocol(name, map(name_and_arity, fns))


ICounted = defprotocol("ICounted", ["count/1"])
count = ICounted.dispatch_for("count")

@ICounted.extend_to(types.NoneType, "count")
def none_count(o):
    return 0

@ICounted.extend_to(dict, "count")
def dict_count(d):
    return len(d)

ISeq = defprotocol("ISeq", ["first/1", "rest/1"])
first = ISeq.dispatch_for("first")
rest = ISeq.dispatch_for("rest")

@ISeq.extend_to(list, "first")
def list_first(l):
    return l[0]

@ISeq.extend_to(list, "rest")
def list_rest(l):
    return l[1:]

@ISeq.extend_to(dict, "first")
def dict_first(d):
    return next(d.iteritems())

@ISeq.extend_to(dict, "rest")
def dict_rest(d):
    items = d.iteritems()
    next(items)
    return items
