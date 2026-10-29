from pathlib import Path
import importlib.util,json,hashlib,shutil,sys
r=Path('/Users/slice/Developer/f65-megawing-m2-banked-renderer-intent');w=Path('/private/tmp/f65-rf-p2-67qvd18g');out=r/'docs/evidence/flight-demo/2026-10-29-m2-rf-ex2-design'
shutil.copyfile(w/'validate.py',out/'validate.py')
spec=importlib.util.spec_from_file_location('rf_design_check',out/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
symbols,edges,closure=v.linked_graph();target=json.loads((v.TARGET/'result.json').read_text())
names=[n for n in target['inputs'] if not n.startswith(('tools/','tests/'))]
assert all(v.sha(r/n)==target['inputs'][n] for n in names)
names+=['interfaces/f65_platform_abi.json5','memory/m2-rebuild-ledger.json',*v.EDITED,
 'spec/manifests/spec-corpus.json','spec/core/F65_Main_Concept_v1.7_HUMAN_APPROVED.md',
 'docs/evidence/flight-demo/2026-10-27-m2-residency-feasibility/accounting.json',
 'docs/evidence/flight-demo/2026-10-29-m2-rf-ex2-design/before-design.tar.gz',
 'docs/evidence/flight-demo/2026-10-29-m2-rf-ex2-design/reviewed-before-p2.tar.gz']
names += [str((v.TARGET/n).relative_to(r)) for n in ['result.json','seal.json','UNADMITTED.symbols','UNADMITTED.map','UNADMITTED.disassembly','sdk-inputs-before.json','UNADMITTED.prg','UNADMITTED.prg.elf']]
model={'schema':1,'identity':'65AERO-M2-RF-EX2-P2-1','base':v.BASE,'reference':{'resident':32839,'ceiling':24575,'deficit':8264,'scratch':190,'reserve':0},
 'relocation':{'bank_candidates':{n:symbols[n] for n in v.BANK},'resident_closure':{n:symbols[n] for n in v.RESIDENT},'edges':{n:sorted(edges[n]) for n in sorted(closure)}},
 'crc':{'symbol':'crc_byte','address':0x77f1,'bytes':84,'direct_callers':['cfphysical_crc'],'resident_chain':['m1_platform_begin','cfrom_begin','cfphysical_crc','crc_byte'],'relocatable_credit':0,'resident_copy_required':True,'bank_duplicate_if_added_bytes':84,'budget_delta':0},
 'ranges':{'bank':[0x48000,0x4c000],'window':[0x8000,0xc000],'workspace':[0x4c000,0x50000],'landing':[0x8000,0xc000],'staging':[0x50000,0x54000],'audio_cache':[0x53000,0x56000],'software_stack':[0xc000,0xd000],'reserve':[0x58000,0x60000]},
 'ownership':{'status':'BLOCKED BY MEMORY OWNERSHIP','staging_owner':'ResourceManager','conflicting_owner':'Audio','overlap':[0x53000,0x54000],'exclusive_pre_audio_lease_proven':False,'exception_approved':False,'inherited_quiescence_proven':False,'active_allocation':False},
 'reuse':dict.fromkeys(['post_successful_platform_init','before_first_tick','no_pending_rom_work','no_runtime_restore_reload','failure_terminal_until_reset','no_handler_user','descriptor_disjoint','new_resident_placement_required','existing_255_stays_charged'],True),
 'gateway':{'owner':'Platform','signature_reads_per_call':16,'verify_after_selection_before_entry':True,'cached_authorization':False,'missing_wrong_changed_unreadable_fail_closed':True,'canonical_restore':True,'restore_uncertain_terminal':True,'non_reentrant':True,'nested_lockout':True,'irq_nmi_costs_required':True,'all_eight_slots_required':True},
 'budget':{'optimistic_removed':8625,'gross_allowance':361,'distinct_new_data':363,'distinct_resident':24577,'distinct_margin':-2,'conditional_new_data':108,'conditional_resident':24322,'conditional_pre_overhead_allowance':253,'unknown_resident_cost_upper_bounds':dict.fromkeys(v.UNKNOWN),'final_resident_allowance':None,'additional_hardware_stack':None,'additional_software_stack':None,'service_cycle_bounds':None,'whole_program_stack':'UNPROVEN','complete_fit':'UNPROVEN'},
 'workspace':{'current_physical_arena_demand':0,'arena_capacity':16384,'renderer_resident_bytes':676,'future_continuation_bytes':None},'decision':'REJECT OPTION A','inputs':{n:v.sha(r/n) for n in sorted(set(names))},
 'reviewed_preservation':{'files':16060,'digest':'bba8638cf77e85e241212c8056130f5ce4102c00ab9f1eb25b46b8a4133e593e','inventory':'reviewed-inventory.json.gz','edited_preimages':'reviewed-before-p2.tar.gz','edited_paths':v.EDITED,'unchanged':16057,'original_unrelated_paths':480},'evidence_tier':'DOCUMENTATION_STATIC_DESIGN_ONLY'}
(out/'accounting.json').write_text(json.dumps(model,indent=2)+'\n')
(out/'validation.json').write_text(json.dumps({'identity':model['identity'],'status':'RUNNING','commands':[],'evidence_tier':model['evidence_tier']},indent=2)+'\n')
print('New accounting and read-only checker created; no validation result claimed yet')
