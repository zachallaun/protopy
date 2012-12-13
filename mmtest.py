from multimethod import defmulti, defmethod

do_work = defmulti(type)

@defmethod(do_work, str)
def do_str_work(s):
    return "a string"

@defmethod(do_work, int)
def do_int_work(i):
    return "an int"

@defmethod(do_work, list)
def do_list_work(l):
    return "a list"

@defmethod(do_work, tuple)
def do_tuple_work(t):
    return "a tuple"

@defmethod(do_work, dict)
def do_dict_work(d):
    return "a dict"
