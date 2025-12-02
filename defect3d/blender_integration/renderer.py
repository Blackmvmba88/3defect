"""
Sistema de renderizado para generar imágenes fotorrealistas.
Rendering system to generate photorealistic images.

Este módulo permite renderizar modelos 3D directamente sin necesidad de abrir Blender manualmente.
This module allows rendering 3D models directly without manually opening Blender.
"""

import os
import subprocess
import tempfile
from typing import Optional, Tuple
from .exporter import BlenderExporter


class BlenderRenderer:
    """
    Renderizador que genera imágenes usando Blender en segundo plano.
    Renderer that generates images using Blender in the background.
    """

    def __init__(self, blender_path: Optional[str] = None):
        """
        Inicializa el renderizador.
        Initialize the renderer.

        Args:
            blender_path: Ruta al ejecutable de Blender. Si es None, intenta encontrarlo automáticamente.
                         Path to Blender executable. If None, tries to find it automatically.
        """
        self.blender_path = blender_path or self._find_blender()

    def _find_blender(self) -> Optional[str]:
        """
        Intenta encontrar Blender en el sistema.
        Tries to find Blender on the system.
        """
        # Ubicaciones comunes de Blender / Common Blender locations
        possible_paths = [
            'blender',  # PATH del sistema / System PATH
            '/usr/bin/blender',
            '/usr/local/bin/blender',
            'C:\\Program Files\\Blender Foundation\\Blender\\blender.exe',
            'C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe',
            'C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe',
        ]

        for path in possible_paths:
            try:
                result = subprocess.run([path, '--version'],
                                        capture_output=True,
                                        timeout=5,
                                        text=True)
                if result.returncode == 0:
                    return path
            except (subprocess.SubprocessError, FileNotFoundError):
                continue

        return None

    def generate_render_script(self, objects, output_path: str,
                               resolution: Tuple[int, int] = (1920, 1080),
                               samples: int = 128,
                               camera_distance: float = 5.0,
                               camera_angle: Tuple[float, float, float] = (60, 0, 45)) -> str:
        """
        Genera un script de Blender que incluye renderizado.
        Generates a Blender script that includes rendering.

        Args:
            objects: Objetos a renderizar / Objects to render
            output_path: Ruta donde guardar la imagen / Path to save the image
            resolution: Resolución (ancho, alto) / Resolution (width, height)
            samples: Número de muestras de renderizado / Number of render samples
            camera_distance: Distancia de la cámara / Camera distance
            camera_angle: Ángulos de la cámara (elevación, azimut, rotación) / Camera angles

        Returns:
            Script de Blender / Blender script
        """
        # Crear script base usando el exportador / Create base script using exporter
        exporter = BlenderExporter()
        if isinstance(objects, list):
            for obj in objects:
                exporter.add_object(obj)
        else:
            exporter.add_object(objects)

        base_script = exporter.generate_blender_script()

        # Añadir configuración de renderizado / Add rendering setup
        render_setup = f"""

# Configuración de renderizado / Render setup
import math

# Configurar motor de render / Set render engine
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = {samples}
bpy.context.scene.render.resolution_x = {resolution[0]}
bpy.context.scene.render.resolution_y = {resolution[1]}
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Configurar cámara / Setup camera
cam_distance = {camera_distance}
cam_elevation = math.radians({camera_angle[0]})
cam_azimuth = math.radians({camera_angle[1]})
cam_rotation = math.radians({camera_angle[2]})

# Eliminar cámara existente / Delete existing camera
if bpy.context.scene.camera:
    bpy.data.objects.remove(bpy.context.scene.camera, do_unlink=True)

# Crear nueva cámara / Create new camera
bpy.ops.object.camera_add()
camera = bpy.context.object
camera.name = 'RenderCamera'

# Posicionar cámara / Position camera
camera.location.x = cam_distance * math.cos(cam_elevation) * math.sin(cam_azimuth)
camera.location.y = -cam_distance * math.cos(cam_elevation) * math.cos(cam_azimuth)
camera.location.z = cam_distance * math.sin(cam_elevation)

# Apuntar cámara al origen / Point camera at origin
direction = -camera.location
rot_quat = direction.to_track_quat('-Z', 'Y')
camera.rotation_euler = rot_quat.to_euler()

# Establecer como cámara activa / Set as active camera
bpy.context.scene.camera = camera

# Configurar iluminación / Setup lighting
# Eliminar luces existentes / Delete existing lights
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# Luz principal / Main light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
main_light = bpy.context.object
main_light.data.energy = 3.0
main_light.rotation_euler = (math.radians(45), 0, math.radians(45))

# Luz de relleno / Fill light
bpy.ops.object.light_add(type='AREA', location=(-3, 3, 5))
fill_light = bpy.context.object
fill_light.data.energy = 500
fill_light.data.size = 5

# Luz trasera / Back light
bpy.ops.object.light_add(type='POINT', location=(0, 5, 3))
back_light = bpy.context.object
back_light.data.energy = 1000

# Configurar fondo / Setup background
world = bpy.data.worlds.get('World')
if world:
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (0.05, 0.05, 0.05, 1)  # Gris oscuro / Dark gray
    bg.inputs[1].default_value = 0.5  # Strength

# Añadir plano de suelo / Add ground plane
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -0.5))
ground = bpy.context.object
ground.name = 'Ground'
ground_mat = bpy.data.materials.new(name='GroundMaterial')
ground_mat.use_nodes = True
ground_mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1)
ground_mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.8
ground.data.materials.append(ground_mat)

# Renderizar / Render
output_path = r'{output_path}'
bpy.context.scene.render.filepath = output_path
bpy.ops.render.render(write_still=True)

print(f"Renderizado guardado en / Render saved to: {{output_path}}")
"""

        return base_script + render_setup

    def render(self, objects, output_path: str,
               resolution: Tuple[int, int] = (1920, 1080),
               samples: int = 128,
               camera_distance: float = 5.0,
               camera_angle: Tuple[float, float, float] = (60, 0, 45),
               save_blend: bool = True) -> bool:
        """
        Renderiza objetos y guarda la imagen.
        Renders objects and saves the image.

        Args:
            objects: Objetos a renderizar / Objects to render
            output_path: Ruta de salida para la imagen / Output path for the image
            resolution: Resolución (ancho, alto) / Resolution (width, height)
            samples: Muestras de renderizado / Render samples
            camera_distance: Distancia de cámara / Camera distance
            camera_angle: Ángulos de cámara / Camera angles
            save_blend: Guardar archivo .blend / Save .blend file

        Returns:
            True si tuvo éxito / True if successful
        """
        if not self.blender_path:
            raise RuntimeError(
                "Blender no encontrado. Instala Blender o proporciona la ruta.\n"
                "Blender not found. Install Blender or provide the path.")

        # Asegurar que el directorio de salida existe / Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generar script / Generate script
        script = self.generate_render_script(
            objects, output_path, resolution, samples,
            camera_distance, camera_angle
        )

        # Guardar script en archivo temporal / Save script to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            script_path = f.name
            f.write(script)

        # Opcionalmente guardar archivo blend / Optionally save blend file
        blend_path = None
        if save_blend:
            blend_path = output_path.rsplit('.', 1)[0] + '.blend'

        try:
            # Ejecutar Blender en segundo plano / Run Blender in background
            cmd = [
                self.blender_path,
                '--background',
                '--python', script_path
            ]

            if blend_path:
                cmd.extend(['--render-output', output_path])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # Tiempo de espera de 5 minutos / 5 minutes timeout
            )

            # Limpiar archivo de script / Clean up script file
            os.unlink(script_path)

            if result.returncode == 0:
                return True
            else:
                print(f"Error de renderizado / Render error:\n{result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("Timeout de renderizado / Render timeout")
            os.unlink(script_path)
            return False
        except Exception as e:
            print(f"Error: {e}")
            if os.path.exists(script_path):
                os.unlink(script_path)
            return False


def render_to_image(objects, output_path: str,
                    resolution: Tuple[int, int] = (1920, 1080),
                    samples: int = 128,
                    blender_path: Optional[str] = None) -> bool:
    """
    Función de conveniencia para renderizar objetos rápidamente.
    Convenience function to quickly render objects.

    Args:
        objects: Objeto(s) a renderizar / Object(s) to render
        output_path: Ruta de salida / Output path
        resolution: Resolución / Resolution
        samples: Muestras / Samples
        blender_path: Ruta a Blender / Path to Blender

    Returns:
        True si tuvo éxito / True if successful
    """
    renderer = BlenderRenderer(blender_path)
    return renderer.render(objects, output_path, resolution, samples)
