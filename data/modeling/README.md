# vSIGMA Hybrid ML Transition

Objetivo: convertir vSIGMA en un sistema híbrido.

- vSIGMA actual genera features inteligentes: mercado, XI, estilo, roles, player impact, unit index.
- El modelo estadístico aprende pesos con histórico API.
- El modo sombra compara ML vs vSIGMA sin sustituirlo.
- Solo se promociona si mejora métricas frente al baseline.

## 1) Construir dataset histórico API

Ejemplo con varias ligas/temporadas:

```powershell
python scripts/build_vsigma_historical_dataset.py `
  --league-season 39:2025 `
  --league-season 140:2025 `
  --league-season 135:2025 `
  --out data/modeling/vsigma_historical_dataset.csv `
  --window 5 `
  --include-odds `
  --sleep 0.2
```

Para prueba rápida:

```powershell
python scripts/build_vsigma_historical_dataset.py --league-season 39:2025 --max-fixtures 200 --out data/modeling/vsigma_historical_dataset.csv --window 5 --sleep 0.2
```

## 2) Entrenar modelo estadístico

```powershell
python scripts/train_vsigma_stat_models.py `
  --dataset data/modeling/vsigma_historical_dataset.csv `
  --model-out data/modeling/models/vsigma_stat_model.json `
  --metrics-out data/modeling/models/vsigma_stat_model_metrics.json
```

El modelo queda en modo sombra salvo que supere métricas mínimas.

## 3) Aplicar modelo en modo sombra a un forecast ad hoc

Primero debe existir el forecast vSIGMA normal.

```powershell
python scripts/apply_vsigma_ml_shadow_forecast.py `
  --date 2026-06-11 `
  --home "Mexico" `
  --away "South Africa" `
  --model data/modeling/models/vsigma_stat_model.json
```

Salida:

```text
data/processed/today/<fecha>/vsigma_ml_shadow_forecast_<slug>.md
```

## Política de promoción

No sustituir vSIGMA hasta que el modelo supere al baseline en:

- Log loss 1X2
- Brier score
- Accuracy como referencia secundaria
- Error medio de goles/xG
- Error medio de tiros/corners cuando haya cobertura estadística suficiente

Si no mejora, sigue como segunda opinión.
