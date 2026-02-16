# Phelipanche (Broomrape) Research Module — Complete Scheme

## 1. Module Overview

The **Phelipanche module** (`coscientist/profiles/broomrape_tomato.py`) is a domain-specific
research profile that configures the Open CoScientist multi-agent AI system for investigating
parasitic weeds of the genus *Phelipanche* (broomrape) — primarily *P. ramosa* and
*P. aegyptiaca* — in **processing-tomato production** under **Mediterranean-type climates**.

It is the first (and currently only) research profile in the system, serving as both a
production configuration and a reference implementation for future profiles.

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     ENTRY POINT: run_broomrape_research.py                  │
│  CLI: python run_broomrape_research.py [goal_key]                          │
│  Default goal_key: "als_resistance"                                        │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PROFILE: broomrape_tomato.py                           │
│                                                                             │
│  ResearchProfile(                                                          │
│    name = "Broomrape × Industrial Tomato"                                  │
│    research_goals      = 6 goals   ──────────────────────────┐             │
│    specialist_fields   = 30 fields ──────────────────────┐   │             │
│    preferred_reasoning = 14 types  ──────────────────┐   │   │             │
│    default_goal_key    = "als_resistance"             │   │   │             │
│  )                                                    │   │   │             │
└───────────────────────────────────────────────────────┼───┼───┼─────────────┘
                                                        │   │   │
                    ┌───────────────────────────────────┘   │   │
                    │   ┌───────────────────────────────────┘   │
                    │   │   ┌───────────────────────────────────┘
                    ▼   ▼   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CONFIGURATION: CoscientistConfig                        │
│                                                                             │
│  literature_review_agent_llm  = GPT-5.1                                    │
│  generation_agent_llms        = {opus: Claude Opus 4.5, gpt: GPT-5.1}     │
│  reflection_agent_llms        = {opus: Claude Opus 4.5, gpt: GPT-5.1}     │
│  evolution_agent_llms         = {gpt: GPT-5.1}                             │
│  meta_review_agent_llm        = Claude Opus 4.5                            │
│  supervisor_agent_llm         = GPT-5.1                                    │
│  final_report_agent_llm       = Claude Opus 4.5                            │
│  specialist_fields            ← 30 from profile                            │
│  preferred_reasoning_types    ← 14 from profile                            │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FRAMEWORK: CoscientistFramework                         │
│                     + STATE: CoscientistStateManager                        │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
              ┌──────── PIPELINE (9 agent stages) ────────┐
              │                                            │
              ▼                                            │
┌──────────────────────────────┐                           │
│ STAGE 1: LITERATURE REVIEW   │                           │
│ LLM: GPT-5.1                │                           │
│ Prompt: topic_decomposition  │                           │
│ Tool: GPTResearcher+Tavily   │                           │
│                              │                           │
│ Goal → ≤5 subtopics →       │                           │
│   web/academic search →     │                           │
│   literature_review          │                           │
└──────────────┬───────────────┘                           │
               ▼                                           │
┌──────────────────────────────┐                           │
│ STAGE 2: HYPOTHESIS          │                           │
│          GENERATION          │                           │
│ LLMs: Claude Opus 4.5       │                           │
│       + GPT-5.1 (random)    │                           │
│                              │                           │
│ For each hypothesis:         │                           │
│  • Pick random specialist    │                           │
│    field (1 of 30)           │                           │
│  • Pick random reasoning     │                           │
│    type (1 of 14)            │                           │
│  • Pick random LLM           │                           │
│  • Pick mode:                │                           │
│    - independent (solo)      │                           │
│    - collaborative (debate)  │                           │
│                              │                           │
│ Output: ParsedHypothesis     │                           │
│  ├─ uid (UUID4)              │                           │
│  ├─ hypothesis (statement)   │                           │
│  ├─ predictions[] (1-3)      │                           │
│  └─ assumptions[]            │                           │
└──────────────┬───────────────┘                           │
               ▼                                           │
┌──────────────────────────────┐                           │
│ STAGE 3: REFLECTION /        │                           │
│          DEEP VERIFICATION   │                           │
│ LLMs: Claude Opus 4.5       │                           │
│       + GPT-5.1 (random)    │                           │
│                              │                           │
│ 3a. Desk Reject (filter)     │                           │
│     → pass/fail              │                           │
│                              │                           │
│ 3b. Parallel (if passed):    │                           │
│  ┌─ Cause & Effect analysis  │                           │
│  │  → _causal_reasoning      │                           │
│  └─ Assumption Decomposer   │                           │
│     → _parsed_assumptions    │                           │
│                              │                           │
│ 3c. Assumption Researcher    │                           │
│     GPTResearcher + Tavily   │                           │
│     → empirical evidence     │                           │
│                              │                           │
│ 3d. Deep Verification        │                           │
│     → ReviewedHypothesis     │                           │
│       (adds verification_    │                           │
│        result, causal_       │                           │
│        reasoning, assumption │                           │
│        _research_results)    │                           │
└──────────────┬───────────────┘                           │
               ▼                                           │
┌──────────────────────────────┐                           │
│ STAGE 4: TOURNAMENT /        │                           │
│          ELO RANKING         │                           │
│ LLM: Claude Opus 4.5        │                           │
│                              │                           │
│ Round Robin:                 │                           │
│  • Every pair compared       │                           │
│  • Prompt: tournament.md     │                           │
│  • Winner decided per match  │                           │
│  • ELO updates (K-factor)    │                           │
│                              │                           │
│ Bracket (top K, power of 2): │                           │
│  • Multi-turn debates        │                           │
│  • Prompt: simulated_debate  │                           │
│  • Up to 10 turns per match  │                           │
│  • Further ELO refinement    │                           │
│                              │                           │
│ Output: EloTournament        │                           │
│  ├─ ratings{uid → float}     │                           │
│  ├─ match_history            │                           │
│  └─ debate transcripts       │                           │
└──────────────┬───────────────┘                           │
               ▼                                           │
┌──────────────────────────────┐                           │
│ STAGE 5: META-REVIEW         │                           │
│ LLM: Claude Opus 4.5        │                           │
│ Prompt: meta_review_         │                           │
│         tournament.md        │                           │
│                              │                           │
│ Synthesizes:                 │                           │
│  • Common strengths          │                           │
│  • Recurring weaknesses      │                           │
│  • Evaluation criteria       │                           │
│  • Bias patterns             │                           │
│  • Actionable insights       │                           │
└──────────────┬───────────────┘                           │
               ▼                                           │
┌──────────────────────────────┐                           │
│ STAGE 6: SUPERVISOR          │◄──────────────────────────┘
│ LLM: GPT-5.1                │         (loop back)
│ Prompt: supervisor_decision  │
│                              │
│ Reviews state + meta-review  │
│ Decides next action:         │
│  • generate_new_hypotheses   │──→ back to Stage 2
│  • evolve_hypotheses         │──→ to Stage 7
│  • expand_literature_review  │──→ back to Stage 1
│  • run_tournament            │──→ back to Stage 4
│  • run_meta_review           │──→ back to Stage 5
│  • finish                    │──→ to Stage 9
└──────────────┬───────────────┘
               │ (if evolve_hypotheses)
               ▼
┌──────────────────────────────┐
│ STAGE 7: EVOLUTION           │
│ LLM: GPT-5.1                │
│                              │
│ Mode A: Evolve from Feedback │
│  • Top-ranked + random hyps  │
│  • Refine via tournament     │
│    critiques                 │
│  • Prompt: evolve_from_      │
│    feedback.md               │
│                              │
│ Mode B: Out of the Box       │
│  • Creative recombination    │
│    of top K hypotheses       │
│  • Prompt: out_of_the_box.md │
│                              │
│ Evolved → reflection queue   │
│         → back to Stage 3    │
└──────────────────────────────┘

               ┌───────────────┐
               │ (if finish)   │
               ▼               │
┌──────────────────────────────┐
│ STAGE 8: PROXIMITY GRAPH     │
│ (runs continuously)          │
│                              │
│ Embedding: text-embedding-   │
│            3-small (256d)    │
│                              │
│ Tracks semantic similarity   │
│ between all hypotheses via   │
│ cosine similarity + NetworkX │
│ community detection          │
│                              │
│ Metrics fed to supervisor:   │
│  • avg cosine similarity     │
│  • cluster count trajectory  │
└──────────────────────────────┘

               │
               ▼
┌──────────────────────────────┐
│ STAGE 9: FINAL REPORT        │
│ LLM: Claude Opus 4.5        │
│ Prompt: final_report.md      │
│                              │
│ All hypotheses by ELO rank   │
│ Top 3 detailed:              │
│  • Hypothesis statement      │
│  • Causal reasoning          │
│  • Verification results      │
│  • Falsifiable predictions   │
│                              │
│ Output → final_report        │
│ Saved to ~/.coscientist/     │
└──────────────────────────────┘
```

---

## 3. Profile Components in Detail

### 3.1 Research Goals (6)

| # | Key | Focus Area | Target |
|---|-----|-----------|--------|
| 1 | `als_resistance` **(default)** | ALS herbicide resistance status & alternative chemistries | Chile's Central Valley, maleic hydrazide, prohexadione-calcium |
| 2 | `integrated_management` | Integrated management programme design | Chemical × biological × cultural × precision ag synergies |
| 3 | `germination_ecology` | Strigolactone-mediated germination | Root exudate profiles, suicidal germination, seedbank depletion |
| 4 | `precision_detection` | Remote sensing & ML detection | UAV multispectral/hyperspectral, Sentinel-2, PlanetScope, GIS DSS |
| 5 | `seed_bank_dynamics` | Seedbank demographic modelling | Seed longevity, dormancy cycling, mechanistic population models |
| 6 | `host_resistance` | Genetic resistance in processing tomato | *S. pennellii*, *S. habrochaites*, CRISPR, marker-assisted selection |

### 3.2 Specialist Fields (30)

```
PARASITIC WEED BIOLOGY (5)          CHEMICAL CONTROL (5)
├─ parasitic plant biology           ├─ herbicide resistance mechanisms
│  (Orobanchaceae)                   │  (ALS inhibitors)
├─ strigolactone signalling          ├─ pre/post-emergence herbicide
│  and germination stimulants        │  strategies
├─ parasite–host plant               ├─ novel herbicide modes of action
│  interactions                      │  and experimental molecules
├─ parasitic weed seed bank          ├─ plant growth regulators (ethylene,
│  ecology                           │  gibberellin, ABA pathways)
└─ Orobanchaceae taxonomy and        └─ herbicide safeners, adjuvants,
   population genetics                  and formulation science

BIOLOGICAL & CULTURAL (5)           HOST RESISTANCE & BREEDING (3)
├─ trap and catch crops              ├─ tomato genetics and
│  for broomrape management          │  molecular breeding
├─ soil solarisation and             ├─ CRISPR and gene-editing
│  biofumigation                     │  technologies
├─ biological control                └─ wild Solanum germplasm
│  (Fusarium, mycorrhiza)               and pre-breeding
├─ allelopathy and root
│  exudate ecology                  TOMATO AGRONOMY (4)
└─ crop rotation design for          ├─ industrial tomato production
   parasitic weed suppression        ├─ Mediterranean agronomy and
                                     │  climate adaptation
PRECISION AGRICULTURE (4)            ├─ drip irrigation and fertigation
├─ remote sensing for parasitic      └─ Solanaceae crop physiology
│  weed detection
├─ hyperspectral and thermal        QUANTITATIVE METHODS (4)
│  imaging of crop stress            ├─ experimental design for
├─ GIS mapping and spatial           │  parasitic weed trials
│  decision support                  ├─ spatial analysis of broomrape
└─ precision herbicide               │  distribution patterns
   application technology            ├─ population dynamics modelling
                                     │  (seed bank demography)
                                     ├─ dose–response modelling
                                     │  and bioassays
                                     └─ Bayesian analysis of
                                        multi-environment trials
```

### 3.3 Preferred Reasoning Types (14 of 18)

| Reasoning Type | Role in Phelipanche Research |
|---------------|----------------------------|
| `FIRST_PRINCIPLES` | Ground-up decomposition of parasite biology |
| `SYSTEMS` | Feedback loops in crop-parasite-soil-herbicide interactions |
| `CAUSAL` | Cause-effect chains (strigolactone → germination → attachment) |
| `STATISTICAL` | Frequentist + Bayesian inference for field trial data |
| `EVOLUTIONARY` | Herbicide resistance evolution under selection pressure |
| `SPATIAL` | Landscape-scale infestation mapping, geostatistics, kriging |
| `ECOLOGICAL` | Community-level interactions (mycorrhiza, allelopathy, trap crops) |
| `MECHANISTIC_MODELLING` | Process-based seedbank population dynamics models |
| `BAYESIAN` | Prior-updating for multi-environment trial analyses |
| `MIXED_MODELS` | GLMMs for nested/repeated-measures field experiments |
| `GEOSTATISTICAL` | Variograms, kriging, remote sensing integration |
| `SIMULATION` | Monte Carlo, agent-based seedbank depletion scenarios |
| `ABDUCTIVE` | Most plausible explanation from incomplete field evidence |
| `COUNTERFACTUAL` | "What if" management scenarios, policy alternatives |

**Excluded types:** `ANALOGY`, `DEDUCTIVE`, `INDUCTIVE`, `HEURISTIC` — considered less relevant for this domain.

---

## 4. Data Flow Diagram

```
                    ┌────────────────────┐
                    │  PROFILE           │
                    │  (30 fields,       │
                    │   14 reasoning,    │
                    │   6 goals)         │
                    └────────┬───────────┘
                             │ selects goal
                             ▼
                    ┌────────────────────┐
                    │  CoscientistState  │     Persisted to:
                    │  (goal, all data)  │──→  ~/.coscientist/<hash>/
                    └────────┬───────────┘     coscientist_state_*.json
                             │
    ┌────────────────────────┼────────────────────────────┐
    │                        │                            │
    ▼                        ▼                            ▼
┌────────┐          ┌────────────────┐           ┌──────────────┐
│ Lit.   │          │ Hypothesis     │           │ Proximity    │
│ Review │──text──→ │ Pipeline       │──embeds──→│ Graph        │
│        │          │                │           │ (NetworkX +  │
└────────┘          │ generated_     │           │  OpenAI      │
                    │ hypotheses[]   │           │  embeddings) │
                    │       │        │           └──────────────┘
                    │       ▼        │
                    │ reflection_    │
                    │ queue[]        │
                    │       │        │
                    │       ▼        │
                    │ reviewed_      │
                    │ hypotheses[]   │
                    │       │        │
                    │       ▼        │
                    │ EloTournament  │
                    │  ├─ ratings{}  │
                    │  ├─ matches{}  │
                    │  └─ debates{}  │
                    │       │        │
                    │       ▼        │
                    │ evolved_       │
                    │ hypotheses[] ──┼──→ back to reflection_queue
                    │       │        │
                    │       ▼        │
                    │ meta_reviews[] │
                    │       │        │
                    │       ▼        │
                    │ final_report   │
                    └────────────────┘
```

---

## 5. Hypothesis Lifecycle

```
BIRTH                VERIFICATION             COMPETITION           EVOLUTION
  │                      │                        │                    │
  ▼                      ▼                        ▼                    ▼
ParsedHypothesis → [desk_reject] → ReviewedHypothesis → EloTournament → evolved
  │                  pass/fail       │                    │              │
  ├─ uid                             ├─ causal_reasoning  ├─ ELO rating  ├─ parent_uid
  ├─ hypothesis                      ├─ assumption_       ├─ win/loss    └─ refined
  ├─ predictions[]                   │  research_results  └─ debate         hypothesis
  └─ assumptions[]                   └─ verification_        transcripts
                                        result
```

---

## 6. File Structure

```
coscientist/
├── profiles/
│   ├── __init__.py              ← ResearchProfile dataclass
│   └── broomrape_tomato.py      ← PROFILE object (goals, fields, reasoning)
├── framework.py                 ← CoscientistConfig + CoscientistFramework
├── global_state.py              ← CoscientistState + CoscientistStateManager
├── reasoning_types.py           ← 18 ReasoningType enum values
├── custom_types.py              ← ParsedHypothesis, ReviewedHypothesis
├── generation_agent.py          ← Hypothesis generation (independent/collaborative)
├── reflection_agent.py          ← Deep verification pipeline
├── ranking_agent.py             ← EloTournament (round robin + bracket)
├── evolution_agent.py           ← Evolve from feedback + out of the box
├── meta_review_agent.py         ← Tournament meta-analysis
├── literature_review_agent.py   ← Topic decomposition + GPTResearcher
├── supervisor_agent.py          ← Orchestration decisions
├── final_report_agent.py        ← Report generation
├── proximity_agent.py           ← ProximityGraph (semantic similarity)
├── multiturn.py                 ← Multi-turn debate infrastructure
└── prompts/
    ├── topic_decomposition.md   ← Literature review subtopic generation
    ├── independent_generation.md← Solo hypothesis generation
    ├── collaborative_generation.md ← Debate-based generation
    ├── desk_reject.md           ← Quick plausibility filter
    ├── cause_and_effect.md      ← Mechanistic reasoning
    ├── assumption_decomposer.md ← Break assumptions into sub-assumptions
    ├── deep_verification.md     ← Comprehensive hypothesis review
    ├── tournament.md            ← Single-turn head-to-head comparison
    ├── simulated_debate.md      ← Multi-turn scientific debate
    ├── meta_review_tournament.md← Cross-debate pattern synthesis
    ├── evolve_from_feedback.md  ← Refine based on critique
    ├── out_of_the_box.md        ← Creative recombination
    ├── supervisor_decision.md   ← Next-action decision
    └── final_report.md          ← Report formatting

run_broomrape_research.py        ← CLI entry point
```

---

## 7. Aspects Requiring Clarification

### 7.1 Scientific / Domain Questions

| # | Question | Impact | Where |
|---|----------|--------|-------|
| **Q1** | The default goal focuses on **Chile's Central Valley** — is this the primary deployment region, or should goals be generalized to broader Mediterranean zones (Spain, Italy, Israel, Turkey, Tunisia)? | Narrows/widens literature search and hypothesis relevance | `broomrape_tomato.py:33-42` |
| **Q2** | Goal 1 mentions **maleic hydrazide and prohexadione-calcium** as experimental molecules. Are these the only candidates of interest, or should the system also explore newer experimental compounds (e.g., T-010, nijmegen-1, GR24 analogues)? | May limit hypothesis diversity | `broomrape_tomato.py:38-39` |
| **Q3** | *P. aegyptiaca* is mentioned in the profile description but **none of the 6 goals explicitly address it** — they all focus on *P. ramosa*. Should there be a dedicated *P. aegyptiaca* goal, or is it intentionally secondary? | Species scope | `broomrape_tomato.py:171-189` |
| **Q4** | The specialist fields do **not include economics/socioeconomics** (e.g., "farm-level cost-benefit analysis", "adoption barriers for smallholders"). Should economic feasibility be part of the evaluation framework? | Hypothesis practicality assessment | `broomrape_tomato.py:107-146` |
| **Q5** | No **climate-change interaction** field exists (e.g., "climate change impacts on Orobanchaceae distribution and phenology"). Given Mediterranean climate projections, should this be added? | Long-term relevance | `broomrape_tomato.py:107-146` |

### 7.2 Technical / Architecture Questions

| # | Question | Impact | Where |
|---|----------|--------|-------|
| **Q6** | The 4 **excluded reasoning types** (ANALOGY, DEDUCTIVE, INDUCTIVE, HEURISTIC) — was this a deliberate domain decision or just a first pass? For example, ANALOGY could be valuable for transferring Striga management strategies to Phelipanche. | Hypothesis diversity | `broomrape_tomato.py:151-166` |
| **Q7** | The profile has **no configurable LLM presets** — the runner script hardcodes `gpt-5.1` + `claude-opus-4-5`. Should the profile carry recommended LLM assignments, or is this intentionally left to the runner? | Profile portability | `run_broomrape_research.py:86-87` |
| **Q8** | Generation uses **random sampling** of (field, reasoning_type, LLM, mode). Should there be a weighting system (e.g., more weight on core parasitic biology fields vs. precision ag) or a coverage tracker to ensure all 30 fields get explored? | Hypothesis coverage balance | `framework.py:315-319` |
| **Q9** | The desk reject prompt is a **binary pass/fail** with no feedback. Should rejected hypotheses receive structured feedback that gets fed back to the generation agent for improvement, rather than being silently discarded? | Loss of creative ideas | `framework.py:303` |
| **Q10** | The proximity graph uses a **fixed embedding model** (`text-embedding-3-small`, 256 dims). Is this sufficient for capturing nuanced domain-specific semantic differences between Phelipanche hypotheses, or should a domain-tuned model be considered? | Semantic clustering quality | `framework.py:164-165` |
| **Q11** | The supervisor sees **ELO statistics and action history** but **not** the actual hypothesis content or literature review text. Is this intentional (to prevent bias) or a limitation that should be addressed? | Supervisor decision quality | `global_state.py:1087-1164` |
| **Q12** | `start()` defaults to **4 initial hypotheses** (hardcoded in `run()`), but the `start()` method accepts `n_hypotheses` as a parameter. Should this be profile-configurable? | Initial hypothesis pool size | `framework.py:542-544` |

### 7.3 Operational Questions

| # | Question | Impact | Where |
|---|----------|--------|-------|
| **Q13** | The `gpt-researcher` dependency requires **Python >= 3.11**, but `setup.py` claims `python_requires=">=3.9"` and CI tests on 3.10. This currently breaks CI. Should the minimum be bumped to 3.11? | CI pipeline, user compatibility | `setup.py:29` |
| **Q14** | The profile is a **Python module** (not YAML/JSON). This means non-programmers cannot easily create or modify profiles. Should there be a declarative format (YAML/TOML) with a loader? | Accessibility for domain scientists | `profiles/__init__.py` |
| **Q15** | There is **no validation** that a profile's specialist fields or reasoning types are compatible with the underlying prompt templates. A field like "quantum computing" would be accepted but produce nonsensical results. Should there be a validation layer? | Profile correctness | `framework.py:182-210` |
| **Q16** | State is persisted as **JSON snapshots** in `~/.coscientist/<hash>/`. There is no cleanup policy — long research campaigns could accumulate significant disk usage. Should there be a retention/archival strategy? | Disk usage | `global_state.py:319-341` |

---

## 8. Summary Statistics

| Metric | Value |
|--------|-------|
| Research goals | 6 |
| Specialist fields | 30 (across 7 categories) |
| Reasoning types | 14 of 18 available |
| Agent stages | 9 (lit review → generation → reflection → tournament → meta-review → supervisor → evolution → proximity → final report) |
| LLMs used | 2 (GPT-5.1 + Claude Opus 4.5) |
| Prompt templates | 15 markdown files |
| Entry point | `run_broomrape_research.py` |
| State persistence | JSON → `~/.coscientist/<sha256[:12]>/` |
| Test fixtures | 3 Phelipanche-specific hypotheses |
