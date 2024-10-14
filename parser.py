
def parse_args( args ):
    results = []
    i = 0
    while i < len( args ):
        arg = args[ i ]
        if "-" in arg[:2]:
            if i + 1 < len( args ):
                results.append( ( arg, arg[ i + 1 ] ) )
                i += 1
        i += 1
