from __future__ import annotations
from pathlib import Path

TIER_MAP={"knowledge/psychology":"Tier A/B scientific-and-framework","brain/psychology":"Tier A/B scientific-and-framework",
"knowledge/relationship":"Tier B relationship-framework","brain/relationship":"Tier B relationship-framework",
"brain/strategy":"Tier B/C strategy","knowledge/scripts":"Tier C practical-scripts","knowledge/cases":"Tier C practical-cases",
"knowledge/tactics":"Tier C practical-tactics","brain/goutoujunshi":"Tier C ethics-translated","brain/evidence":"Tier A/B evidence-discipline"}

class KnowledgeBase:
    """Tiered retrieval whose results are actually injected into LLM prompts.
    Tier C is examples/tactics only, never scientific fact."""
    def __init__(self, root: str|Path):
        self.base=Path(root)
    def _tier(self, path: Path) -> str:
        s=str(path)
        for k,v in TIER_MAP.items():
            if k in s: return v
        return "Tier B relationship-framework"
    def search(self, query: str, limit: int=3) -> list[dict]:
        hits=[]; roots=[self.base/"knowledge", self.base/"brain"]
        for r in roots:
            if not r.exists(): continue
            for fp in r.rglob("*.md"):
                try: txt=fp.read_text(encoding="utf-8")
                except Exception: continue
                score=0
                for kw in ["依恋","Gottman","石墙","冲突","暧昧","约会","分手","复合","相亲","冷淡","NVC","空间","边界"]:
                    if kw in query and kw in txt: score+=25
                    if kw in txt and kw in fp.name: score+=5
                score+=sum(1 for ch in set(txt[:2000]) if ch in set(query))
                hits.append({"path":str(fp.relative_to(self.base)),"tier":self._tier(fp),"score":score,"snippet":txt[:420].replace("\n"," ")})
        hits.sort(key=lambda x:-x["score"])
        return hits[:limit]
    def prompt_block(self, hits: list[dict]) -> str:
        lines=[]
        for h in hits:
            lines.append(f"[{h['tier']}] source={h['path']} :: {h['snippet']}")
        return "\n".join(lines)
