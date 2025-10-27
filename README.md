# CAL HACK 12.0 : ARCANA - MULTI AGENT INTERIOR DESIGN PLATFORM

Transform any room photo or sketch into a photorealistic, purchasable design in seconds.
Arcana uses Anthropic’s Claude multi-agent architecture, ControlNet image generation, and contextual RAG retrieval to deliver professional-grade interior design intelligence fast, accurate, and visually stunning



## Hackers: 
- Fozhan Babaeiyan Ghamsari 
- My Lu


## OVERVIEW
Arcana reimagines interior design through collaborating AI agents that handle every step of the process — from understanding your style to recommending real furniture and optimizing layouts for your space and budget.
- Upload a photo, describe your vision, and Arcana’s AI designer team handles the rest.

## HOW IT WORK 

Multi-Agent Claude Architecture

- Orchestrator (Claude Opus 4): Coordinates all agents and synthesizes results.

- Style Analysis Agent (Claude Sonnet 4): Extracts color palettes, aesthetics, and spatial constraints.

- Product Recommendation Agent (Claude Sonnet 4): Queries a furniture knowledge graph via contextual RAG.

- Layout Optimization Agent (Claude Sonnet 4): Calculates spatial arrangements and clearances.

- Budget Management Agent (Claude Sonnet 4): Tracks costs and suggests alternatives.

**ControlNet Integration**
Generate photorealistic, style-specific designs from room photos or sketches.
Users can instantly visualize multiple design variations — modern, minimalist, Scandinavian, and more.

**Contextual Retrieval (RAG) System**
Furniture recommendations use contextual embeddings that improve retrieval accuracy by up to 67%.
Each item is explained in design context (“Fits 12x15ft rooms, minimalist aesthetic, 5-year warranty”).


### TECH STACK:
- AI & Orchestration : Anthropic Claude Opus 4 + Sonnet 4
- Image Generation : ControlNet + Stable Diffusion
- Retrieval and Storage  : ElasticSearch (vector + BM25 hybrid), Neo4j PKG
- Backend : FastAPI(python)
- Frontend : React + Tailwind

---
## HOW TO RUN | SET UP INSTRUCTION
1. Clone the repo
``` bash
    git clone https://github.com/arcana-ai/arcana.git
    cd arcana
```

2. Install dependencies
``` bash
pip install -r requirements.txt
npm install
```

3. set enviroment variable
```
export CLAUDE_API_KEY=your_key
export ELASTIC_URL=your_elastic_instance
export CONTROLNET_URL=your_controlnet_endpoint
```

4. Run backend and frontend
```
# Backend
uvicorn app.main:app --reload

# Frontend
npm run dev
```