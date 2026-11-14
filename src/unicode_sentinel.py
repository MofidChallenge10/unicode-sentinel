"""Detect risky Unicode code points in text files."""
import argparse,json,sys,unicodedata
from pathlib import Path
BIDI={0x061C,0x200E,0x200F,*range(0x202A,0x202F),*range(0x2066,0x206A)}
ZERO_WIDTH={0x200B,0x200C,0x200D,0x2060,0xFEFF}
def scan(text):
    findings=[]
    for line_no,line in enumerate(text.splitlines(),1):
        for col,ch in enumerate(line,1):
            cp=ord(ch); category=unicodedata.category(ch)
            if cp in BIDI: kind="bidi-control"
            elif cp in ZERO_WIDTH: kind="zero-width"
            elif category=="Cc" and ch not in "\t": kind="control"
            elif category=="Cf": kind="format"
            else: continue
            findings.append({"line":line_no,"column":col,"codepoint":f"U+{cp:04X}","name":unicodedata.name(ch,"UNKNOWN"),"kind":kind})
    return findings
def main(argv=None):
    p=argparse.ArgumentParser(description="Locate invisible Unicode format/control characters.")
    p.add_argument("files",nargs="+"); p.add_argument("--json",action="store_true"); a=p.parse_args(argv)
    results={}; failed=False
    for file in a.files:
        try: data=Path(file).read_text(encoding="utf-8")
        except (OSError,UnicodeError) as e: results[file]=[{"error":str(e)}]; failed=True; continue
        results[file]=scan(data); failed |= bool(results[file])
    if a.json: print(json.dumps(results,indent=2,ensure_ascii=False))
    else:
        for file,items in results.items():
            print(f"{file}: {len(items)} finding(s)")
            for x in items: print(f"  {x.get('line')}:{x.get('column')} {x.get('codepoint')} {x.get('name')} [{x.get('kind')}]")
    return int(failed)
if __name__=="__main__": sys.exit(main())
