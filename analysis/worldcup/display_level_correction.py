"""
WORLD CUP 2026 — DISPLAY-ONLY LEVEL-CORRECTION REVERSIBLE SKELETON (Fase 4P). READ-ONLY by default ·
NO API · NO scraping · NO web · NO market/odds/betting · NO fabrication · NO secrets · NO external
sources. Pure football. ALL FLAGS OFF -> NOTHING is applied: every corrected output equals the original
byte-for-byte (exact reversibility). No weights, no base prediction, no Telegram are ever touched here.

This module is the PREPARED, INERT machinery for a FUTURE display-only correction of the over/under-
predicted team SOT / shots / corners levels. It does not decide policy: a later, explicitly-approved
(🔴) phase would flip a flag in display_level_correction_config.json. Until then it is a safe no-op.

PURE FUNCTIONS (no side effects, fully testable):
  load_display_correction_config()                         -> config dict (safe default if absent)
  config_status(config)                                    -> "all_disabled" / "some_enabled"
  should_apply_display_correction(module, readiness, cfg)  -> (bool, reason)
  apply_display_level_correction(value, module, profile, cfg, readiness) -> result dict
  apply_sot_display_correction / apply_shots_display_correction / apply_corners_display_correction
  check_activation_allowed(module, readiness, cfg)         -> (bool, reason)   [non-raising]
  assert_display_correction_activation_allowed(...)        -> True or raises   [fail-closed guard]

SAFE FALLBACKS (always -> NO correction, original value, clear reason):
  missing config · global enabled False · module enabled False · requires_readiness and not READY ·
  missing readiness · missing/insufficient correction profile · non-numeric value.

Run (diagnostic, modifies nothing):  python analysis/worldcup/display_level_correction.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import evaluate_worldcup_team_sot_level_correction as lc  # thresholds (single source of truth)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CONFIG_PATH = HERE / "display_level_correction_config.json"
READINESS_JSON = HERE / "worldcup_display_correction_readiness.json"

MODULES = ("team_sot", "team_shots", "team_corners")
SUPPORTED_MODES = ("global_ratio", "global_bias", "pre_fixture_ratio")
N_MIN_ACTIVATE = lc.N_MIN_ACTIVATE
READY_STATUS = "READY_FOR_PROPOSAL"

# the readiness gate names modules with a team_*_display_correction key; map to this module's short keys
READINESS_KEY = {"team_sot": "team_sot_display_correction",
                 "team_shots": "team_shots_display_correction",
                 "team_corners": "team_corners_display_correction"}

# safe default config: everything OFF
SAFE_DEFAULT_CONFIG = {"enabled": False, "modules": {m: {"enabled": False, "mode": "global_ratio",
                                                         "requires_readiness": True} for m in MODULES}}


class DisplayCorrectionActivationError(RuntimeError):
    """Raised by the fail-closed activation guard when activation is NOT allowed."""


# ===================================================================== config
def load_display_correction_config(path=CONFIG_PATH):
    """Load the config; on any problem return the safe all-OFF default (fail-closed)."""
    p = Path(path)
    if not p.exists():
        return dict(SAFE_DEFAULT_CONFIG)
    try:
        cfg = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return dict(SAFE_DEFAULT_CONFIG)
    if not isinstance(cfg, dict):
        return dict(SAFE_DEFAULT_CONFIG)
    cfg.setdefault("enabled", False)
    cfg.setdefault("modules", {})
    return cfg


def _module_cfg(config, module_name):
    return (config.get("modules") or {}).get(module_name) or {}


def config_status(config):
    """'all_disabled' if global OFF and every module OFF; else 'some_enabled'."""
    if config.get("enabled"):
        return "some_enabled"
    for m in MODULES:
        if _module_cfg(config, m).get("enabled"):
            return "some_enabled"
    return "all_disabled"


# ===================================================================== readiness lookup
def _readiness_record(readiness_summary, module_name):
    """Find the per-module record in a Fase-4O readiness summary. Returns dict or None."""
    if not isinstance(readiness_summary, dict):
        return None
    key = READINESS_KEY.get(module_name, module_name)
    for m in (readiness_summary.get("modules") or []):
        if m.get("module") in (key, module_name):
            return m
    return None


def _is_ready(readiness_summary, module_name):
    rec = _readiness_record(readiness_summary, module_name)
    return bool(rec and rec.get("readiness_status") == READY_STATUS)


# ===================================================================== apply gate
def should_apply_display_correction(module_name, readiness_summary, config):
    """(bool, reason). True only if global enabled AND module enabled AND (readiness not required OR the
    module is READY_FOR_PROPOSAL). Fail-closed on anything missing."""
    if not config or not config.get("enabled"):
        return False, "config global enabled=false -> no se aplica."
    mcfg = _module_cfg(config, module_name)
    if not mcfg or not mcfg.get("enabled"):
        return False, f"módulo {module_name} enabled=false -> no se aplica."
    if mcfg.get("requires_readiness", True):
        if readiness_summary is None:
            return False, "requires_readiness=true y no hay readiness -> no se aplica."
        if not _is_ready(readiness_summary, module_name):
            rec = _readiness_record(readiness_summary, module_name)
            st = (rec or {}).get("readiness_status", "desconocido")
            return False, f"readiness={st} != {READY_STATUS} -> no se aplica."
    return True, "config+readiness OK -> se aplicaría."


# ===================================================================== apply correction
def _coerce(value):
    try:
        if value is None or value == "":
            return None
        f = float(value)
    except (TypeError, ValueError):
        return None
    return f if (f == f and f not in (float("inf"), float("-inf"))) else None


def _result(original, display, applied, mode, reason, dq, conf):
    return {"original_value": original, "display_value": display, "correction_applied": applied,
            "correction_mode": mode, "correction_reason": reason, "data_quality": dq, "confidence": conf}


def _profile_param(profile, mode):
    """Pull the parameter for a mode from the correction profile. Returns (param, ok)."""
    if not isinstance(profile, dict):
        return None, False
    if mode == "global_ratio":
        v = profile.get("global_ratio", profile.get("ratio"))
    elif mode == "global_bias":
        v = profile.get("global_bias", profile.get("bias"))
    elif mode == "pre_fixture_ratio":
        v = profile.get("pre_fixture_ratio")
    else:
        return None, False
    v = _coerce(v)
    return v, (v is not None)


def apply_display_level_correction(value, module_name, correction_profile, config,
                                   readiness_summary=None):
    """Return the display value for one team-stat level value. With flags OFF (current state) this is
    EXACTLY the original (correction_applied=false, mode='disabled'). NEVER mutates the original; always
    returns both original_value and display_value. Fail-closed everywhere."""
    original = _coerce(value)
    if original is None:
        return _result(value, value, False, "disabled", "valor no numérico -> original sin tocar.",
                       "no_data", "baja")

    should, reason = should_apply_display_correction(module_name, readiness_summary, config)
    if not should:
        # exact reversibility: display == original
        return _result(original, original, False, "disabled", reason, "evaluable", "baja")

    mode = _module_cfg(config, module_name).get("mode", "global_ratio")
    if mode not in SUPPORTED_MODES:
        return _result(original, original, False, "fallback_unsupported_mode",
                       f"modo '{mode}' no soportado -> fallback original.", "evaluable", "baja")

    param, ok = _profile_param(correction_profile, mode)
    if not ok:
        return _result(original, original, False, "fallback_no_profile",
                       f"sin parámetro para modo '{mode}' -> fallback original.", "no_data", "baja")

    if mode in ("global_ratio", "pre_fixture_ratio"):
        display = max(0.0, original * param)
    else:  # global_bias
        display = max(0.0, original - param)

    return _result(original, display, True, mode,
                   f"corrección display '{mode}' aplicada (param={round(param, 4)}).",
                   "evaluable", "media")


def apply_sot_display_correction(value, correction_profile, config, readiness_summary=None):
    return apply_display_level_correction(value, "team_sot", correction_profile, config, readiness_summary)


def apply_shots_display_correction(value, correction_profile, config, readiness_summary=None):
    return apply_display_level_correction(value, "team_shots", correction_profile, config, readiness_summary)


def apply_corners_display_correction(value, correction_profile, config, readiness_summary=None):
    return apply_display_level_correction(value, "team_corners", correction_profile, config, readiness_summary)


# ===================================================================== activation guard (fail-closed)
def check_activation_allowed(module_name, readiness_summary, config):
    """(allowed: bool, reason). Non-raising. Activation requires the global proposal gate, the module's
    READY_FOR_PROPOSAL status, n>=50, anti-look-ahead, no strong bias inversion, and present delta
    metrics. Fail-closed on anything missing."""
    if not isinstance(readiness_summary, dict):
        return False, "sin readiness summary -> bloqueado."
    if not readiness_summary.get("should_propose_activation_any", False):
        return False, "should_propose_activation_any=false -> bloqueado (gate global)."
    rec = _readiness_record(readiness_summary, module_name)
    if not rec:
        return False, f"sin registro de readiness para {module_name} -> bloqueado."
    if rec.get("readiness_status") != READY_STATUS:
        return False, f"readiness_status={rec.get('readiness_status')} != {READY_STATUS} -> bloqueado."
    if (rec.get("n") or 0) < N_MIN_ACTIVATE:
        return False, f"n={rec.get('n')} < {N_MIN_ACTIVATE} -> bloqueado."
    gates = rec.get("gates") or {}
    if not gates.get("anti_lookahead_available", False):
        return False, "sin anti-look-ahead -> bloqueado."
    if not gates.get("no_strong_bias_inversion_gate", True):
        return False, "inversión fuerte de sesgo -> bloqueado."
    if rec.get("delta_mae_pre_fixture") is None:
        return False, "faltan métricas delta_mae/delta_rmse -> bloqueado."
    return True, "todas las condiciones de activación OK (sigue siendo 🔴: requiere aprobación explícita)."


def assert_display_correction_activation_allowed(module_name, readiness_summary, config):
    """Fail-closed guard: returns True if activation is allowed, otherwise raises
    DisplayCorrectionActivationError with the blocking reason."""
    allowed, reason = check_activation_allowed(module_name, readiness_summary, config)
    if not allowed:
        raise DisplayCorrectionActivationError(f"[{module_name}] {reason}")
    return True


# ===================================================================== diagnostic --check (no writes)
def _load_readiness(path=READINESS_JSON):
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def run_check(config_path=CONFIG_PATH, readiness_path=READINESS_JSON):
    """Print the inert state. Modifies NOTHING. Returns a dict (also used by tests)."""
    config = load_display_correction_config(config_path)
    readiness = _load_readiness(readiness_path)
    status = config_status(config)
    print("=== display-level correction skeleton — DIAGNOSTIC (--check) ===")
    print(f"config loaded: {config_path.name if hasattr(config_path, 'name') else config_path}")
    print(f"global enabled: {bool(config.get('enabled'))}  (config_status={status})")
    per_module = {}
    for m in MODULES:
        mcfg = _module_cfg(config, m)
        rec = _readiness_record(readiness, m)
        rstat = (rec or {}).get("readiness_status", "NO_READINESS")
        allowed, _reason = check_activation_allowed(m, readiness, config)
        per_module[m] = {"enabled": bool(mcfg.get("enabled")), "mode": mcfg.get("mode"),
                         "requires_readiness": mcfg.get("requires_readiness", True),
                         "readiness_status": rstat, "activation_allowed": allowed}
        print(f"  {m:14} enabled={bool(mcfg.get('enabled'))!s:5} mode={str(mcfg.get('mode')):13} "
              f"readiness={rstat:20} activation_allowed={allowed}")
    any_allowed = any(v["activation_allowed"] for v in per_module.values())
    print(f"NO ACTIVATION: nada se aplica (global+módulos OFF). any_activation_allowed={any_allowed}")
    print("Reversibilidad exacta: con flags OFF, display_value == original_value siempre.")
    return {"config_status": status, "global_enabled": bool(config.get("enabled")),
            "modules": per_module, "any_activation_allowed": any_allowed}


def main(argv=None):
    ap = argparse.ArgumentParser(description="World Cup display-level correction skeleton (Fase 4P).")
    ap.add_argument("--check", action="store_true", help="print inert state; modifies nothing")
    a = ap.parse_args(argv)
    if a.check:
        run_check()
    else:
        cfg = load_display_correction_config()
        print(f"display-level correction skeleton: config_status={config_status(cfg)} "
              f"(global enabled={bool(cfg.get('enabled'))}). Use --check for the full diagnostic.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
