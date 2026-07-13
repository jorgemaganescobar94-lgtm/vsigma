# vSIGMA Mundial — instrucciones estrictas

Estas reglas aplican a todo `analysis/worldcup/**` y prevalecen sobre las instrucciones de la raíz cuando sean más específicas.

## Objetivo único

Construir, operar y evaluar predicciones deportivas propias del Mundial: 1X2, goles, marcadores, estadísticas de equipo, eventos de jugadores y simulación del torneo. No es un sistema de apuestas.

## Fuentes permitidas y prohibidas

Se permiten datos deportivos necesarios para el modelo, como estado de suscripción, fixtures, equipos, selecciones, plantillas, jugadores, clasificaciones, alineaciones, lesiones, estadísticas y eventos.

Quedan prohibidos, sin excepción:

- API-Football `/odds`, `/predictions` y cualquier endpoint equivalente;
- cuotas, consenso de mercado, tips o probabilidades externas como feature, benchmark de selección o salida;
- stakes, edge económico, ROI, P&L o recomendaciones de apuesta.

Si una función compartida puede alcanzar un endpoint prohibido, no ejecutarla hasta demostrar por lectura o test que la ruta concreta no lo hace.

## Integridad temporal

- `fixture_id` es la clave principal de unión cuando exista.
- Una predicción evaluable debe quedar congelada al saque inicial. Después del KO no se reescribe ni se sustituye por una versión posterior.
- Registrar por separado predicciones matinales y últimas predicciones pre-KO; no mezclarlas en comparaciones homogéneas.
- Nunca usar resultado, alineación confirmada tardía, evento o estadística posterior al timestamp de la predicción.
- Los backtests deben ser walk-forward u otra separación temporal verificable. Cualquier riesgo de leakage bloquea la conclusión.

## Fase Mundial: producción congelada

Hasta completar la final y la auditoría pre-registrada:

- no cambiar fórmulas, pesos, calibración, features, jerarquía de modelos ni probabilidades publicadas;
- no cambiar flags, gates, cron, workflows, consumo de API ni formato/envío de Telegram;
- sí se permite `settle`, scorecards, vigilancia, reconciliación de datos, documentación y correcciones puramente mecánicas que no alteren predicciones, siempre con aprobación cuando afecten producción.

El protocolo vinculante de cierre está en `docs/WORLD_CUP_FINAL_EVALUATION_PROTOCOL.md`.

## Aprendizaje y comparación

- Comparar modelos solo en el mismo conjunto de partidos y con la misma semántica temporal.
- Métrica primaria 1X2: log-loss. Reportar también Brier, ECE, accuracy, N y cobertura.
- Toda diferencia entre candidatos debe incluir bootstrap pareado e IC95%; si el intervalo incluye cero, el resultado es inconcluso.
- Estadísticas de equipo y props se evalúan por familia; una mejora en una métrica no gradúa las demás.
- Una señal de clubes transferida a selecciones no se considera validada sin evidencia específica. El análisis histórico conocido de club-form → selecciones fue nulo.
- Auto-refit solo puede conservarse bajo sus gates existentes, reproducibilidad y límites de movimiento; un PASS no autoriza nuevos gates ni cambios manuales.

## Operación segura

- Ejecutar el pipeline manual o despachar un workflow puede consumir API y enviar Telegram real: requiere autorización explícita.
- Consultar `/status` para diagnosticar el plan es admisible; minimizar llamadas y no imprimir la clave.
- `Persist` y cualquier guardado crítico deben ejecutarse de forma segura incluso si falla un componente auxiliar.
- No borrar históricos ni snapshots congelados. Ante duplicados o schemas cambiantes, parar y reconciliar antes de continuar.
- Añadir al staging únicamente rutas explícitas; nunca secretos ni `.env`.

## Verificación

Para cambios locales que no tengan efectos externos, usar la prueba más estrecha posible. La suite de referencia es:

```powershell
.\.venv\Scripts\python.exe -m pytest analysis/worldcup -q
```

En otros entornos, usar el Python aislado equivalente. Documentar tests no ejecutables y la razón; no sustituir evidencia por una afirmación.

## Salida obligatoria

Cada entrega debe indicar si cambió alguna predicción oficial. Si la respuesta no es un `NO` verificable, detener la entrega hasta obtener aprobación expresa de Jorge.
