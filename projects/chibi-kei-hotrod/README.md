# Chibi Kei Hot-Rod

Misión de vehículo estilizado para `3defect`: microauto extremo, corto, ancho, bajo y con cabina alta. El proyecto se construye **silhouette-first**: primero proporciones y lectura visual, después detalle.

## Estado

**P0 — silueta paramétrica en progreso.**

Objetivos visuales principales:

- cabina alta y compacta;
- nariz casi inexistente;
- frente vertical;
- wheelbase corto;
- stance bajo;
- ruedas pequeñas y anchas;
- salpicaderas oversized;
- cola gruesa con mini spoiler;
- splitter delantero;
- lectura inmediata de micro hot-rod.

## Archivos

- `build_hotrod.py`: generador Blender.
- `verify_hotrod.py`: verificación de proporciones y geometría.
- `validation.json`: métricas y gates.
- `Chibi_Kei_Hotrod.blend`: escena editable generada.
- `Chibi_Kei_Hotrod.glb`: exportación del vehículo.
- `Chibi_Kei_Hotrod.png`: render de control.

## Regenerar

Desde la raíz del repo:

```sh
blender --background --python projects/chibi-kei-hotrod/build_hotrod.py
blender --background projects/chibi-kei-hotrod/Chibi_Kei_Hotrod.blend --python projects/chibi-kei-hotrod/verify_hotrod.py
```

## Parámetros P0

El generador expone proporciones principales al inicio del archivo:

- largo total;
- ancho;
- altura;
- wheelbase;
- diámetro y ancho de llanta;
- track;
- altura de cabina;
- altura al piso.

La meta de P0 es que el vehículo se reconozca **sin materiales ni detalles**.