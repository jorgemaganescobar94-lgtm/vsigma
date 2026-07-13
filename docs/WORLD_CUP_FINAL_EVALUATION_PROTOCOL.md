# Protocolo pre-registrado de evaluación final — Mundial 2026

**Versión:** 1.0  
**Fecha de pre-registro:** 2026-07-13, antes de la final  
**Ámbito:** predicciones ya emitidas y congeladas por vSIGMA Mundial  
**Propietario de decisión:** Jorge  

## 1. Propósito

Cerrar el Mundial con una auditoría reproducible, sin hindsight y sin cambiar el modelo durante la competición. El informe final medirá qué funcionó, qué no y qué queda inconcluso; no promocionará automáticamente ningún componente.

Este protocolo no modifica probabilidades, flags, gates, workflows, API, cron ni Telegram.

## 2. Congelación y unidad de análisis

- La unidad primaria es `fixture_id` con resultado final confirmado.
- Solo entran predicciones creadas antes del saque inicial y conservadas sin sobrescritura.
- Se conservará el snapshot final de entradas, salidas, timestamps, versión/commit y checksums.
- Correcciones posteriores solo podrán arreglar metadatos demostrablemente mecánicos. No podrán cambiar una probabilidad histórica.
- Si falta trazabilidad temporal, la fila se etiqueta y excluye de comparaciones causales; puede aparecer en un anexo descriptivo.

## 3. Cohortes fijadas de antemano

El informe presentará, como mínimo:

1. todos los partidos válidos, como resumen descriptivo;
2. predicción matinal;
3. última predicción pre-KO;
4. cruces A/B solo en partidos comunes a ambos modelos y con la misma semántica temporal;
5. fases del torneo, únicamente como desglose secundario y sin elegir cortes por el resultado observado.

Las cohortes matinal y pre-KO no se agruparán para declarar un ganador. Se informarán N, exclusiones y motivo de cada exclusión.

## 4. Candidatos fijados

Se evaluarán únicamente las variantes que ya tengan predicciones congeladas y trazables:

- L3 de referencia;
- modelo full-data L1;
- ensemble conservador;
- variante de matchup total, si existe en muestra común;
- ajustes de contexto, solo frente a su base en muestra común;
- cada familia de estadísticas de equipo y props por separado.

No se reconstruirá retrospectivamente una predicción que no quedó registrada.

## 5. Métricas fijadas

### 1X2

- principal: log-loss multiclase, menor es mejor;
- secundarias: Brier multiclase, ECE, accuracy y cobertura;
- siempre: N, baseline usado y skill frente a ese baseline.

### Goles y marcador

- log-loss de BTTS y Over/Under cuando exista probabilidad congelada;
- MAE y sesgo de goles esperados/totales;
- cobertura del marcador exacto como descriptivo, no como criterio único.

### Estadísticas de equipo

- MAE, RMSE, sesgo y cobertura de intervalos por familia;
- local y visitante por separado cuando la muestra lo permita.

### Props de jugadores

- log-loss, Brier, ECE y cobertura por familia: gol, asistencia, tarjeta y tiros;
- ninguna familia hereda la conclusión de otra.

## 6. Incertidumbre y comparaciones

- Las diferencias entre modelos se calcularán de forma pareada sobre los mismos partidos.
- Se usarán 10.000 remuestras bootstrap por `fixture_id`, semilla fija `20260713`, e IC95% percentil.
- Se publicará el signo de la diferencia con la convención explícita de cada métrica.
- Si el IC95% incluye cero, la conclusión será `INCONCLUSA`, aunque la media sea favorable.
- Una muestra pequeña se informará como evidencia exploratoria, no como validación.
- No se crearán umbrales, cohortes o métricas después de ver el resultado para favorecer una variante.

## 7. Reglas de decisión

Cada componente recibirá una sola etiqueta:

- `RETENER`: evidencia favorable y coherente, con trazabilidad completa;
- `RETENER_EN_SOMBRA`: señal prometedora pero incertidumbre o N insuficiente;
- `SIN_EVIDENCIA`: diferencia inconclusa o cobertura insuficiente;
- `RETIRAR`: degradación consistente o fallo de integridad;
- `NO_EVALUABLE`: no existe muestra común o trazabilidad suficiente.

La etiqueta no cambia producción. Promover, retirar o recalibrar requiere una propuesta posterior, validación fuera de muestra cuando corresponda y aprobación expresa de Jorge.

## 8. Procedimiento después de la final

1. Esperar resultados finales oficiales y ejecutar una única liquidación controlada.
2. Verificar que cada fixture se liquidó una vez y que las predicciones pre-KO no cambiaron.
3. Congelar snapshot, commit, timestamps, schemas y checksums.
4. Ejecutar scorecards por cohorte y las comparaciones pareadas fijadas.
5. Generar tablas de exclusiones, cobertura e incertidumbre.
6. Redactar `analysis/worldcup/WORLD_CUP_FINAL_AUDIT_2026.md` con resultados reproducibles.
7. Revisar contradicciones entre informe, CSV y logs.
8. Presentar conclusiones a Jorge. No activar ningún cambio en esa misma entrega.

## 9. Contenido mínimo del informe final

- commit y fecha de corte;
- inventario de archivos y checksums;
- diagrama breve de procedencia de datos;
- N total y N por cohorte/modelo/familia;
- tabla completa de exclusiones;
- métricas puntuales e IC95%;
- comparaciones pareadas;
- sensibilidad separando matinal y pre-KO;
- incidentes y limitaciones;
- etiquetas de decisión de la sección 7;
- lista explícita de propuestas que necesitarían autorización.

## 10. Guardarraíles

- Cero endpoints de apuestas o predicciones externas.
- Cero datos de cuotas.
- Cero edición retrospectiva de probabilidades.
- Cero activación automática derivada del informe.
- Cero secretos en logs, artefactos o Git.
- Si una comprobación de integridad falla, se detiene la conclusión afectada y se documenta el bloqueo.
