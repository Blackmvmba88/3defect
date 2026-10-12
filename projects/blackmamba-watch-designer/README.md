# BlackMamba Watch Designer — MVP incremental

Estudio de diseño mecánico dentro de `3defect`; no es todavía un reloj funcional
ni una certificación de precisión o fabricabilidad.

## Ejecutar

Desde la raíz, con Python 3.11+ y `numpy` instalado:

```sh
python -m projects.blackmamba-watch-designer.demo --output watch-output
python -m pytest tests/test_watch_designer.py -q
blender --background --python watch-output/watch_blender.py
```

La demo genera geometría JSON, un script Blender y estados de simulación JSON.
Usa metros, segundos y radianes para la simulación. El modelo tiene una reducción
20 → 40 dientes; entrada 2 rad/s, salida −1 rad/s. El script Blender crea una
escena nueva y borra sus objetos actuales: ejecutar en una escena vacía.

## Arquitectura inspeccionada

- `defect3d/clock_mechanisms`: API pública `Gear`, `Spring`, `GearTrain`,
  `Pendulum`, `Escapement`. Antes: discos sin dientes, toros separados y relaciones
  basadas en orden de inserción. Ahora: perfil de evolvente extruido y alambre
  helicoidal continuo mediante `ClockMesh`, una subclase de `Shape3D` compatible
  con `CompositePart`, transformaciones, serialización y exportación Blender.
- `defect3d/physics/simulator.py`: integración traslacional de fuerzas. No hay
  restricciones de engrane ni dinámica rotacional; se conserva sin cambios.
  `GearTrain.simulate` añade cinemática ideal independiente y no mueve la malla.
- `defect3d/blender_integration/exporter.py`: exporta las mallas mediante
  `from_pydata`, conservando materiales y transformaciones. No añade contactos
  físicos ni animación; la cámara genérica requiere ajuste para escala reloj.
- `defect3d/evolutionary/__init__.py`: el optimizador genérico promediaba y mutaba
  atributos derivados sin reconstruirlos. `ClockOptimizer` ahora evalúa y devuelve
  diseños reconstruidos por el creador, con rango de longitud alrededor del período
  objetivo. Es una búsqueda de período ideal del péndulo, no de precisión real.
  El optimizador genérico sigue necesitando una futura revisión para otros dominios.
- `02_clock_mechanisms`: ejemplos existentes; se corrige torque inversamente
  proporcional a velocidad en el ejemplo físico y se retiran afirmaciones de
  precisión física no demostrada.

## Compatibilidad y convenciones

Se conservan constructores posicionales, clases públicas, `.part`, `to_dict`,
`Gear.gear_ratio`, `Spring.force/energy`, `total_ratio` y `output_speed`.
La nueva validación rechaza parámetros no finitos, negativos o dientes no enteros.
`volume()` devuelve ahora el volumen de la malla dentada muestreada sin eje.
Los hijos de `.part` cambian de primitivas a mallas: código que inspeccione sus
componentes internos debe adaptarse. Las claves JSON antiguas se mantienen y se
agregan presión, riesgo de socavado y conexiones.

`Gear.gear_ratio(other)` = dientes propios / dientes de other.
`total_ratio()` = magnitud entrada/salida para el último engranaje.
`output_speed()` conserva su convención de magnitud; `signed_output_speed()` y
`speed_factors()` incluyen inversión por cada engrane externo.
`connects_to` referencia un engranaje ya agregado; al omitirlo se conecta al
anterior, como en los ejemplos existentes. Se permiten ramas con una única raíz.
No se representan engranajes compuestos coaxiales, internos ni ciclos.
`mesh_validation(other)` comprueba módulo y ángulo de presión y devuelve la
separación nominal entre centros. No reposiciona piezas ni comprueba su contacto.

## Límites físicos

- Evolvente de engranajes rectos externos, presión predeterminada 20°, adendo m,
  dedendo 1.25m. El pie usa transición radial y arco, sin filete trocoidal,
  corrección de perfil, agujero, juego, tolerancias ni análisis de interferencia.
  `undercut_risk` señala dientes por debajo del umbral ideal de tallado sin
  corrección; no demuestra ausencia de socavado ni manufacturabilidad.
  No son perfiles cicloidales tradicionales de relojería.
- La hélice representa un resorte de alambre circular, no un resorte motor espiral
  de barrilete ni una espiral de volante. `coil_diameter` es diámetro medio;
  `free_length` mide la altura de la línea central, no la envolvente del alambre.
  Los extremos no están rectificados. `coil_overlap_risk` es una advertencia
  aproximada por paso; no reemplaza detección de autointersecciones.
  La rigidez es suministrada por el usuario; Hooke no incluye límite elástico,
  contacto de espiras, material, fatiga ni cargas máximas.
- Cinemática con velocidad impuesta, sin inercia, torque, pérdidas, colisiones,
  contacto de dientes ni transmisión resorte/escape. Las posiciones no se validan
  como ensamblaje. Los estados son relativos a ángulo cero, no a la fase visual.
- Péndulo y escape existentes son modelos ideales simplificados. El escape no
  regula esta simulación. No se afirma reserva de marcha ni desviación diaria.

## Verificación y pendientes

154 pruebas aprobadas, 8 omitidas por integración opcional Blender, en Python
3.11 y 3.14. Las 13 pruebas nuevas cubren topología cerrada, volumen orientado,
radios, validación, hélice fraccionaria, Hooke, ramas y signos, tiempo final exacto,
exportación, transformaciones, JSON y reconstrucción evolutiva. Exportación de la
demo ejecutada en Blender 5.2 LTS sin errores; avisa de futura obsolescencia de
`Material.use_nodes`. Se reparó el registro de módulo de la prueba existente del
resorte para permitir su carga con dataclasses.

Siguientes incrementos: ensamblaje y fases automáticos, tren compuesto coaxial,
contactos y juego, perfiles de reloj y filetes reales, barrilete y espiral de
volante, dinámica con escape y disipación, animación Blender, ensayos materiales,
metrología y contraste con prototipo físico. Sin estos ensayos no hay validación
de precisión o fabricación.
