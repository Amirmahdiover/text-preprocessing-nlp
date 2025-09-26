import srt, json, re
from pathlib import Path

def clean_line(s: str):
    s = re.sub(r"</?[^>]+>", " ", s)      # drop HTML tags
    s = re.sub(r"\[[^\]]+\]", " ", s)     # drop [notes]
    s = re.sub(r"♪+", " ", s)
    return " ".join(s.split()).strip()

def load_srt(path: Path, lang="en"):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    subs = list(srt.parse(raw))
    rows = []
    for i, sub in enumerate(subs, 1):
        merged = " ".join(line.strip() for line in sub.content.splitlines())
        duration_ms = int((sub.end - sub.start).total_seconds() * 1000)
        rows.append({
            "index": i,
            f"text_{lang}": clean_line(merged),   # language-specific key
            f"text_{lang}_raw": sub.content
        })
    return rows

def write_json(rows, out_path: Path, indent=2):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    data_dir = Path("dataset")
    out_dir  = data_dir / "out"

    # detect English & Persian episode 1
    pat = re.compile(r"S0*1E0*1", re.IGNORECASE)
    eng_files = [p for p in data_dir.glob("*.srt") if pat.search(p.stem) and "eng" in p.stem.lower()]
    fa_files  = [p for p in data_dir.glob("*.srt") if pat.search(p.stem) and ("fa" in p.stem.lower() or "per" in p.stem.lower() or "farsi" in p.stem.lower())]

    if not eng_files or not fa_files:
        raise SystemExit("❌ Could not find both English & Persian S01E01 subtitles.")

    eng_path = sorted(eng_files)[0]
    fa_path  = sorted(fa_files)[0]
    print(f"Converting: {eng_path.name} + {fa_path.name}")

    eng_rows = load_srt(eng_path, lang="en")
    fa_rows  = load_srt(fa_path, lang="fa")

    # align by index
    combined = []
    for e, f in zip(eng_rows, fa_rows):
        combined.append({
            "index": e["index"],
            "text_en": e["text_en"],
            "text_fa": f.get("text_fa", ""),
            "text_en_raw": e["text_en_raw"],
            "text_fa_raw": f.get("text_fa_raw", "")
        })

    out_path = out_dir / f"{eng_path.stem}_with_fa.json"
    write_json(combined, out_path)
    print(f"✅ JSON with English + Persian saved at: {out_path.resolve()}")
