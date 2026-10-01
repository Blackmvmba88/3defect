# Pink Flight / Flight Lab

Prototipo local de vuelo infinito con el F-18 rosa del proyecto. El avión permanece en Z=0; ciudad, luces y obstáculos se desplazan hacia él.

## Abrir

```sh
npm install
npm run dev -- --port 5173
```

Visita http://127.0.0.1:5173. WASD o flechas para pilotar; P/Escape para pausa. En móvil, arrastra en la zona de vuelo. El sonido es opcional.

## Diseñar sin código

Abre **Flight Lab**. Puedes elegir cámaras o cambiar ángulo, elevación, distancia, campo de visión y punto de mira. También puedes ajustar velocidad/cantidad/color de luces, exposición, velocidad del escenario, separación y anchura de obstáculos. Los cambios se ven en directo; **Probar mi diseño** empieza una partida nueva con ellos.

Los ajustes y el récord se guardan en este navegador. **Guardar escena** exporta un JSON; **Abrir escena** lo recupera. **Capturar imagen** descarga una imagen de la escena sin la interfaz. El JSON guarda parámetros, no incluye el modelo: necesita este proyecto para reproducirse.

## Desarrollo

- `src/main.js`: escena Three.js, estado del juego, entradas y editor.
- `src/flight.js`: movimiento y colisiones con comprobación de cruce entre fotogramas.
- `src/settings.js`: valores por defecto y validación de proyectos.
- `public/models/f18-pink.glb`: modelo real, normalizado y agrupado por material.
- `export_aircraft.py`: regeneración del GLB desde el Blender rosa; solo genera la copia de juego.
- `npm test`: comprobaciones de colisiones, movimiento y validación de escenas.
- `npm run build`: compilación estática en `dist/`.

Los materiales del GLB son una adaptación PBR de los shaders de Blender. Es una base jugable con editor de parámetros; todavía no es un editor general de niveles ni incluye física aeronáutica. Las colisiones usan un volumen reducido de estilo arcade para que el vuelo sea tolerante.
