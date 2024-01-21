def print_flush(*args, **kwargs):
    kwargs['flush'] = True
    print(*args, **kwargs)
