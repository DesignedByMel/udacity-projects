from math import sqrt, acos, degrees, pi

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_COMPONENET_PARALLEL_VECTOR_MSG = "No unique parallel component vector to this basis vector"
    NO_UNIQUE_COMPONENET_ORTHONGONAL_VECTOR_MSG = "No unique orthogonal component vector to this basis vector"
    ONLY_DEFINED_IN_TWO_OR_THREE_DIM_MSG = "Cross Product is only defined in 2 or 3 dimensions"

    def plus(self, v):
        new_cord = [x + y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_cord)


    def minus(self, v):
        new_cord = [x - y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_cord)


    def scalar_mult(self, c):
        new_cord = [c*x for x in self.coordinates]
        return Vector(new_cord)


    def magnitude(self):
        return sqrt(sum([x**2 for x in self.coordinates]))


    def normalize(self):
        try:
            mag = self.magnitude()
            return self.scalar_mult(1.0/mag)

        except ZeroDivisionError:
            raise Exception("Cannot normalize the zero vector")


    def dot_product(self, v):
        return sum([x * y for x,y in zip(self.coordinates, v.coordinates)])

    def cross_product(self, v):
        v1 = self.coordinates
        v2 = v.coordinates

        try:
            self.check_dim()
            v.check_dim()

            x = (v1[1] * v2[2]) - (v2[1] * v1[2])
            y = -((v1[0] * v2[2]) - (v2[0] * v1[2]))
            z = (v1[0] * v2[1]) - (v2[0] * v1[1])

            return Vector([x, y, z])

        except ValueError as e:
            msg = str(e)
            if msg == 'two dimensional':
                self_inflated = Vector(self.coordinates + (0, ))
                v_inflated = Vector(v.coordinates + (0, ))
                return self_inflated.cross_product(v_inflated)
            elif msg == 'needs to be in three dimensions':
                raise Exception(self.ONLY_DEFINED_IN_TWO_OR_THREE_DIM_MSG)
            else:
                raise e

    def check_dim(self):
        if self.dimension == 2:
            raise ValueError('two dimensional')
        elif self.dimension != 3:
            raise ValueError("needs to be in three dimensions")


    def area_paralellogram(self, v):
        cross = self.cross_product(v)
        return sqrt(sum([x**2 for x in cross.coordinates]))


    def area_triangle(self, v):
        return self.area_paralellogram(v) / 2


    def angle_between(self, v, in_degrees=False):
        try:
            inner_mult = self.dot_product(v)
            angle_in_radians = acos(inner_mult/(self.magnitude() * v.magnitude()))

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

        if in_degrees:
            return degrees(angle_in_radians)

        return angle_in_radians


    def is_parallel(self, v):
        if(self.is_zero_vector() or v.is_zero_vector() or
           self.angle_between(v) == 0 or self.angle_between(v) == pi):
            return True
        else:
            return False


    def component_orthogonal_vector(self, v_basis):
        try:
            v_project = self.component_projection_vector(v_basis)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_COMPONENET_PARALLEL_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_COMPONENET_ORTHONGONAL_VECTOR_MSG)
            else:
                raise e

        return self.minus(v_project)


    def component_projection_vector(self, v_basis):
        try:
            u = v_basis.normalize()
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_COMPONENET_PARALLEL_VECTOR_MSG)
            else:
                raise e

        dot = self.dot_product(u)

        return u.scalar_mult(dot)


    def is_orthogonal(self, v, tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance


    def is_zero_vector(self, tolerance=1e-10):
        return self.magnitude() < tolerance


    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([x for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)



    def __eq__(self, v):
        return self.coordinates == v.coordinates


Vector([1, 2]).cross_product(Vector([2, 1]))