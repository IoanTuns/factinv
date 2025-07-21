import operator

def to_screen(parameters={}, op=None, value=None):
    print_status = True
    ops = { 
               '+' : operator.add,
                '-' : operator.sub,
                '*' : operator.mul,
                '/' : operator.truediv,
                '//' : operator.floordiv,
                '%' : operator.mod,
                '^' : operator.xor,
            }
    for x in parameters:
        name = x
        val = parameters[x]
        if print_status is True:
            if op is not None and value is not None:
                    total = ops[op](val, value)
                    print('Pentru %s %s %s valoarea este: %s'%(
                        name,
                        op,
                        value,
                        round(total),
                    ))
            else:
                print('Pentru %s valoarea este: %s'%(
                            name,
                            val,
                        ))