from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    CANNOT_NORMALIZE_THE_ZERO_VECTOR = 'cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'no unique parallel component'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'only defined in to or three dimension'
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        squared = [x**2 for x in self.coordinates]
        return sqrt(sum(squared))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal(1.0)/Decimal(magnitude))
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_THE_ZERO_VECTOR)

    def dot(self, v):
        return sum([x*y for x, y in zip(self.coordinates, v.coordinates)])

    def cross(self, v):
        try:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = v.coordinates
            new_coordinates = [y1*z2 - y2*z1, 
                               -(x1*z2 - x2*z1),
                               x1*y2 - x2*y1]
        except ValueError as e :
            msg = str(e)
            if(msg == 'need more than 2 values to unpack'):
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to umpack' or msg == 'need more than 1 value to umpack'):
                raise Exception('')
        return Vector(new_coordinates)

    def area_of_triangle_with(self, v):
        return Decimal(self.area_of_parallelogram_with(v))/Decimal('2.0')

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()

    def angle_with(self, v, in_degrees=False):
        try:
            angle_in_radians = acos(self.normalized().dot(v.normalized()))
            if in_degrees:
                return angle_in_radians * (180.0/pi)
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_THE_ZERO_VECTOR:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    # def is_zero(self, tolerance=1e-10):
    #     return self.magnitude < tolerance

    def is_zero(self):
        return set(self.coordinates) == set([Decimal(0)])

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v):
        return (self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v) == pi)


    def component_paralle_to(self, b):
        try:
            normalized_b = b.normalized()
            return normalized_b.times_scalar(self.dot(normalized_b))

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_THE_ZERO_VECTOR:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self, b):
        try:
            projection = self.component_paralle_to(b)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e


v = Vector([3.039, 1.879])
w = Vector([0.825, 2.036])
print(v.component_paralle_to(w))

v = Vector([3.009, -6.172, 3.692, -2.51])
w = Vector([6.404, -9.144, 2.759, 8.718])
print(v.component_paralle_to(w))
print(v.component_orthogonal_to(w))

v = Vector([8.462, 7.893, -8.187])
w = Vector([6.984, -5.975, 4.778])
print(v.cross(w))

v = Vector([1.5, 9.547, 3.691])
w = Vector([-6.007, 0.124, 5.772])
print(v.area_of_parallelogram_with(w))



