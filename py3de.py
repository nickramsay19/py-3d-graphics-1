import math

class Engine3D:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.aspect_ratio = float(self.width) / float(self.height)

        self.fov = math.radians(90)

        self.fNear = 0.1
        self.fFar = 1000.0

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

class Cube:
    def __init__(self, engine, x, y, z, xr, yr, zr):
        self.engine = engine
        self.x = x
        self.y = y
        self.z = z
        self.xr = xr
        self.yr = yr
        self.zr = zr

        self.mat4x4 = Matrix4x4(matrix = [
            [ engine.aspect_ratio * engine.fov, 0.0,        0.0,                                                          0.0 ],
            [ 0.0,                              engine.fov, 0.0,                                                          0.0 ],
            [ 0.0,                              0.0,        engine.fFar / (engine.fFar - engine.fNear),                   1.0 ],
            [ 0.0,                              0.0,        (-engine.fFar * engine.fNear) / (engine.fFar - engine.fNear), 0.0 ]
        ])

        self.mesh = Mesh(triangles = [

            # South
            Triangle(vectors = [
                Vec3D(0, 0, 0), Vec3D(0, 1, 0), Vec3D(1, 1, 0)
            ]),
            Triangle(vectors = [
                Vec3D(0, 0, 0), Vec3D(1, 1, 0), Vec3D(1, 0, 0)
            ]),

            # East
            Triangle(vectors = [
                Vec3D(1, 0, 0), Vec3D(1, 1, 0), Vec3D(1, 1, 1)
            ]),
            Triangle(vectors = [
                Vec3D(1, 0, 0), Vec3D(1, 1, 1), Vec3D(1, 0, 1)
            ]),

            # North
            Triangle(vectors = [
                Vec3D(1, 0, 1), Vec3D(1, 1, 1), Vec3D(0, 1, 1)
            ]),
            Triangle(vectors = [
                Vec3D(1, 0, 1), Vec3D(0, 1, 1), Vec3D(0, 0, 1)
            ]),

            # West
            Triangle(vectors = [
                Vec3D(0, 0, 1), Vec3D(0, 1, 1), Vec3D(0, 1, 0)
            ]),
            Triangle(vectors = [
                Vec3D(0, 0, 1), Vec3D(0, 1, 0), Vec3D(0, 0, 0)
            ]),

            # Top
            Triangle(vectors = [
                Vec3D(0, 1, 0), Vec3D(0, 1, 1), Vec3D(1, 1, 1)
            ]),
            Triangle(vectors = [
                Vec3D(0, 1, 0), Vec3D(1, 1, 1), Vec3D(1, 1, 0)
            ]),

            # Bottom
            Triangle(vectors = [
                Vec3D(1, 0, 1), Vec3D(0, 0, 1), Vec3D(0, 0, 0)
            ]),
            Triangle(vectors = [
                Vec3D(1, 0, 1), Vec3D(0, 0, 0), Vec3D(1, 0, 0)
            ]),
        ])
        
    def ToTriangleList(self):
        triangle_list = []

        for tri in self.mesh.triangles:

            # rotate the triangles
            matRotZ = Matrix4x4(matrix = [
                [ math.cos(self.zr),   math.sin(self.zr), 0.0, 0.0 ],
                [ - math.sin(self.zr), math.cos(self.zr), 0.0, 0.0 ],
                [ 0.0,                0.0,              1.0, 0.0 ],
                [ 0.0,                0.0,               0.0, 1.0 ]
            ])
            matRotX = Matrix4x4(matrix = [
                [ 1.0, 0.0,                      0.0,                    0.0 ],
                [ 0.0, math.cos(self.xr * 0.5),   math.sin(self.xr * 0.5), 0.0 ],
                [ 0.0, - math.sin(self.xr * 0.5), math.cos(self.xr * 0.5), 0.0 ],
                [ 0.0, 0.0,                      0.0,                    1.0]
            ])

            triRotatedZ = Triangle(vectors = [
                Matrix4x4.MultipleMatrixVector(tri.vectors[0], matRotZ),
                Matrix4x4.MultipleMatrixVector(tri.vectors[1], matRotZ),
                Matrix4x4.MultipleMatrixVector(tri.vectors[2], matRotZ)
            ])
            triRotatedZX = Triangle(vectors = [
                Matrix4x4.MultipleMatrixVector(triRotatedZ.vectors[0], matRotX),
                Matrix4x4.MultipleMatrixVector(triRotatedZ.vectors[1], matRotX),
                Matrix4x4.MultipleMatrixVector(triRotatedZ.vectors[2], matRotX)
            ])

            # translate the triangles
            triTranslated = Triangle(vectors = [
                Vec3D(triRotatedZX.vectors[0].x + self.x, triRotatedZX.vectors[0].y + self.y, triRotatedZX.vectors[0].z + self.z),
                Vec3D(triRotatedZX.vectors[1].x + self.x, triRotatedZX.vectors[1].y + self.y, triRotatedZX.vectors[1].z + self.z),
                Vec3D(triRotatedZX.vectors[2].x + self.x, triRotatedZX.vectors[2].y + self.y, triRotatedZX.vectors[2].z + self.z),
            ])

            # projection, normalise
            triProjected = Triangle()
            triProjected.vectors[0] = Matrix4x4.MultipleMatrixVector(triTranslated.vectors[0], self.mat4x4)
            triProjected.vectors[1] = Matrix4x4.MultipleMatrixVector(triTranslated.vectors[1], self.mat4x4)
            triProjected.vectors[2] = Matrix4x4.MultipleMatrixVector(triTranslated.vectors[2], self.mat4x4)

            # scale back into width & height
            triProjected.vectors[0].x += 1.0; triProjected.vectors[0].y += 1.0
            triProjected.vectors[1].x += 1.0; triProjected.vectors[1].y += 1.0
            triProjected.vectors[2].x += 1.0; triProjected.vectors[2].y += 1.0

            triProjected.vectors[0].x *= 0.5 * float(self.engine.width); triProjected.vectors[0].y *= 0.5 * float(self.engine.height); 
            triProjected.vectors[1].x *= 0.5 * float(self.engine.width); triProjected.vectors[1].y *= 0.5 * float(self.engine.height); 
            triProjected.vectors[2].x *= 0.5 * float(self.engine.width); triProjected.vectors[2].y *= 0.5 * float(self.engine.height); 

            triangle_list.append(Triangle(vectors = [
                Vec3D(triProjected.vectors[0].x, triProjected.vectors[0].y, triProjected.vectors[0].z ),
                Vec3D(triProjected.vectors[1].x, triProjected.vectors[1].y, triProjected.vectors[1].z ),
                Vec3D(triProjected.vectors[2].x, triProjected.vectors[2].y, triProjected.vectors[2].z ),
            ]))

        return triangle_list