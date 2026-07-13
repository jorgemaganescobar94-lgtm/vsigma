# vSIGMA — instrucciones de trabajo

## Misión vigente

vSIGMA es un sistema de predicción deportiva auditable. Su objetivo es producir y evaluar probabilidades de fútbol con datos deportivos, sin apuestas ni recomendaciones financieras.

La autoridad específica para el Mundial está en `analysis/worldcup/AGENTS.md`. Las instrucciones más cercanas al archivo que se edita prevalecen sobre este documento.

## Alcance del repositorio

- `analysis/worldcup/**`: sistema vigente del Mundial. Aplican además sus instrucciones anidadas.
- `docs/**`: protocolos y documentación de gobierno.
- El resto del repositorio contiene automatizaciones y artefactos históricos, incluidos componentes con vocabulario de mercados. Son legado congelado: se pueden inspeccionar para diagnosticar, pero no ampliar, ejecutar ni convertir en objetivo del sistema salvo autorización expresa de Jorge para una tarea concreta.

La presencia histórica de campos como `market`, `odds`, `edge`, `stake` o `betting_permission` no autoriza su uso. No deben alimentar predicciones deportivas nuevas.

## Prohibiciones absolutas

- No consultar, integrar ni simular endpoints de apuestas o predicciones de terceros. En API-Football están prohibidos `/odds`, `/predictions` y variantes equivalentes.
- No generar apuestas, stakes, señales de ejecución, rentabilidad esperada ni consejos financieros.
- No mostrar, registrar, copiar ni versionar secretos. `.env`, claves de API y tokens quedan fuera de Git.
- No usar información posterior al instante de predicción. Toda evaluación debe respetar el bloqueo al saque inicial.
- No introducir datos de cuotas como variables, etiquetas auxiliares o criterios de selección.

## Autoridad y control de cambios

El código de la rama base actual prevalece sobre documentos antiguos. Antes de editar:

1. comprobar rama, `HEAD`, autor y archivos de los commits nuevos;
2. leer los documentos de estado y decisiones aplicables;
3. detenerse si hay conflicto, solapamiento inesperado, commit desconocido o necesidad de `force-push`.

Requieren aprobación expresa de Jorge antes de implementarse o activarse:

- cambios de modelo, probabilidades, calibración, features o fuentes;
- flags, gates, umbrales o criterios de promoción;
- workflows, horarios, cadencias, consumo de API o envíos a Telegram;
- secretos, permisos, producción o migraciones de datos.

La aprobación para investigar, documentar o abrir un PR no equivale a aprobación para activar producción.

## Forma de trabajo

- Usar una rama `agent/<descripcion>` y abrir PR en borrador; no escribir directamente en `main`.
- Hacer cambios pequeños, explícitos, reversibles por Git y, cuando aplique, por flag.
- Añadir al staging solo rutas concretas; nunca `git add .`.
- Ejecutar la verificación mínima válida y registrar exactamente qué se comprobó.
- Mantener los artefactos auxiliares en modo fail-safe: un fallo de informe no debe destruir predicciones, resultados ni aprendizaje.
- Separar siempre hechos verificados, inferencias, hipótesis y decisiones del supervisor.
- No declarar una mejora con datos in-sample. Exigir evaluación fuera de muestra, tamaño suficiente e incertidumbre reportada.

## Estado de fase

Durante el Mundial, el modelo publicado permanece congelado. Se permite liquidar resultados, vigilar calidad, documentar y preparar la auditoría final. Cualquier cambio predictivo queda para después del cierre y necesita evidencia más aprobación expresa.

## Entrega de una tarea

Informar:

1. archivos modificados;
2. comandos, tests o comprobaciones ejecutados;
3. resultado de validación y limitaciones;
4. efectos reales o ausencia de ellos en producción;
5. siguiente paso recomendado y si requiere aprobación.
