"""Read-only RF-EX2 design validation. Never runs target tools or admits a bank."""
import ast
import bisect
import copy
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "docs/evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections/target-1793167696482111000"
BASE = "b20f91cb8023ea02e33d5fec6870026023bd8fbf"
EDITED = ["WORK_IN_PROGRESS.md", "docs/plans/65AERO_M2_BANKED_RENDERER_BUILD_INTENT.md",
          "docs/plans/65AERO_M2_RESIDENCY_FEASIBILITY.md"]
BANK = "m2_transform sine multiply_rotation m2_multiply_q46 m2_project_prepared to_camera plane_distance interpolate_delta project_axis rounded_ratio __udivdi3".split()
RESIDENT = "m2_camera_valid m2_point_valid __modhi3 __umodhi3 __mulsi3 memcpy __memset".split()
UNKNOWN = "gateway_signature typed_wrappers canonical_restore loader_crc_retirement fault_terminal context_continuation alignment_duplication compiler_scratch_delta".split()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, "duplicate JSON key")
            value[key] = item
        return value
    return json.loads(path.read_text(), object_pairs_hook=pairs)


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def linked_graph():
    symbols = {}
    for line in (TARGET / "UNADMITTED.symbols").read_text().splitlines():
        fields = line.split()
        if len(fields) == 4 and fields[2] in ("t", "T", "w", "W") and int(fields[1], 16):
            symbols[fields[3]] = {"address": int(fields[0], 16), "bytes": int(fields[1], 16)}
    ordered = sorted((record["address"], name) for name, record in symbols.items())
    starts = [address for address, name in ordered]
    by_start = {record["address"]: name for name, record in symbols.items()}
    edges = {name: set() for name in symbols}
    unresolved = []
    for line in (TARGET / "UNADMITTED.disassembly").read_text().splitlines():
        match = re.match(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+\s*(jsr|jmp)\s+(.*)$", line)
        if not match:
            continue
        address = int(match[1], 16)
        index = bisect.bisect_right(starts, address) - 1
        if index < 0:
            continue
        owner = ordered[index][1]
        record = symbols[owner]
        if address >= record["address"] + record["bytes"]:
            continue
        target = re.match(r"\$([0-9a-f]+)\b", match[3])
        if not target:
            unresolved.append(owner)
            continue
        destination = int(target[1], 16)
        if record["address"] <= destination < record["address"] + record["bytes"]:
            continue
        if destination not in by_start:
            unresolved.append(owner)
            continue
        edges[owner].add(by_start[destination])
    pending = ["m2_transform", "m2_project_prepared"]
    closure = set()
    while pending:
        name = pending.pop()
        if name not in closure:
            closure.add(name)
            pending.extend(edges[name] - closure)
    require(not set(unresolved) & (closure | {"crc_byte", "cfphysical_crc"}),
            "unresolved direct/indirect closure edge")
    return symbols, edges, closure


def intersection(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))


def validate_contract(data):
    require(set(data) == {"schema", "identity", "base", "reference", "relocation", "crc",
            "ranges", "ownership", "reuse", "gateway", "budget", "workspace", "decision",
            "inputs", "reviewed_preservation", "evidence_tier"}, "accounting schema fields")
    require(data["schema"] == 1 and type(data["schema"]) is int, "schema version")
    require(data["identity"] == "65AERO-M2-RF-EX2-P2-1" and data["base"] == BASE, "identity/base")
    require(data["evidence_tier"] == "DOCUMENTATION_STATIC_DESIGN_ONLY", "evidence tier")
    require(data["reference"] == {"resident": 32839, "ceiling": 24575, "deficit": 8264,
            "scratch": 190, "reserve": 0}, "reference accounting")
    spans = data["ranges"]
    require(spans == {"bank": [0x48000, 0x4c000], "window": [0x8000, 0xc000],
        "workspace": [0x4c000, 0x50000], "landing": [0x8000, 0xc000],
        "staging": [0x50000, 0x54000], "audio_cache": [0x53000, 0x56000],
        "software_stack": [0xc000, 0xd000], "reserve": [0x58000, 0x60000]}, "exact ranges")
    require(intersection(spans["staging"], spans["audio_cache"]) == 4096, "audio overlap")
    for a, b in [("window", "software_stack"), ("bank", "workspace"),
                 ("bank", "reserve"), ("staging", "reserve")]:
        require(intersection(spans[a], spans[b]) == 0, "forbidden overlap")
    owner = data["ownership"]
    require(owner == {"status": "BLOCKED BY MEMORY OWNERSHIP", "staging_owner": "ResourceManager",
        "conflicting_owner": "Audio", "overlap": [0x53000, 0x54000],
        "exclusive_pre_audio_lease_proven": False, "exception_approved": False,
        "inherited_quiescence_proven": False, "active_allocation": False}, "ownership disposition")
    require(all(value is True for value in data["reuse"].values()) and set(data["reuse"]) == {
        "post_successful_platform_init", "before_first_tick", "no_pending_rom_work",
        "no_runtime_restore_reload", "failure_terminal_until_reset", "no_handler_user",
        "descriptor_disjoint", "new_resident_placement_required", "existing_255_stays_charged"}, "reuse lifetime")
    require(data["gateway"] == {"owner": "Platform", "signature_reads_per_call": 16,
        "verify_after_selection_before_entry": True, "cached_authorization": False,
        "missing_wrong_changed_unreadable_fail_closed": True, "canonical_restore": True,
        "restore_uncertain_terminal": True, "non_reentrant": True, "nested_lockout": True,
        "irq_nmi_costs_required": True, "all_eight_slots_required": True}, "gateway contract")
    budget = data["budget"]
    require(budget == {"optimistic_removed": 8625, "gross_allowance": 361,
        "distinct_new_data": 363, "distinct_resident": 24577, "distinct_margin": -2,
        "conditional_new_data": 108, "conditional_resident": 24322,
        "conditional_pre_overhead_allowance": 253, "unknown_resident_cost_upper_bounds": dict.fromkeys(UNKNOWN),
        "final_resident_allowance": None, "additional_hardware_stack": None,
        "additional_software_stack": None, "service_cycle_bounds": None,
        "whole_program_stack": "UNPROVEN", "complete_fit": "UNPROVEN"}, "conservative cost accounting")
    require(data["workspace"] == {"current_physical_arena_demand": 0, "arena_capacity": 16384,
        "renderer_resident_bytes": 676, "future_continuation_bytes": None}, "workspace accounting")
    require(data["decision"] == "REJECT OPTION A", "decision must reject blocked/unbounded candidate")


def regressions(data):
    mutations = [
        ("unknown_is_not_zero", lambda x: x["budget"]["unknown_resident_cost_upper_bounds"].update(gateway_signature=0)),
        ("no_final_253_claim", lambda x: x["budget"].update(final_resident_allowance=253)),
        ("no_staging_exclusivity_claim", lambda x: x["ownership"].update(exclusive_pre_audio_lease_proven=True)),
        ("no_silent_exception", lambda x: x["ownership"].update(exception_approved=True)),
        ("no_reserve_use", lambda x: x["reference"].update(reserve=1)),
        ("no_stack_overlap", lambda x: x["ranges"].update(window=[0x8000, 0xc001])),
        ("no_cached_signature", lambda x: x["gateway"].update(cached_authorization=True)),
        ("every_call_reads_signature", lambda x: x["gateway"].update(signature_reads_per_call=0)),
        ("verification_before_entry", lambda x: x["gateway"].update(verify_after_selection_before_entry=False)),
        ("signature_faults_close", lambda x: x["gateway"].update(missing_wrong_changed_unreadable_fail_closed=False)),
        ("no_unsafe_reuse", lambda x: x["reuse"].update(no_pending_rom_work=False)),
        ("descriptor_cannot_alias", lambda x: x["reuse"].update(descriptor_disjoint=False)),
        ("no_double_buffer_credit", lambda x: x["reuse"].update(existing_255_stays_charged=False)),
        ("no_assumed_stack", lambda x: x["budget"].update(additional_software_stack=0)),
        ("no_guessed_timing", lambda x: x["budget"].update(service_cycle_bounds=[1]*8)),
        ("no_prototype_permission", lambda x: x.update(decision="PROCEED TO PROTOTYPE DESIGN REVIEW")),
    ]
    for name, mutate in mutations:
        altered = copy.deepcopy(data)
        mutate(altered)
        try:
            validate_contract(altered)
        except ValueError:
            continue
        raise ValueError("mutation accepted: " + name)
    return [name for name, mutate in mutations]


def main():
    data = load(HERE / "accounting.json")
    validate_contract(data)
    for name, expected in data["inputs"].items():
        require(sha(ROOT / name) == expected, "source/artifact changed: " + name)
    symbols, edges, closure = linked_graph()
    require(closure == set(BANK + RESIDENT), "closure membership")
    relocation = data["relocation"]
    require(relocation["bank_candidates"] == {n: symbols[n] for n in BANK}, "bank itemization")
    require(relocation["resident_closure"] == {n: symbols[n] for n in RESIDENT}, "resident itemization")
    require(relocation["edges"] == {n: sorted(edges[n]) for n in sorted(closure)}, "closure edges")
    require(sum(symbols[n]["bytes"] for n in closure) == 9736, "closure total")
    require(sum(symbols[n]["bytes"] for n in BANK) == 8625, "removal total")
    require(sum(symbols[n]["bytes"] for n in RESIDENT) == 1111, "retained total")
    require(data["crc"] == {"symbol": "crc_byte", "address": 0x77f1, "bytes": 84,
        "direct_callers": ["cfphysical_crc"], "resident_chain": ["m1_platform_begin", "cfrom_begin", "cfphysical_crc", "crc_byte"],
        "relocatable_credit": 0, "resident_copy_required": True,
        "bank_duplicate_if_added_bytes": 84, "budget_delta": 0}, "CRC classification")
    require(symbols["crc_byte"] == {"address": 0x77f1, "bytes": 84}, "CRC symbols")
    mapping = (TARGET / "UNADMITTED.map").read_text()
    require(re.search(r"^\s*77f1\s+77f1\s+54\s+1\s+crc_byte$", mapping, re.M), "CRC map")
    require(sorted(n for n, targets in edges.items() if "crc_byte" in targets) == ["cfphysical_crc"], "CRC caller")
    for caller, target in zip(data["crc"]["resident_chain"], data["crc"]["resident_chain"][1:]):
        require(target in edges[caller], "CRC resident call path")
    require("crc_byte" not in closure, "CRC not removable")
    require(32839-8625 == 24214 and 24214+363 == 24577 and 24214+108 == 24322, "resident arithmetic")
    require(24575-24322 == 253 and 16384-8625-16 == 7743, "allowance arithmetic")
    require(8192-16 < 8264, "8 KiB capacity")
    # Derive address arithmetic only; this does not execute MAP or prove bus reads.
    require(((0x34 & 15) << 16) == 0x40000 and (0x34 >> 4) == 3, "MAP encoding")
    require([a+0x40000 for a in [0x8000,0x9fff,0xa000,0xbfff]] == [0x48000,0x49fff,0x4a000,0x4bfff], "MAP endpoints")
    registry = load(ROOT / "interfaces/f65_platform_abi.json5")
    require("0x053000-0x055fff audio cache" in registry["r0c_admitted_proof_contracts"][0]["memory"]["prohibited"], "audio reservation")
    excluded = [[0x10000,0x18000], [0x18000,0x1c000], [0x1c000,0x20000],
        [0x20000,0x40000], [0x40000,0x48000], [0x56000,0x57000],
        [0x57000,0x58000], [0x58000,0x60000], [0xff80000,0xff88000],
        [0x8000000,0x8020000], [0x100,0x200], [0x200,0x300], [0x1900,0x2000],
        [0xc000,0xd000]]
    for span in excluded:
        require(intersection(data["ranges"]["bank"], span) == 0 and
                intersection(data["ranges"]["staging"], span) == 0, "excluded owner borrowed")
    require(intersection([0x2001,0xa048], data["ranges"]["landing"]) == 8264, "current landing collision")
    contract_text = (ROOT / EDITED[2]).read_text()
    for phrase in ["16 volatile signature reads", "Prior success never grants",
                   "resident terminal sink", "BLOCKED BY MEMORY OWNERSHIP", "REJECT OPTION A"]:
        require(phrase in contract_text, "contract/model mismatch: " + phrase)
    checked_seals = 0
    for parent_name in ["2026-10-27-m2-min-rebuild", "2026-10-27-m2-min-rebuild-corrections", "2026-10-28-m2-banked-renderer-intent"]:
        parent = ROOT / "docs/evidence/flight-demo" / parent_name
        seals = list(parent.glob("*/seal.json"))
        if (parent / "seal.json").exists(): seals.append(parent / "seal.json")
        for seal in seals:
            items = load(seal)
            require(set(items) == {str(p.relative_to(seal.parent)) for p in seal.parent.rglob("*")
                    if p.is_file() and p != seal}, "sealed inventory changed")
            for name, identity in items.items():
                path = seal.parent / name
                require(path.stat().st_size == identity["bytes"] and sha(path) == identity["sha256"], "sealed member changed")
            checked_seals += 1
    require(checked_seals == 13, "prior sealed packet count")
    profile = load(ROOT / "interfaces/m2_rebuild.json")
    require(profile["target_budgets"] == [0]*8 and profile["runtime_enablement"] is False and profile["memory"]["reserve_used"] == 0, "launch/limits")
    # Preservation covers the review snapshot; edited preimages live in an archive.
    reviewed = json.loads(gzip.decompress((HERE / "reviewed-inventory.json.gz").read_bytes()))
    require(len(reviewed) == 16060 and hashlib.sha256(json.dumps(reviewed, sort_keys=True).encode()).hexdigest() == "bba8638cf77e85e241212c8056130f5ce4102c00ab9f1eb25b46b8a4133e593e", "reviewed inventory identity")
    with tarfile.open(HERE / "reviewed-before-p2.tar.gz", "r:gz") as archive:
        require(set(archive.getnames()) == set(EDITED), "reviewed preimage archive")
        for name in EDITED:
            raw = archive.extractfile(name).read()
            require(len(raw) == reviewed[name]["bytes"] and hashlib.sha256(raw).hexdigest() == reviewed[name]["sha256"], "edited preimage preserved")
    for name, item in reviewed.items():
        if name not in EDITED:
            path = ROOT / name
            require(path.stat().st_size == item["bytes"] and sha(path) == item["sha256"], "unrelated reviewed file changed: " + name)
    prior = load(ROOT / "docs/evidence/flight-demo/2026-10-27-m2-min-rebuild/final-check-1793159584829644000/original-checkout-current-inventory.json")
    original = Path("/Users/slice/Developer/f65-megawing")
    for name, item in prior.items():
        path = original / name
        require(path.stat().st_size == item["bytes"] and sha(path) == item["sha256"], "original path changed")
    require(len(prior) == 480, "original path count")
    historical = load(ROOT / "docs/evidence/flight-demo/2026-10-27-m2-residency-feasibility/accounting.json")["original_checkout_before"]
    for command, key in [(('status','--porcelain=v1'),'status_sha256'),(('diff','--binary'),'diff_sha256')]:
        require(hashlib.sha256(git(original,*command)).hexdigest() == historical[key], "original Git state changed")
    require(git(ROOT,"rev-parse","HEAD").decode().strip() == BASE and git(ROOT,"branch","--show-current").decode().strip() == "codex/65aero-m2-banked-renderer-intent", "branch ancestry")
    require(set(git(ROOT,"diff","--name-only").decode().splitlines()) == {"WORK_IN_PROGRESS.md", "docs/plans/65AERO_M2_RESIDENCY_FEASIBILITY.md"} and not git(ROOT,"diff","--cached","--name-only"), "tracked scope")
    additions = [n.decode() for n in git(ROOT,"ls-files","--others","--exclude-standard","-z").split(b'\0') if n]
    for name in additions:
        require(name == EDITED[1] or name.startswith(("docs/evidence/flight-demo/2026-10-28-m2-banked-renderer-intent/", "docs/evidence/flight-demo/2026-10-29-m2-rf-ex2-design/")), "untracked scope")
    documents = [ROOT / name for name in EDITED]
    require("crc_byte58" not in documents[2].read_text() and "crc_byte84" in documents[2].read_text(), "CRC document correction")
    for path in documents + [HERE / "validate.py", HERE / "accounting.json"]:
        text = path.read_text()
        require(all(line == line.rstrip(' \t') for line in text.splitlines()), "whitespace")
        if path.suffix == '.py': ast.parse(text, filename=str(path))
        for href in re.findall(r'\]\(([^)]+)\)', text) if path.suffix == '.md' else []:
            if '://' not in href and not href.startswith('#'):
                require((path.parent / href.split('#')[0]).exists(), "documentation target missing: " + href)
    mutations = regressions(data)
    print(json.dumps({"checks": "PASS", "tier": data["evidence_tier"], "crc_bytes": 84,
        "crc_removal_credit": 0, "closure_bytes": 9736, "optimistic_removal": 8625,
        "conditional_allowance_before_unknowns": 253, "final_allowance": None,
        "ownership": data["ownership"]["status"], "recommendation": data["decision"],
        "reviewed_files": 16060, "archived_edited_preimages": 3, "unchanged_reviewed_files": 16057,
        "original_paths": 480, "fail_closed_model_cases": mutations,
        "target_tools_run": False, "runtime_admitted": False}, indent=2))


if __name__ == '__main__':
    main()
