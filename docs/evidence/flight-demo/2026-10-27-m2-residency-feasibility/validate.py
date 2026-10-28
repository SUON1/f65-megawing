#!/usr/bin/env python3
"""Read-only design/accounting validation; never builds or executes a bank."""
import copy
import io
import re
import tarfile
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BASE = "af3b0913c4b73eb6b8add638fb88bdbbae158036"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def conditional_budget_gate(adopted, source_complete, costs, stack, service):
    # Necessary budget precondition only, never executable admission.
    # None is unknown, never a zero-cost estimate or permission to dispatch.
    return (
        adopted is True
        and source_complete is True
        and type(costs) is list
        and len(costs) > 0
        and all(type(value) is int and value >= 0 for value in costs)
        and sum(costs) <= 1836
        and stack is True
        and service is True
    )


ACCOUNTING_KEYS = {
    'baseline',
    'contract_revision',
    'cpu_alias',
    'derived_estimates',
    'effective',
    'finalized_contract',
    'founder_disposition',
    'git_inputs',
    'historical_incomplete_packet',
    'identity',
    'informing_drafts',
    'main_push_ci',
    'new_resident_data_minimum',
    'original_checkout_before',
    'placement_exception',
    'prior_checkpoint',
    'proposed_physical_ranges',
    'prototype_admitted',
    'publication_record',
    'published_record',
    'reference',
    'reference_bodies',
    'schema',
    'signature',
    'unpriced_other_terms',
    'unpriced_resident_terms',
}
UNRESOLVED_IDENTITIES_SHA256 = '523020a2703af4cf9dfbb00397dbb1fb844338dfb160584be87cde2d2394b84d'

def strict_json(raw):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique_pairs)


def disjoint(a, b):
    return a[1] <= b[0] or b[1] <= a[0]


def required_flags(value, true_names=(), false_names=()):
    require(type(value) is dict, "expected contract object")
    for name in true_names:
        require(value.get(name) is True, "required true flag: " + name)
    for name in false_names:
        require(value.get(name) is False, "required false flag: " + name)


def validate_finalization(data):
    require(set(data) == ACCOUNTING_KEYS, "accounting schema fields")
    require(data["schema"] == "65AERO-M2-RESIDENCY-FEASIBILITY-ACCOUNTING-3",
            "accounting schema identity")
    require(type(data["contract_revision"]) is int and data["contract_revision"] == 3,
            "contract revision")
    required_flags(data, false_names=("effective", "prototype_admitted"))
    direction = data["founder_disposition"]
    require(set(direction) == {"scope", "decisions", "design_exception_approved",
            "actual_placement_admitted", "permanent_architecture_allocation",
            "production_memory_map_changed", "public_abi_changed",
            "banked_runtime_admitted"}, "disposition schema")
    require(direction["scope"] == "approved versioned M2 development design and publication only",
            "approved direction scope")
    require(direction["decisions"] == {name: "APPROVED_DEVELOPMENT_DESIGN_ONLY"
            for name in ("RF-D1", "RF-D2", "RF-D3", "RF-EX1")},
            "founder development-design approval")
    required_flags(direction, true_names=("design_exception_approved",),
        false_names=("actual_placement_admitted", "permanent_architecture_allocation",
            "production_memory_map_changed", "public_abi_changed", "banked_runtime_admitted"))
    exception = data["placement_exception"]
    require(exception["id"] == "RF-EX1" and exception["status"] ==
            "APPROVED_DEVELOPMENT_DESIGN_ONLY", "placement review boundary")
    required_flags(exception, false_names=("effective",))
    require(exception["current_architecture_placement"] ==
            "EXPLICIT_DEVELOPMENT_EXCEPTION;PRODUCTION_OWNERSHIP_UNCHANGED", "hidden authority conflict")
    require(exception["implementation_of_exception"] == "NOT_IMPLEMENTED;SEPARATE_AUTHORIZATION_REQUIRED",
            "placement implementation must stop")

    contract = data["finalized_contract"]
    require(set(contract) == {"range_notation", "run_bank", "exclusions",
        "resource_parent", "protected_proof_sublocations", "boot_leases",
        "gateway", "future_engine", "source_baseline"}, "contract schema")
    nested_fields = {
        "run_bank": "range_ref owner loader_mapper lifetime capacity_bytes runtime_writers",
        "exclusions": "simulation audio_state_and_queues display_controls shared_scratch display_a display_b graphics_assets resource_outside_boot_lease protected_reserve color_ram rom_backup",
        "protected_proof_sublocations": "audio_cache dma_lists proof_reserved",
        "boot_leases": "owner landing_range_ref staging_range_ref exclusive normal_operation_blocked_until_verified_retirement landing_full_zero_and_readback_bytes staging_released_after_run_identity_and_landing_retirement staging_release_is_not_a_wipe failure runtime_reload",
        "gateway": "non_reentrant max_body_quanta_per_invocation signature_reads_per_invocation near_spans_checked_before_mapping verification_owner verify_after_selection_before_branch previous_verification_authorizes_next_call unreadable_unprovable_mapping_refuses_admission nested_call irq_masked_through_restore nmi canonical_restore_before_public_return_yield_or_clock stack_bounds_require_actual_whole_program_proof all_eight_service_slots_require_nonzero_proven_bounds",
        "future_engine": "profile_only full_graphics_workspace_bytes_after_proposed_bank shared_owner_borrowing permanent_resource_lease banking_as_public_engine_service m3_m4_and_full_profile_require_new_combined_ledger_and_service_admission simulation_hz stages reserve_use",
        "source_baseline": "status must_be_source_complete_under_git old_packet_required separate_increment_from_banking failing_resident_fit_may_be_retained runtime_enablement_permitted prototype_before_baseline_and_reviewed_contract_integration",
    }
    for name, fields in nested_fields.items():
        require(type(contract[name]) is dict and set(contract[name]) == set(fields.split()),
                "nested contract schema: " + name)
    ranges = data["proposed_physical_ranges"]
    expected = {
        "graphics_code_bank": [0x48000, 0x4A000],
        "remaining_graphics_workspace": [0x4A000, 0x50000],
        "boot_landing": [0x8000, 0xA000], "boot_staging": [0x50000, 0x52000],
        "resident": [0x2001, 0x8000], "hardware_stack": [0x100, 0x200],
        "base_page": [0x200, 0x300], "software_stack": [0xC000, 0xD000],
        "protected_reserve": [0x58000, 0x60000],
        "rom_backup": [0x8000000, 0x8020000],
    }
    require(ranges == expected, "exact proposed range changed")
    require(data["cpu_alias"] == [0x8000, 0xA000], "execution alias changed")

    main_text = (ROOT / "spec/core/F65_Main_Concept_v1.7_HUMAN_APPROVED.md").read_text()
    table = main_text.split("#### A. General fast chip RAM", 1)[1].split(
        "#### B. VIC-IV Color RAM", 1)[0]
    parent = {}
    for first, last in re.findall(r"\$([0-9A-F]{6})-\$([0-9A-F]{6})", table):
        parent[int(first, 16)] = int(last, 16) + 1
    parent_starts = {
        "simulation": 0x10000, "audio_state_and_queues": 0x18000,
        "display_controls": 0x1C000, "shared_scratch": 0x1D000,
        "display_a": 0x20000, "display_b": 0x30000,
        "graphics_assets": 0x40000, "protected_reserve": 0x58000,
    }
    excluded = contract["exclusions"]
    require(set(excluded) == set(parent_starts) | {
        "resource_outside_boot_lease", "color_ram", "rom_backup"}, "exclusion schema")
    for name, start in parent_starts.items():
        require(excluded[name] == [start, parent[start]], "parent exclusion: " + name)
    require(contract["resource_parent"] == [0x50000, parent[0x50000]],
            "ResourceManager parent changed")
    require(excluded["resource_outside_boot_lease"] ==
            [ranges["boot_staging"][1], parent[0x50000]], "resource exclusion changed")
    require(excluded["color_ram"] == [0xFF80000, 0xFF88000], "Color RAM exclusion")
    require(excluded["rom_backup"] == ranges["rom_backup"], "backup exclusion")
    for name, span in excluded.items():
        require(disjoint(span, ranges["graphics_code_bank"]), "bank borrows " + name)
        require(disjoint(span, ranges["boot_staging"]), "staging borrows " + name)
    require(parent[0x48000] == 0x50000 and
            ranges["graphics_code_bank"][0] == 0x48000, "parent workspace boundary")
    # This overlap is approved development design only, never an active allocation.
    require(not disjoint([0x48000, parent[0x48000]], ranges["graphics_code_bank"]),
            "workspace authority conflict unexpectedly absent")

    registry = strict_json((ROOT / "interfaces/f65_platform_abi.json5").read_text())
    proof = registry["r0c_admitted_proof_contracts"][0]["memory"]["prohibited"][:3]
    names = ["audio_cache", "dma_lists", "proof_reserved"]
    for name, row in zip(names, proof):
        match = re.search(r"0x([0-9a-f]+)-0x([0-9a-f]+)", row)
        span = [int(match[1], 16), int(match[2], 16) + 1]
        require(contract["protected_proof_sublocations"][name] == span,
                "proof exclusion changed: " + name)
        require(disjoint(span, ranges["boot_staging"]), "boot overlaps " + name)

    bank = contract["run_bank"]
    require(bank["range_ref"] == "graphics_code_bank" and bank["owner"] == "Graphics"
            and bank["loader_mapper"] == "protected CoreRuntime/Platform only"
            and bank["capacity_bytes"] == 8192, "code owner/capacity")
    require(bank["lifetime"] ==
            "reserved from boot load through reset; immutable after READY; quarantined on failure",
            "bank lifetime")
    required_flags(bank, false_names=("runtime_writers",))
    boot = contract["boot_leases"]
    require(boot["owner"] == "ResourceManager load-time lease; Platform sole executor",
            "boot loader/lease ownership")
    required_flags(boot, true_names=("exclusive",
        "normal_operation_blocked_until_verified_retirement",
        "staging_released_after_run_identity_and_landing_retirement",
        "staging_release_is_not_a_wipe"), false_names=("runtime_reload",))
    require(boot["landing_range_ref"] == "boot_landing" and
            boot["staging_range_ref"] == "boot_staging" and
            boot["landing_full_zero_and_readback_bytes"] == 8192, "boot lease retirement")
    require(boot["failure"] ==
            "READY false; quarantine leases/bank; reset-only terminal lockout",
            "boot failure ownership")
    gateway = contract["gateway"]
    required_flags(gateway, true_names=("non_reentrant", "near_spans_checked_before_mapping",
        "verify_after_selection_before_branch", "unreadable_unprovable_mapping_refuses_admission",
        "irq_masked_through_restore", "canonical_restore_before_public_return_yield_or_clock",
        "stack_bounds_require_actual_whole_program_proof",
        "all_eight_service_slots_require_nonzero_proven_bounds"),
        false_names=("previous_verification_authorizes_next_call",))
    require(gateway["max_body_quanta_per_invocation"] == 1 and
            gateway["signature_reads_per_invocation"] == 16 and
            gateway["verification_owner"] == "protected Platform gateway", "gateway scope")
    require(gateway["nested_call"] ==
            "resident terminal sink; retain outer ownership; no normal return",
            "nested bank return")
    require(gateway["nmi"] ==
            "fixed resident handler; no C/MAP/bank/DMA; sticky interference; prove all races",
            "NMI ownership")
    future = contract["future_engine"]
    required_flags(future, true_names=("profile_only",
        "m3_m4_and_full_profile_require_new_combined_ledger_and_service_admission"),
        false_names=("shared_owner_borrowing", "permanent_resource_lease",
                     "banking_as_public_engine_service"))
    require(future["full_graphics_workspace_bytes_after_proposed_bank"] == 24576
            and future["simulation_hz"] == 100 and future["stages"] == 21
            and future["reserve_use"] == 0, "future engine budgets")
    source = contract["source_baseline"]
    require(source["status"] == "NOT_ESTABLISHED_ON_MAIN", "source baseline promoted")
    required_flags(source, true_names=("must_be_source_complete_under_git",
        "separate_increment_from_banking", "failing_resident_fit_may_be_retained"),
        false_names=("old_packet_required", "runtime_enablement_permitted",
                     "prototype_before_baseline_and_reviewed_contract_integration"))
    resident_terms = {
        "gateway_entry_and_per_invocation_signature_text", "typed_wrappers_and_trampolines",
        "normal_restoration_text", "boot_loader_copy_crc_text",
        "additional_fault_recovery_lockout_text", "constants_beyond_minimum_data",
        "padding_compiler_scratch_and_codegen_delta", "unavoidable_hot_cold_duplication",
    }
    other_terms = {
        "bank_entry_return_thunks_alignment_and_codegen_delta", "additional_hardware_stack",
        "additional_software_stack", "eight_dispatch_slot_bounds", "begin_commit_and_guard_bounds",
    }
    for key, names in [("unpriced_resident_terms", resident_terms),
                       ("unpriced_other_terms", other_terms)]:
        require(type(data[key]) is dict and set(data[key]) == names,
                "missing/unknown cost category: " + key)
        require(all(value is None for value in data[key].values()),
                "unreviewed measured/estimated cost: " + key)
    require(type(gateway["max_body_quanta_per_invocation"]) is int,
            "body quantum must be an integer count")
    budget = data["derived_estimates"]
    require([budget[k] for k in ("selected_text", "gross_headroom",
        "new_data_minimum", "remaining_overhead_allowance")] == [4374, 2199, 363, 1836],
        "frozen feasibility estimates changed")
    historical = data["historical_incomplete_packet"]
    require(historical["members"] == 37 and historical["previously_verified"] == 22
            and historical["not_verified_recoverable"] == 15 and
            historical["git_worktree_tier_unverified"] == 8, "historical scope")
    require(historical["inventory_sha256"] ==
            "1e932efe541468afce20081b9654186b457c458b24d70df992a6c911b2233447",
            "original inventory identity")
    required_flags(historical, false_names=("adopted", "recovery_performed_this_task"))
    rows = historical["unresolved_members"]
    require(len(rows) == 15 and len({r["path"] for r in rows}) == 15,
            "unresolved member count")
    for row in rows:
        require(set(row) == {"path", "sealed_sha256", "status"} and
                re.fullmatch("[0-9a-f]{64}", row["sealed_sha256"]) and row["status"] ==
                "NOT VERIFIED RECOVERABLE; no new recovery attempted", "unresolved record")
    retained = [[r["path"], r["sealed_sha256"]] for r in rows]
    require(sha(json.dumps(retained, separators=(",", ":")).encode()) ==
            UNRESOLVED_IDENTITIES_SHA256, "original unresolved identities changed")


def verify_prior_checkpoint(data):
    prior = data["prior_checkpoint"]
    archive = (HERE / prior["archive"]).read_bytes()
    require(sha(archive) == prior["archive_sha256"] ==
            "1e7aded9b572be45a4809b770261cdfa19e173c34463c91d9a288c6fbdd4a2cb",
            "prior archive identity")
    require(sha((HERE / "validation.json").read_bytes()) ==
            prior["original_validation_sha256"] ==
            "b37a3f1ad9a8d536b7a7bddeb101975b34c3ea59762cf2b63f4fd192d1fe1906",
            "original validation modified")
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as packet:
        members = packet.getmembers()
        by_name = {m.name: m for m in members}
        require(len(members) == len(by_name) == prior["members"] == 5,
                "prior member set")
        prefix = "docs/evidence/flight-demo/2026-10-27-m2-residency-feasibility/"
        record = packet.extractfile(by_name[prefix + "validation.json"]).read()
        require(sha(record) == prior["original_validation_sha256"], "archived result identity")
        originals = strict_json(record)["checkpoint_files"]
        require(set(by_name) == set(originals) | {prefix + "validation.json"},
                "unexpected prior member")
        for name, identity in originals.items():
            raw = packet.extractfile(by_name[name]).read()
            require(len(raw) == identity["bytes"] and sha(raw) == identity["sha256"],
                    "prior checkpoint member: " + name)
    return 5


def finalization_negative_cases(data):
    cases = [
        (["schema"], "UNREVIEWED"),
        (["unpriced_resident_terms"], {}),
        (["unpriced_other_terms"], {}),
        (["finalized_contract", "gateway", "max_body_quanta_per_invocation"], True),
        (["unapproved_field"], True),
        (["effective"], True),
        (["founder_disposition", "actual_placement_admitted"], True),
        (["founder_disposition", "design_exception_approved"], False),
        (["founder_disposition", "public_abi_changed"], True),
        (["placement_exception", "effective"], True),
        (["placement_exception", "current_architecture_placement"], "PASS"),
        (["proposed_physical_ranges", "graphics_code_bank"], [0x10000, 0x12000]),
        (["cpu_alias"], [0x8000, 0xC000]),
        (["finalized_contract", "gateway", "previous_verification_authorizes_next_call"], True),
        (["finalized_contract", "gateway", "non_reentrant"], False),
        (["finalized_contract", "gateway", "unreadable_unprovable_mapping_refuses_admission"], False),
        (["finalized_contract", "boot_leases", "landing_full_zero_and_readback_bytes"], 8191),
        (["finalized_contract", "boot_leases", "staging_released_after_run_identity_and_landing_retirement"], False),
        (["finalized_contract", "future_engine", "banking_as_public_engine_service"], True),
        (["finalized_contract", "source_baseline", "runtime_enablement_permitted"], True),
        (["finalized_contract", "source_baseline", "old_packet_required"], True),
        (["derived_estimates", "remaining_overhead_allowance"], 1837),
    ]
    for path, value in cases:
        invalid = copy.deepcopy(data)
        target = invalid
        for component in path[:-1]:
            target = target[component]
        target[path[-1]] = value
        try:
            validate_finalization(invalid)
        except (ValueError, KeyError, TypeError):
            continue
        raise ValueError("contract negative case accepted: " + "/".join(path))
    return len(cases)


def verify_publication_approval(data):
    publication = strict_json((HERE / data["publication_record"]).read_text())
    require(publication["approved_decisions"] == ["RF-D1", "RF-D2", "RF-D3", "RF-EX1"],
            "founder publication approval scope")
    status = publication["target_status"]
    require(all(status[key] == "UNPROVEN" for key in
                ("actual_fit", "stack", "gateway", "service")), "target proof promoted")
    required_flags(status, false_names=("banking_implemented", "runtime_admitted"))
    require(status["reserve_used"] == 0, "publication reserve use")
    require(publication["budget_estimates"] == {
        "proposed_code_removal": 4374, "projected_headroom": 2199,
        "minimum_additional_data": 363, "remaining_overhead_allowance": 1836},
        "approved budget changed")
    prior = (HERE / "finalization-validation.json").read_bytes()
    require(sha(prior) == publication["reviewed_result_sha256"] ==
            "e2080820650866510b9bd7ae50de699c261d3f5bf5ea7c8b96b045190927c31d",
            "reviewed result identity changed")
    snapshot = publication["reviewed_archive"]
    raw = (HERE / snapshot["file"]).read_bytes()
    require(len(raw) == snapshot["bytes"] and sha(raw) == snapshot["sha256"] ==
            "de7b83806f538522f3a29c21053680abaef83cdbd4d2d9ddad4696c474d4d038",
            "reviewed revision archive changed")
    originals = strict_json(prior)["checkpoint_files"]
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as packet:
        expected = {
            "WORK_IN_PROGRESS.md",
            "docs/plans/65AERO_M2_RESIDENCY_FEASIBILITY.md",
            str((HERE / "accounting.json").relative_to(ROOT)),
            str((HERE / "validate.py").relative_to(ROOT)),
        }
        require(len(packet.getmembers()) == snapshot["members"] == 4 and
                {m.name for m in packet.getmembers()} == expected,
                "reviewed revision member set")
        for name in expected:
            body = packet.extractfile(name).read()
            require(len(body) == originals[name]["bytes"] and
                    sha(body) == originals[name]["sha256"], "reviewed bytes: " + name)
        name = "docs/plans/65AERO_M2_RESIDENCY_FEASIBILITY.md"
        before = packet.extractfile(name).read().decode()
        after = (ROOT / name).read_text()
        def operational_clauses(text):
            return text.split("## RF-CODE-1", 1)[1].split(
                "## One reconciled feasibility calculation", 1)[0]
        require(operational_clauses(before) == operational_clauses(after),
                "reviewed operational contracts changed during publication")
        def budget_clauses(text):
            return text.split("## One reconciled feasibility calculation", 1)[1].split(
                "**Feasibility:", 1)[0]
        require(budget_clauses(before) == budget_clauses(after),
                "reviewed budget changed during publication")
    require((ROOT / "WORK_IN_PROGRESS.md").read_text().startswith(
        "# Work in Progress\n\n- **Status: NONE"), "publication WIP must be NONE")
    return 4


def main():
    data = strict_json((HERE / "accounting.json").read_text())
    validate_finalization(data)
    prior_members = verify_prior_checkpoint(data)
    reviewed_members = verify_publication_approval(data)
    contract_negatives = finalization_negative_cases(data)
    require(data["baseline"] == BASE, "wrong baseline")
    head = subprocess.check_output(
        ["git", "--no-optional-locks", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    ancestry = subprocess.run(
        ["git", "--no-optional-locks", "merge-base", "--is-ancestor", BASE, head],
        cwd=ROOT, check=False
    )
    require(ancestry.returncode == 0, "unverified baseline ancestry")
    allowed = {
        "WORK_IN_PROGRESS.md",
        "CURRENT_STATE.md",
        "docs/plans/65AERO_M2_RESIDENCY_FEASIBILITY.md",
        *[str((HERE / name).relative_to(ROOT)) for name in
          ["accounting.json", "validate.py", "validation.json",
           "checkpoint-before-conditional.tar.gz", "finalization-validation.json",
           "reviewed-revision-2.tar.gz", "publication.json"]],
    }
    changed = subprocess.check_output(
        ["git", "--no-optional-locks", "diff", "--name-only", BASE],
        cwd=ROOT, text=True
    ).splitlines()
    untracked = subprocess.check_output(
        ["git", "--no-optional-locks", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT, text=True
    ).splitlines()
    require(set(changed + untracked) <= allowed, "baseline changed beyond this checkpoint")
    for name, expected in data["git_inputs"].items():
        blob = subprocess.check_output(
            ["git", "--no-optional-locks", "show", BASE + ":" + name], cwd=ROOT
        )
        require(sha(blob) == expected, "Git input identity: " + name)
        require(sha((ROOT / name).read_bytes()) == expected, "modified input: " + name)

    manifest = strict_json((ROOT / "spec/manifests/spec-corpus.json").read_text())
    present = [d for d in manifest["documents"] if d["present"]]
    for doc in present:
        require(sha((ROOT / doc["relative_path"]).read_bytes()) == doc["sha256"],
                "authority identity: " + doc["document_key"])

    reference = data["reference"]
    published = strict_json((ROOT / data["published_record"]).read_text())
    old = published["retained_development_evidence"]
    for key in ["prg_sha256", "resident_bytes", "resident_limit", "deficit_bytes",
                "compiler_scratch_bytes", "hardware_stack_bytes",
                "software_stack_bytes", "trap_stack_bytes", "reserve_bytes"]:
        require(reference[key] == old[key], "reference mismatch: " + key)

    removed = sum(data["reference_bodies"].values())
    minimum = sum(data["new_resident_data_minimum"].values())
    resident = reference["resident_bytes"]
    limit = reference["resident_limit"]
    calculated = {
        "selected_text": removed,
        "reference_deficit": resident - limit,
        "resident_after_reference_removal": resident - removed,
        "gross_headroom": limit - (resident - removed),
        "new_data_minimum": minimum,
        "resident_with_minimum_data": resident - removed + minimum,
        "remaining_overhead_allowance": limit - (resident - removed + minimum),
        "bank_with_header_minimum": removed + data["signature"]["bytes"],
        "bank_remaining_before_other_costs": 8192 - removed - data["signature"]["bytes"],
        "if_2199_were_removal_deficit": resident - 2199 + minimum - limit,
        "boot_component_union_maximum": (0xA000 - 0x2001) + 8192 + 8192,
        "runtime_resident_bank_envelopes": (0x8000 - 0x2001) + 8192,
    }
    require(calculated == data["derived_estimates"], "arithmetic mismatch")
    allocations = data["proposed_physical_ranges"]
    for label, span in allocations.items():
        require(0 <= span[0] < span[1], "invalid span: " + label)
    spans = list(allocations.items())
    for i, (left, a) in enumerate(spans):
        for right, b in spans[i + 1:]:
            require(a[1] <= b[0] or b[1] <= a[0], "overlap: " + left + "/" + right)
    require(allocations["resident"] == [0x2001, 0x8000], "resident ceiling")
    require(allocations["protected_reserve"] == [0x58000, 0x60000], "reserve changed")
    require(reference["reserve_bytes"] == 0, "reserve use")
    require(data["signature"] == {
        "bytes": 16, "format": "ASCII 65M2RUN2 + expected_build_id[0:8]",
        "owner": "protected Platform gateway", "every_invocation": True,
        "after_selection_before_execution": True, "cached_authorization": False,
        "failure": "no bank execution; canonical restoration; sticky fault and reset lockout",
        "negative_cases_required_not_executed": [
            "missing", "incorrect", "unreadable", "changed_between_successive_calls"]
    }, "per-invocation verification contract weakened")
    costs = list(data["unpriced_resident_terms"].values())
    require(all(c is None for c in costs), "unreviewed new cost estimate")
    require(data["effective"] is False and data["prototype_admitted"] is False,
            "unapproved adoption/admission")
    negatives = [
        (False, True, [0], True, True),  # Missing architectural adoption.
        (True, False, [0], True, True),  # Missing source-complete identity.
        (True, True, [None], True, True),
        (True, True, [1837], True, True),
        (True, True, [0], False, True),
        (True, True, [0], True, False),
        (True, True, [-1], True, True),
        (True, True, [], True, True),
        (True, True, [True], True, True),
    ]
    require(all(not conditional_budget_gate(*case) for case in negatives),
            "prototype gate fails open")
    require(conditional_budget_gate(True, True, [1836], True, True),
            "cost-boundary rule inconsistent")
    require(not conditional_budget_gate(False, False, costs, False, False),
            "current state incorrectly admitted")
    result = {
        "static_validation": "PASS",
        "identity": data["identity"],
        "baseline": BASE,
        "head": head,
        "branch": subprocess.check_output(
            ["git", "--no-optional-locks", "branch", "--show-current"],
            cwd=ROOT, text=True).strip(),
        "pinned_git_inputs": len(data["git_inputs"]),
        "manifest_documents_verified": len(present),
        "arithmetic": calculated,
        "fail_closed_negative_cases": len(negatives),
        "signature_cases": "specified only; target/host bank calls NOT RUN",
        "founder_direction": "APPROVED_RF_D1_D2_D3_RF_EX1_DEVELOPMENT_DESIGN",
        "placement_exception": "RF-EX1_APPROVED_DEVELOPMENT_DESIGN_ONLY",
        "contract_adoption": "APPROVED_DESIGN;NO_ACTIVE_ALLOCATION",
        "contract_revision": data["contract_revision"],
        "schema_contract_negative_cases": contract_negatives,
        "prior_checkpoint_members_verified": prior_members,
        "reviewed_revision_members_verified": reviewed_members,
        "unresolved_historical_members_recorded": 15,
        "complete_budget": "UNPROVEN",
        "prototype_admission": "NOT_ADMITTED",
        "actual_fit": "UNPROVEN",
        "stack": "UNPROVEN",
        "gateway": "UNPROVEN",
        "service": "UNPROVEN",
        "target_fit": "NOT_BUILT",
        "changed_stack_map_service": "UNPROVEN",
        "xemu": "NOT_RUN",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
