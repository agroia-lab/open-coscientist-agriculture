"""Broomrape (Phelipanche spp.) on industrial tomato — research profile.

This profile configures the Open CoScientist multi-agent system for
research on parasitic weeds of the family Orobanchaceae — primarily
*Phelipanche ramosa* and *P. aegyptiaca* — in processing-tomato
production systems under Mediterranean-type climates.

The profile provides:
- 6 curated research goals spanning chemical control, integrated
  management, germination ecology, precision detection, seed-bank
  dynamics, and host resistance
- 30 specialist fields covering parasitic-weed biology, herbicide
  science, Mediterranean agronomy, precision agriculture, and
  quantitative methods
- A recommended subset of 14 reasoning types particularly relevant
  to this research domain

Usage
-----
>>> from coscientist.profiles.broomrape_tomato import PROFILE
>>> print(PROFILE.default_goal)
>>> print(PROFILE.specialist_fields[:5])
"""

from coscientist.profiles import ResearchProfile
from coscientist.reasoning_types import ReasoningType

# ---------------------------------------------------------------------------
# Research Goals
# ---------------------------------------------------------------------------
_RESEARCH_GOALS = {
    # ---- Goal 1 (default): ALS resistance & alternative herbicides ----------
    "als_resistance": (
        "In industrial tomato grown under Mediterranean-type climatic conditions, "
        "with emphasis on Chile's Central Valley, what is the current status and "
        "distribution of Phelipanche ramosa resistance to ALS-inhibiting herbicides, "
        "and which alternative herbicide modes of action—including experimental or "
        "not-yet-registered molecules (such as maleic hydrazide and prohexadione-"
        "calcium) and mixtures—show potential for crop-safe control of P. ramosa "
        "from the seedbank and germination phases through to parasite attachment "
        "(with secondary consideration of later stages), with the aim of generating "
        "testable hypotheses and designing field and greenhouse trials?"
    ),
    # ---- Goal 2: Integrated Phelipanche management -------------------------
    "integrated_management": (
        "How can chemical (pre- and post-emergence herbicides, fumigants), "
        "biological (Fusarium oxysporum f.sp. orthoceras, mycorrhizal "
        "competition), cultural (trap crops, catch crops, soil solarisation, "
        "crop rotation with non-hosts), and precision agriculture (remote "
        "sensing–guided variable-rate herbicide application) tactics be "
        "combined into a durable integrated management programme for "
        "Phelipanche ramosa in drip-irrigated industrial tomato, and what "
        "are the most critical interactions, synergies, and trade-offs among "
        "these tactics across successive growing seasons?"
    ),
    # ---- Goal 3: Strigolactone-mediated germination ecology -----------------
    "germination_ecology": (
        "What are the quantitative relationships between tomato root "
        "strigolactone exudation profiles (composition, concentration, "
        "spatial distribution in the rhizosphere), Phelipanche ramosa "
        "seed conditioning requirements (thermal time, moisture thresholds), "
        "and germination efficiency under field conditions, and how can this "
        "knowledge be exploited to develop germination-stimulant-based "
        "management strategies (e.g., suicidal germination with synthetic "
        "strigolactone analogues, reduced-exudation tomato genotypes, or "
        "soil amendment timing) that deplete the P. ramosa seed bank?"
    ),
    # ---- Goal 4: Precision detection & mapping ------------------------------
    "precision_detection": (
        "How can remote sensing technologies—UAV-mounted multispectral and "
        "hyperspectral cameras, thermal imaging, and satellite time-series "
        "(Sentinel-2, PlanetScope)—combined with machine-learning classifiers "
        "be used to detect and map Phelipanche spp. infestations in industrial "
        "tomato fields at early (pre-emergence) and symptomatic stages, and "
        "how can the resulting spatially explicit infestation maps drive "
        "site-specific management decisions (variable-rate herbicide "
        "application, targeted soil treatments) through GIS-based decision "
        "support systems?"
    ),
    # ---- Goal 5: Seed bank dynamics & depletion -----------------------------
    "seed_bank_dynamics": (
        "What are the key demographic parameters (seed production per "
        "attachment, seed longevity, depth-dependent germination, secondary "
        "dormancy cycling) governing the Phelipanche ramosa soil seed bank "
        "in Mediterranean tomato rotations, and how can mechanistic "
        "population models—parameterised from field data and validated "
        "against multi-year monitoring—predict seed-bank trajectories under "
        "different management scenarios (continuous tomato, rotation with "
        "non-hosts, trap-crop deployment, herbicide programmes)?"
    ),
    # ---- Goal 6: Host resistance in processing tomato -----------------------
    "host_resistance": (
        "What are the genetic bases and mechanisms of resistance and tolerance "
        "to Phelipanche ramosa in cultivated tomato (Solanum lycopersicum) and "
        "its wild relatives (S. pennellii, S. habrochaites), including "
        "reduced strigolactone exudation, post-attachment incompatibility, "
        "cell-wall reinforcement, and phytoalexin accumulation, and how "
        "can marker-assisted selection or CRISPR-based gene editing accelerate "
        "the introgression of these resistance traits into elite processing-"
        "tomato cultivars adapted to Mediterranean conditions?"
    ),
}

# ---------------------------------------------------------------------------
# Specialist Fields
# ---------------------------------------------------------------------------
BROOMRAPE_SPECIALIST_FIELDS = [
    # --- Parasitic weed biology (core) ---
    "parasitic plant biology (Orobanchaceae)",
    "strigolactone signalling and germination stimulants",
    "parasite–host plant interactions",
    "parasitic weed seed bank ecology",
    "Orobanchaceae taxonomy and population genetics",
    # --- Chemical control ---
    "herbicide resistance mechanisms (ALS inhibitors)",
    "pre-emergence and post-emergence herbicide strategies",
    "novel herbicide modes of action and experimental molecules",
    "plant growth regulators (ethylene, gibberellin, and ABA pathways)",
    "herbicide safeners, adjuvants, and formulation science",
    # --- Biological and cultural control ---
    "trap and catch crops for broomrape management",
    "soil solarisation and biofumigation",
    "biological control of parasitic weeds (Fusarium, mycorrhiza)",
    "allelopathy and root exudate ecology",
    "crop rotation design for parasitic weed suppression",
    # --- Host resistance and breeding ---
    "tomato genetics and molecular breeding",
    "CRISPR and gene-editing technologies for crop improvement",
    "wild Solanum germplasm and pre-breeding",
    # --- Tomato agronomy ---
    "industrial tomato production systems",
    "Mediterranean agronomy and climate adaptation",
    "drip irrigation and fertigation management",
    "Solanaceae crop physiology",
    # --- Precision agriculture ---
    "remote sensing for parasitic weed detection",
    "hyperspectral and thermal imaging of crop stress",
    "GIS mapping and spatial decision support",
    "precision herbicide application technology",
    # --- Quantitative methods ---
    "experimental design for parasitic weed trials",
    "spatial analysis of broomrape distribution patterns",
    "population dynamics modelling (seed bank demography)",
    "dose–response modelling and bioassays",
    "Bayesian analysis of multi-environment trials",
]

# ---------------------------------------------------------------------------
# Preferred Reasoning Types
# ---------------------------------------------------------------------------
_PREFERRED_REASONING = [
    ReasoningType.FIRST_PRINCIPLES,
    ReasoningType.SYSTEMS,
    ReasoningType.CAUSAL,
    ReasoningType.STATISTICAL,
    ReasoningType.EVOLUTIONARY,
    ReasoningType.SPATIAL,
    ReasoningType.ECOLOGICAL,
    ReasoningType.MECHANISTIC_MODELLING,
    ReasoningType.BAYESIAN,
    ReasoningType.MIXED_MODELS,
    ReasoningType.GEOSTATISTICAL,
    ReasoningType.SIMULATION,
    ReasoningType.ABDUCTIVE,
    ReasoningType.COUNTERFACTUAL,
]

# ---------------------------------------------------------------------------
# Profile object
# ---------------------------------------------------------------------------
PROFILE = ResearchProfile(
    name="Broomrape × Industrial Tomato",
    description=(
        "Research profile for the management of parasitic weeds of the genus "
        "Phelipanche (broomrape), primarily P. ramosa and P. aegyptiaca, in "
        "processing-tomato production under Mediterranean-type climates. "
        "Covers herbicide resistance and alternative chemistries, integrated "
        "management (chemical × biological × cultural × precision ag), "
        "strigolactone-mediated germination ecology, remote-sensing-based "
        "detection and mapping, soil seed-bank population dynamics, and "
        "host-plant resistance breeding. Quantitative emphasis on GLMMs, "
        "Bayesian hierarchical models, geostatistics, mechanistic population "
        "models, and dose–response analysis."
    ),
    research_goals=_RESEARCH_GOALS,
    specialist_fields=BROOMRAPE_SPECIALIST_FIELDS,
    preferred_reasoning_types=_PREFERRED_REASONING,
    default_goal_key="als_resistance",
)
