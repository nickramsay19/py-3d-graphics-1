class Engine3D:
    def __init__(self):
        pass

class Vec3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

class Triangle:
    def __init__(self, vectors = [Vec3D(), Vec3D(), Vec3D()]):
        self.vectors = vectors

class Mesh:
    def __init__(self, triangles = []):
        self.triangles = triangles

class Matrix4x4:
    def __init__(self, matrix = []):
        self.matrix = matrix

    @staticmethod
    def MultipleMatrixVector(i, m):
        o = Vec3D()

        o.x = i.x * m.matrix[0][0] + i.y * m.matrix[1][0] + i.z * m.matrix[2][0] + m.matrix[3][0]
        o.y = i.x * m.matrix[0][1] + i.y * m.matrix[1][1] + i.z * m.matrix[2][1] + m.matrix[3][1]
        o.z = i.x * m.matrix[0][2] + i.y * m.matrix[1][2] + i.z * m.matrix[2][2] + m.matrix[3][2]
        w   = i.x * m.matrix[0][3] + i.y * m.matrix[1][3] + i.z * m.matrix[2][3] + m.matrix[3][3]

        if w != 0:
            o.x /= w
            o.y /= w
            o.z /- w

        return o
