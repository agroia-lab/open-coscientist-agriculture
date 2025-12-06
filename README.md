# 🌱 Open CoScientist Agents: Agriculture Edition

A multi-agent AI system for **agricultural research** and scientific discovery, specialized for weed science, crop protection, and sustainable farming. Based on [Open CoScientist Agents](https://github.com/conradry/open-coscientist-agents) and Google DeepMind's [AI co-scientist](https://arxiv.org/abs/2502.18864).

Built with LangGraph, [GPT Researcher](https://github.com/assafelovic/gpt-researcher), GPT-5.1, and Claude Opus 4.5.

![App Demo](assets/app_demo.gif)

## 🎯 Agricultural Focus

This fork is optimized for agricultural research with:

- **10 Specialist Fields**: Weed science, agronomy, plant pathology, soil science, herbicide physiology, parasitic plant biology, integrated pest management, crop physiology, plant biochemistry, agricultural ecology
- **Agricultural Agent Role**: Configured for crop protection and sustainable farming research
- **Academic Search**: Tavily with PubMed, ScienceDirect, and agricultural journal access

## 📋 Example Research Output

See our first research report on **Phelipanche ramosa (broomrape) control in industrial tomato**:
- [`Phelipanche_FULL_Research_Report.md`](Phelipanche_FULL_Research_Report.md) - 76,000+ characters covering:
  - ALS herbicide resistance mechanisms
  - Maleic hydrazide and prohexadione-calcium efficacy
  - Trial design for Chile's Central Valley
  - 9 testable research hypotheses

## Key Features

### Multi-Agent Architecture
- **Literature Review Agent**: Decomposes research goals and conducts comprehensive agricultural literature analysis
- **Generation Agents**: Create novel hypotheses using multiple reasoning approaches (causal, systems, statistical, etc.)
- **Reflection Agents**: Perform deep verification and causal reasoning analysis
- **Evolution Agents**: Refine hypotheses based on feedback and competition
- **Meta-Review Agent**: Synthesizes insights across research directions
- **Supervisor Agent**: Orchestrates the research workflow
- **Final Report Agent**: Generates comprehensive research summaries

### Tournament-Style Hypothesis Competition
- **ELO Rating System**: Ranks hypotheses through head-to-head analysis
- **Debate Transcripts**: Records why one hypothesis outperforms another
- **Win-Loss Statistics**: Tracks performance across evaluation rounds
- **Hypothesis Evolution**: Shows how ideas improve through refinement

## Installation

### Prerequisites
- Python 3.11+
- macOS (tested on M1), Linux, or Windows

### Install from Source
```bash
git clone https://github.com/lfleon9b/open-coscientist-agriculture.git
cd open-coscientist-agriculture
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## Configuration

### Environment Variables
Create a `.env` file with your API keys:

```bash
# Required
OPENAI_API_KEY="your-openai-key"
ANTHROPIC_API_KEY="your-anthropic-key"
TAVILY_API_KEY="your-tavily-key"

# Optional (for Google models)
GOOGLE_API_KEY="your-google-key"

# Optional (for PubMed Central direct access)
NCBI_API_KEY="your-ncbi-key"  # Free from https://www.ncbi.nlm.nih.gov/account/

# Optional (for monitoring)
LANGSMITH_API_KEY="your-langsmith-key"
LANGSMITH_PROJECT="your-project-name"
LANGSMITH_TRACING="true"
```

## Quick Start

### Run Agricultural Research
```python
import asyncio
from run_agriculture_research import main

# Edit GOAL in run_agriculture_research.py, then:
asyncio.run(main())
```

Or from command line:
```bash
source venv/bin/activate
export $(grep -v '^#' .env | xargs)
python run_agriculture_research.py
```

### Quick Test (Low Cost)
```bash
python quick_test.py  # ~$0.05-0.10
```

### Export Reports
```bash
python export_report.py
```

### Web Interface
```bash
cd app
pip install -r viewer_requirements.txt
streamlit run tournament_viewer.py
```

## Example Research Questions

### Weed Science
```python
GOAL = "What are the main herbicide resistance mechanisms in Palmer amaranth?"
```

### Parasitic Weeds
```python
GOAL = "What alternative herbicides show potential for Phelipanche ramosa control in tomato?"
```

### Integrated Pest Management
```python
GOAL = "How can cover crops reduce herbicide dependency in corn-soybean rotations?"
```

## Models Used

| Agent | Model | Purpose |
|-------|-------|---------|
| Literature Review | GPT-5.1 | Research decomposition |
| Hypothesis Generation | Claude Opus 4.5 + GPT-5.1 | Creative ideation |
| Reflection | Claude Opus 4.5 + GPT-5.1 | Deep verification |
| Meta Review | Claude Opus 4.5 | Synthesis |
| Final Report | Claude Opus 4.5 | Writing |
| Web Research | GPT-5.1 + Tavily | Literature search |

## Cost Estimates

| Run Type | Estimated Cost | Time |
|----------|---------------|------|
| Quick Test | $0.05-0.10 | 2-5 min |
| Full Research | $2-5 | 10-20 min |
| Complex Query | $5-15 | 30-60 min |

## Project Structure

```
open-coscientist-agriculture/
├── coscientist/           # Core agent system
│   ├── framework.py       # Main orchestration
│   ├── prompts/           # Agent prompts
│   └── researcher_config.json  # GPT-Researcher config
├── app/                   # Streamlit web interface
├── run_agriculture_research.py  # Main research script
├── quick_test.py          # Low-cost validation
├── export_report.py       # Report extraction
└── Phelipanche_FULL_Research_Report.md  # Example output
```

## Limitations

- **Paywalled Journals**: Cannot access full text of subscription journals (uses abstracts)
- **Rate Limits**: API rate limits may slow parallel execution
- **Cost**: Premium models (GPT-5.1, Opus 4.5) increase costs
- **Regional Data**: May have limited access to Chile-specific agricultural data

## Contributing

Contributions welcome! Areas of interest:
- Additional agricultural specialist fields
- Integration with agricultural databases (USDA, FAO)
- Support for local document ingestion
- Cost optimization strategies

## License

MIT License - see [LICENSE](LICENSE)

## Acknowledgments

- Based on [Open CoScientist Agents](https://github.com/conradry/open-coscientist-agents) by @conradry
- Inspired by Google DeepMind's [AI co-scientist](https://arxiv.org/abs/2502.18864)
- Built with [LangGraph](https://github.com/langchain-ai/langgraph), [GPT Researcher](https://github.com/assafelovic/gpt-researcher)
- Visualization by [Streamlit](https://streamlit.io/)

---

**🌾 Happy Researching!**
