from __future__ import annotations
from pathlib import Path

class KnowledgeBase:
    """Tiered, on-demand retrieval. SKILL.md routes; knowledge files carry detail."""
    def __init__(self, root: str|Path):
        self.root=Path(root)/"knowledge"
    def search(self, query: str, limit: int=3) -> list[dict]:
        q=set(query)
        hits=[]
        if not self.root.exists(): return hits
        for p in self.root.rglob("*.md"):
            try: txt=p.read_text(encoding="utf-8")
            except Exception: continue
            score=sum(1 for ch in set(txt) if ch in q)
            # keyword boost
            for kw in ["依恋","Gottman","冲突","暧昧","约会","分手","复合","相亲","冷淡","NVC","CBT"]:
                if kw in query and kw in txt: score+=20
            tier="A/B" if "psychology" in str(p) else ("C" if "scripts" in str(p) or "cases" in str(p) or "tactics" in str(p) else "B")
            hits.append({"path":str(p.relative_to(self.root.parent)),"tier":tier,"score":score,"snippet":txt[:180].replace("\n"," ")})
        hits.sort(key=lambda x:-x["score"])
        return hits[:limit]
