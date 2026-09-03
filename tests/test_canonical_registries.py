import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "registries" / name).read_text(encoding="utf-8"))


def test_project_registry_has_exactly_six_canonical_projects() -> None:
    projects = load("project_registry.json")["projects"]
    assert {item["project_id"] for item in projects} == {
        "ecosystem-predictor",
        "core-predictor",
        "predictor-ops",
        "brasileirao-predictor",
        "cripto-predictor",
        "stocks-predictor",
    }


def test_required_claims_exist_and_business_claim_stays_b0() -> None:
    claims = {item["claim_id"]: item for item in load("evidence_registry.json")["claims"]}
    required = {
        "CLAIM-CORE-FOUNDATION",
        "CLAIM-OPS-INTEGRITY",
        "CLAIM-BR-MARKET-H24",
        "CLAIM-BR-MARKET-H6",
        "CLAIM-BR-MARKET-H1",
        "CLAIM-BR-MARKET-PIT",
        "CLAIM-BR-FEATURE-PIT",
        "CLAIM-CR-HMM",
        "CLAIM-CR-LLM",
        "CLAIM-CR-H6",
        "CLAIM-CR-COSTS",
        "CLAIM-ST-FACTOR-FAMILIES",
        "CLAIM-ST-PIT",
        "CLAIM-ST-SURVIVORSHIP",
        "CLAIM-ST-VENDOR",
        "CLAIM-BIZ-001",
        "CLAIM-ECON-001",
        "CLAIM-ECON-001A",
        "CLAIM-ECON-001B",
        "CLAIM-ECON-001C",
        "CLAIM-ECON-001D",
        "CLAIM-ECON-001E",
        "CLAIM-ECON-001F",
    }
    assert required <= claims.keys()
    assert claims["CLAIM-BIZ-001"]["state"] == "B0"
    assert claims["CLAIM-CR-H6"]["state"] == "INCONCLUSIVE"


def test_br_preservation_is_granular_and_not_false_pass() -> None:
    backup = load("backup_registry.json")
    br = backup["br_preservation"]
    assert br["matches_db"] == "PASS"
    assert br["prediction_store"] == "MISSING_CONFIRMED"
    assert br["overall"] == "PARTIAL"
    assert backup["v0_offsite_backup"] == "PARTIAL"


def test_exp001_remains_fail_closed() -> None:
    checkpoints = load("canonical_checkpoints.json")
    assert checkpoints["EXP001_DATA_STATUS"] == "PARTIALLY_READY"
    assert checkpoints["EXP001_HISTORICAL_READY"] == "NO"
    assert checkpoints["EXP001_EXECUTION"] == "NOT_STARTED"
    assert checkpoints["BR_RESEARCH_DECISION"] == "UNKNOWN"
    assert checkpoints["EXP001_HISTORICAL"] == "NOT_VIABLE"


def test_exp001_prospective_contract_is_active_and_complete() -> None:
    contract = json.loads(
        (ROOT / "canonical_contracts" / "exp001_prospective.json").read_text(encoding="utf-8")
    )
    assert contract["state"] == "ACTIVE"
    assert {"dataset_version", "probabilities"} <= set(contract["required_fields"])


def test_commercial_discovery_starts_with_real_names_but_no_claim_promotion() -> None:
    registry = load("commercial_discovery.json")
    assert registry["claim_state"] == "B0"
    assert len(registry["contacts"]) >= 10
    assert len({item["contact_id"] for item in registry["contacts"]}) == len(registry["contacts"])
    assert {item["ICP"] for item in registry["contacts"]} <= {"ICP-1", "ICP-2"}
    assert registry["gates"]["BIZ-001_10_NOMINAL_CONTACTS"] == "YES"
    assert registry["v1"]["outreach"] == "READY_FOR_HUMAN_EXECUTION"
    assert registry["outreach_001"]["selected_contact_id"] == "ICP2-001"
    assert registry["outreach_001"]["status"] == "READY_FOR_HUMAN_EXECUTION"
    assert registry["outreach_001"]["sent_at"] is None
    assert registry["interview_001"]["status"] == "NOT_STARTED"
    assert registry["interview_001"]["evidence_source"] is None
    assert len(registry["evidence_capture_template"]["subclaims"]) == 6
    assert registry["follow_up_rule"]["maximum_follow_ups"] == 1
    assert all(item["status"] == "RESEARCHED_NOT_CONTACTED" for item in registry["contacts"])


def test_economics_stays_e0_without_fabricated_revenue_or_margin() -> None:
    registry = load("economics_registry.json")
    assert registry["claim_state"] == "E0"
    assert registry["actuals"]["revenue"] == 0
    assert registry["actuals"]["paid_engagements"] == 0
    assert registry["unit_economics"] == "UNKNOWN"
    assert registry["profitability"] == "UNKNOWN"
    assert registry["pricing_framework"]["market_price"] == "UNKNOWN"
    assert registry["primary_next_action"] == "HUMAN_OPERATOR_SEND_OUTREACH_001"


def test_harness_alignment_does_not_equate_core_versions() -> None:
    registry = load("harness_registry.json")
    statuses = {
        (item["repo"], item["reported_core_version"]): item["status"] for item in registry["harnesses"]
    }
    assert statuses[("brasileirao-predictor", "3.1.0")] == "ALIGNED"
    assert statuses[("cripto-predictor", "3.0.0")] == "COMPATIBLE_BUT_OLDER"
    assert registry["overall_alignment"] == "COMPATIBLE_BUT_OLDER"
