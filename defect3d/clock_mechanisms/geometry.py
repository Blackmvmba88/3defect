"""Sampled involute spur profiles and continuous helical wire meshes."""
import math
from defect3d.core.shapes import Shape3D


def positive(value, name):
    if isinstance(value, bool) or not math.isfinite(value) or value <= 0:
        raise ValueError(f'{name} must be finite and positive')


def integer(value, name, minimum=1):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f'{name} must be an integer >= {minimum}')


def position3(value):
    if len(value) != 3 or not all(math.isfinite(v) for v in value):
        raise ValueError('position must contain three finite coordinates')


class ClockMesh(Shape3D):
    """Local-space polygon mesh; compatible with CompositePart and BlenderExporter."""
    def __init__(self, vertices, faces, position=(0, 0, 0), name='clock_mesh'):
        super().__init__(position=position)
        self.vertices = vertices
        self.faces = faces
        self.name = name

    def to_dict(self):
        return dict(super().to_dict(), vertices=self.vertices, faces=self.faces)

    def get_bounds(self):
        import numpy as np
        from defect3d.core.transformations import apply_transform, transform_point
        matrix = apply_transform(self.position, self.rotation, self.scale)
        points = np.array([transform_point(v, matrix) for v in self.vertices])
        return points.min(axis=0), points.max(axis=0)


def gear_mesh(teeth, module, thickness, pressure_angle, samples, position):
    rp = teeth * module / 2
    rb = rp * math.cos(math.radians(pressure_angle))
    root = rp - 1.25 * module
    tip = rp + module
    def inv(r):
        t = math.sqrt(max(0, (r / rb)**2 - 1))
        return t - math.atan(t)
    half = math.pi / (2 * teeth) + inv(rp)
    if half - inv(tip) <= 0:
        raise ValueError('pressure angle produces a pointed/overlapping tooth')
    profile = []
    def point(r, a):
        profile.append((r * math.cos(a), r * math.sin(a)))
    for i in range(teeth):
        center = i * 2 * math.pi / teeth
        point(root, center - half)
        for j in range(samples + 1):
            r = max(root, rb) + (tip - max(root, rb)) * j / samples
            point(r, center - half + inv(r))
        # Sample the addendum arc between the involute flanks.
        a = half - inv(tip)
        for j in range(1, samples + 1):
            point(tip, center - a + 2 * a * j / samples)
        for j in range(samples - 1, -1, -1):
            r = max(root, rb) + (tip - max(root, rb)) * j / samples
            point(r, center + half - inv(r))
        point(root, center + half)
        for j in range(1, samples):
            point(root, center + half + (2 * math.pi / teeth - 2 * half) * j / samples)
    n = len(profile)
    vertices = [(x, y, z) for z in (-thickness/2, thickness/2) for x, y in profile]
    vertices += [(0, 0, -thickness/2), (0, 0, thickness/2)]
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.extend([(i, j, j+n, i+n), (2*n, j, i), (2*n+1, i+n, j+n)])
    area = abs(sum(profile[i][0]*profile[(i+1)%n][1] - profile[(i+1)%n][0]*profile[i][1] for i in range(n))) / 2
    return ClockMesh(vertices, faces, position, 'involute_gear'), area * thickness


def spring_mesh(coils, wire, diameter, length, samples, position):
    radius, tube = diameter/2, wire/2
    segments = max(2, math.ceil(coils * samples))
    slope = length / (2 * math.pi * coils)
    norm = math.hypot(radius, slope)
    vertices, faces, centerline = [], [], []
    sides = 12
    for i in range(segments + 1):
        t = 2 * math.pi * coils * i / segments
        c, s = math.cos(t), math.sin(t)
        center = (radius*c, radius*s, length*i/segments)
        centerline.append(center)
        # Radial normal and tangent-cross-normal form a continuous tube frame.
        for j in range(sides):
            a = 2 * math.pi * j / sides
            u, v = tube*math.cos(a), tube*math.sin(a)
            vertices.append((center[0]+u*c-v*s*slope/norm,
                             center[1]+u*s+v*c*slope/norm,
                             center[2]-v*radius/norm))
    for i in range(segments):
        for j in range(sides):
            k = (j+1)%sides
            faces.append((i*sides+j, i*sides+k, (i+1)*sides+k, (i+1)*sides+j))
    faces += [tuple(reversed(range(sides))), tuple(segments*sides+j for j in range(sides))]
    return ClockMesh(vertices, faces, position, 'helical_spring'), centerline
