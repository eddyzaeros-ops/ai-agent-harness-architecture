# -*- coding: utf-8 -*-
"""
build_master_pptx.py
Master compiler script to build the complete 54-slide OWASP LLM Guardrail Design presentation.
Includes all 13 comparison tables, 6 Mermaid sequence diagrams, 5 technical code/specs,
and 6 publication-grade Matplotlib charts.
Strictly complies with pptx-template-1 design standards.
"""

import os
import shutil
import sys
from pptx import Presentation

# Ensure module path is active
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slides_common import init_presentation as create_base_presentation, update_all_slide_footers
from slides_m00 import (
    build_slide_01_cover,
    build_slide_02_overview_matrix,
    build_slide_03_module_navigation_table,
    build_slide_04_four_tier_synergy_flow,
    build_slide_05_defense_in_depth_scenario,
    build_slide_06_attack_tree_interception
)
from slides_m01 import (
    build_slide_07_llm_architecture,
    build_slide_08_llm_sequence_flow,
    build_slide_09_llm_top10_p1,
    build_slide_10_llm_top10_p2,
    build_slide_11_llm_quant_p1,
    build_slide_12_llm_quant_p2,
    build_slide_13_audit_log_spec,
    build_slide_14_llm_tech_stack
)
from slides_m02 import (
    build_slide_15_agentic_paradigm,
    build_slide_16_agentic_three_dimensions_diagram,
    build_slide_17_agentic_sequence_flow,
    build_slide_18_agentic_top10_p1,
    build_slide_19_agentic_top10_p2,
    build_slide_20_agentic_quant_p1,
    build_slide_21_agentic_quant_p2,
    build_slide_22_agentic_security_controls
)
from slides_m03 import (
    build_slide_23_skills_lethal_trifecta,
    build_slide_24_skills_lifecycle_architecture,
    build_slide_25_skills_sequence_flow,
    build_slide_26_skills_top10_p1,
    build_slide_27_skills_top10_p2,
    build_slide_28_skills_quant_p1,
    build_slide_29_skills_quant_p2,
    build_slide_30_skills_manifest_and_envelope
)
from slides_m04 import (
    build_slide_31_rag_lifecycle,
    build_slide_32_rag_architecture_diagram,
    build_slide_33_rag_sequence_flow,
    build_slide_34_rag_top10_p1,
    build_slide_35_rag_top10_p2,
    build_slide_36_rag_quant_p1,
    build_slide_37_rag_quant_p2,
    build_slide_38_rag_code_and_bundle
)
from slides_m05 import (
    build_slide_39_mitre_paradigm,
    build_slide_40_mitre_kill_chain_architecture,
    build_slide_41_mitre_telescoping_kill_chain,
    build_slide_42_mitre_atlas_p1,
    build_slide_43_mitre_atlas_p2,
    build_slide_44_mitre_quant_p1,
    build_slide_45_mitre_quant_p2,
    build_slide_46_defense_principles_engineering
)
from slides_conclusion import (
    build_slide_47_zero_trust_manifesto,
    build_slide_48_manifesto_quote
)
from slides_charts import (
    build_slide_chart_0_overview_radar,
    build_slide_chart_1_llm_dual_axis,
    build_slide_chart_2_agentic_scatter,
    build_slide_chart_3_skills_horizontal,
    build_slide_chart_4_rag_grouped,
    build_slide_chart_5_atlas_killchain
)
from slides_glossary import (
    build_slide_glossary_1,
    build_slide_glossary_2,
    build_slide_glossary_3,
    build_slide_glossary_4
)

def build_all_slides():
    print("=" * 65)
    print("Building 54-Slide Master OWASP AI Guardrail Presentation...")
    print("=" * 65)

    prs = create_base_presentation()

    slide_builders = [
        # Module 00: Overview & System Architecture (Slides 01 - 07)
        ("Slide 01: Cover Page", build_slide_01_cover),
        ("Slide 02: Overview & 4-Tier Matrix", build_slide_02_overview_matrix),
        ("Slide 03: [Chart 0] Six-Dimensional Defense Capability Radar", build_slide_chart_0_overview_radar),
        ("Slide 04: Module Navigation & Standards Cross-Reference", build_slide_03_module_navigation_table),
        ("Slide 05: 4-Tier Synergistic Defense Pipeline Flow", build_slide_04_four_tier_synergy_flow),
        ("Slide 06: Defense-in-Depth Multi-Stage Interception Scenario", build_slide_05_defense_in_depth_scenario),
        ("Slide 07: Attack Tree & Interception Verification", build_slide_06_attack_tree_interception),

        # Module 01: Core LLM Guardrails (Slides 08 - 16)
        ("Slide 08: Bidirectional LLM Guardrail Pipeline Architecture", build_slide_07_llm_architecture),
        ("Slide 09: LLM Guardrail Runtime Sequence Flow", build_slide_08_llm_sequence_flow),
        ("Slide 10: OWASP LLM Top 10 Defense Matrix (Part 1)", build_slide_09_llm_top10_p1),
        ("Slide 11: OWASP LLM Top 10 Defense Matrix (Part 2)", build_slide_10_llm_top10_p2),
        ("Slide 12: LLM Guardrails Quantitative KPI & Benchmarks (Part 1)", build_slide_11_llm_quant_p1),
        ("Slide 13: LLM Guardrails Quantitative KPI & Benchmarks (Part 2)", build_slide_12_llm_quant_p2),
        ("Slide 14: [Chart 1] LLM Top 10 Occurrence vs. Latency Dual-Axis", build_slide_chart_1_llm_dual_axis),
        ("Slide 15: Technical Spec: JSON Audit Logging Schema", build_slide_13_audit_log_spec),
        ("Slide 16: Technology Selection Matrix & Guardrail Frameworks", build_slide_14_llm_tech_stack),

        # Module 02: Agentic Architecture & Tool Guardrails (Slides 17 - 25)
        ("Slide 17: Agentic Security: Passive LLM vs Autonomous Agent", build_slide_15_agentic_paradigm),
        ("Slide 18: Three-Dimensional Six-Gate Guardrail Architecture", build_slide_16_agentic_three_dimensions_diagram),
        ("Slide 19: Agent Tool Execution Sequence Flow", build_slide_17_agentic_sequence_flow),
        ("Slide 20: OWASP Agentic Top 10 Defense Matrix (Part 1)", build_slide_18_agentic_top10_p1),
        ("Slide 21: OWASP Agentic Top 10 Defense Matrix (Part 2)", build_slide_19_agentic_top10_p2),
        ("Slide 22: Agentic Guardrails Quantitative KPI & Benchmarks (Part 1)", build_slide_20_agentic_quant_p1),
        ("Slide 23: Agentic Guardrails Quantitative KPI & Benchmarks (Part 2)", build_slide_21_agentic_quant_p2),
        ("Slide 24: [Chart 2] Agentic 10 Threats Occurrence vs Interception", build_slide_chart_2_agentic_scatter),
        ("Slide 25: Agentic Defense-in-Depth Core Security Controls", build_slide_22_agentic_security_controls),

        # Module 03: Skills & Extension Security (Slides 26 - 34)
        ("Slide 26: Skills Security: Lethal Trifecta Attack Vector", build_slide_23_skills_lethal_trifecta),
        ("Slide 27: Four-Stage Skills Lifecycle Defense Architecture", build_slide_24_skills_lifecycle_architecture),
        ("Slide 28: Skill Execution Runtime Sequence Flow", build_slide_25_skills_sequence_flow),
        ("Slide 29: OWASP Skills Top 10 Defense Matrix (Part 1)", build_slide_26_skills_top10_p1),
        ("Slide 30: OWASP Skills Top 10 Defense Matrix (Part 2)", build_slide_27_skills_top10_p2),
        ("Slide 31: Skills Guardrails Quantitative KPI & Benchmarks (Part 1)", build_slide_28_skills_quant_p1),
        ("Slide 32: Skills Guardrails Quantitative KPI & Benchmarks (Part 2)", build_slide_29_skills_quant_p2),
        ("Slide 33: [Chart 3] Skills 10 Risks Distribution vs Sandbox Defense", build_slide_chart_3_skills_horizontal),
        ("Slide 34: Technical Specs: YAML Skill Manifest & XML Untrusted Result", build_slide_30_skills_manifest_and_envelope),

        # Module 04: RAG Pipeline Security & Ingestion Defense (Slides 35 - 43)
        ("Slide 35: RAG Full Lifecycle Ingestion & Query Defense", build_slide_31_rag_lifecycle),
        ("Slide 36: Enterprise RAG Six-Stage Guardrail Architecture", build_slide_32_rag_architecture_diagram),
        ("Slide 37: RAG Query & Ingestion Pipeline Sequence Flow", build_slide_33_rag_sequence_flow),
        ("Slide 38: OWASP RAG Top 10 Defense Matrix (Part 1)", build_slide_34_rag_top10_p1),
        ("Slide 39: OWASP RAG Top 10 Defense Matrix (Part 2)", build_slide_35_rag_top10_p2),
        ("Slide 40: RAG Pipeline Quantitative KPI & Benchmarks (Part 1)", build_slide_36_rag_quant_p1),
        ("Slide 41: RAG Pipeline Quantitative KPI & Benchmarks (Part 2)", build_slide_37_rag_quant_p2),
        ("Slide 42: [Chart 4] RAG Risk Share vs. Retrieval Poisoning Impact", build_slide_chart_4_rag_grouped),
        ("Slide 43: Technical Specs: Python Pre-Filtering & XML Grounding Bundle", build_slide_38_rag_code_and_bundle),

        # Module 05: MITRE ATLAS AI Threat Matrix (Slides 44 - 52)
        ("Slide 44: Threat Modeling: MITRE ATT&CK vs MITRE ATLAS", build_slide_39_mitre_paradigm),
        ("Slide 45: ATLAS Attack Kill Chain & Defense Architecture", build_slide_40_mitre_kill_chain_architecture),
        ("Slide 46: Telescoping Kill Chain Attack Trajectory", build_slide_41_mitre_telescoping_kill_chain),
        ("Slide 47: MITRE ATLAS Top 10 AI Threat Defense Matrix (Part 1)", build_slide_42_mitre_atlas_p1),
        ("Slide 48: MITRE ATLAS Top 10 AI Threat Defense Matrix (Part 2)", build_slide_43_mitre_atlas_p2),
        ("Slide 49: MITRE ATLAS Quantitative Defense Benchmarks (Part 1)", build_slide_44_mitre_quant_p1),
        ("Slide 50: MITRE ATLAS Quantitative Defense Benchmarks (Part 2)", build_slide_45_mitre_quant_p2),
        ("Slide 51: [Chart 5] ATLAS AI Kill Chain Defense Interception Rates", build_slide_chart_5_atlas_killchain),
        ("Slide 52: AI Defense Engineering: Four Fundamental Principles", build_slide_46_defense_principles_engineering),

        # Appendix: Comprehensive Glossary of Terms & Acronyms (Slides 53 - 56)
        ("Slide 53: [Appendix 1] Glossary: Core Architecture & Governance", build_slide_glossary_1),
        ("Slide 54: [Appendix 2] Glossary: Semantic Boundary & Prompt Attacks", build_slide_glossary_2),
        ("Slide 55: [Appendix 3] Glossary: Skills Security & Micro-Sandbox", build_slide_glossary_3),
        ("Slide 56: [Appendix 4] Glossary: RAG Pipeline, Vector DB & MITRE ATLAS", build_slide_glossary_4),

        # Conclusion & Engineering Principles (Slides 57 - 58)
        ("Slide 57: Zero-Trust AI Guardrail Engineering Manifesto", build_slide_47_zero_trust_manifesto),
        ("Slide 58: Harness Engineering: Key Insight Quote & Closing", build_slide_48_manifesto_quote),
    ]

    for idx, (name, builder_func) in enumerate(slide_builders, 1):
        print(f"[{idx:02d}/58] Building {name}...")
        builder_func(prs)

    print("\nApplying unified sequential footer numbering across all slides...")
    update_all_slide_footers(prs)

    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "OWASP_LLM_Guardrail_Design.pptx")
    root_output_path = os.path.join(os.path.dirname(output_dir), "OWASP_LLM_Guardrail_Design.pptx")

    print("\nSaving presentation to primary location...")
    prs.save(output_path)
    print(f"Successfully saved to: {output_path}")

    print("Copying presentation to workspace root...")
    try:
        shutil.copy2(output_path, root_output_path)
        print(f"Successfully copied to: {root_output_path}")
    except Exception as e:
        print(f"Warning: Could not copy to root ({e}), but primary file is saved.")

    total_slides = len(prs.slides)
    print("\n" + "=" * 65)
    print(f"BUILD COMPLETE: Generated {total_slides} slides successfully!")
    print("=" * 65)

if __name__ == "__main__":
    build_all_slides()
