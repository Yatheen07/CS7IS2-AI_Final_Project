class Cube:
    '''
    Implementation of a 2x2x2 Rubik's cube
    '''
    def __init__(self):
        (flu, luf, ufl,
        fur, urf, rfu, 
        fdl, dlf, lfd, 
        frd, rdf, dfr, 
        bul, ulb, lbu, 
        bru, rub, ubr, 
        bld, ldb, dbl, 
        bdr, drb, rbd) = [i for i in range(24)]
        
        # Init state
        self.I = (
            flu, luf, ufl, 
            fur, urf, rfu, 
            fdl, dlf, lfd,
            frd, rdf, dfr, 
            bul, ulb, lbu, 
            bru, rub, ubr, 
            bld, ldb, dbl, 
            bdr, drb, rbd
        )

        # Dictionary of rotations of Front, Left and Up (Clockwise and Counterclockwise)
        self.rotations = {
            'F': (
                fdl, dlf, lfd,
                flu, luf, ufl, 
                frd, rdf, dfr, 
                fur, urf, rfu, 
                bul, ulb, lbu, 
                bru, rub, ubr, 
                bld, ldb, dbl, 
                bdr, drb, rbd
            ),
            'L': (
                ulb, lbu, bul, 
                fur, urf, rfu, 
                ufl, flu, luf, 
                frd, rdf, dfr,
                dbl, bld, ldb, 
                bru, rub, ubr, 
                dlf, lfd, fdl, 
                bdr, drb, rbd
            ),
            'U': (
                rfu, fur, urf, 
                rub, ubr, bru, 
                fdl, dlf, lfd, 
                frd, rdf, dfr,
                luf, ufl, flu, 
                lbu, bul, ulb, 
                bld, ldb, dbl, 
                bdr, drb, rbd
            ),
        }

        # Getting the counter clockwise rotations of Front, Left and Up face
        self.rotations['Fi'] = self._get_counter_clockwise(self.rotations['F'])
        self.rotations['Li'] = self._get_counter_clockwise(self.rotations['L'])
        self.rotations['Ui'] = self._get_counter_clockwise(self.rotations['U'])
    
    def _get_counter_clockwise(self, rot):
        q = [0] * len(rot)
        for i in rot:
            q[rot[i]] = i
        return tuple(q)
    
    def apply_rotation(self, node, rot):
        return tuple(rot[i] for i in node)
