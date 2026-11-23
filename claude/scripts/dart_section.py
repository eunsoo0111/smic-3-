import requests, re, json, sys, time
S = requests.Session(); H = {"User-Agent": "Mozilla/5.0"}
def section(t):
    url = f"https://dart.fss.or.kr/report/viewer.do?rcpNo={t['rcpNo']}&dcmNo={t['dcmNo']}&eleId={t['eleId']}&offset={t['offset']}&length={t['length']}&dtd=dart4.xsd"
    for i in range(4):
        try:
            r = S.get(url, headers=H, timeout=40); break
        except Exception: time.sleep(2)
    raw = r.content
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            txt = raw.decode(enc); break
        except Exception: continue
    txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S)
    txt = re.sub(r"</t[dh]>", " | ", txt); txt = re.sub(r"</tr>", "\n", txt); txt = re.sub(r"<br\s*/?>", "\n", txt)
    txt = re.sub(r"</p>", "\n", txt)
    txt = re.sub(r"<[^>]+>", "", txt); txt = re.sub(r"&nbsp;", " ", txt); txt = re.sub(r"[ \t]+", " ", txt); txt = re.sub(r"\n\s*\n+", "\n", txt)
    return txt
if __name__ == "__main__":
    toc = json.load(open(sys.argv[1])); ids = sys.argv[2].split(","); out = sys.argv[3]
    with open(out, "w") as f:
        for t in toc:
            if t["eleId"] in ids:
                f.write(f"\n\n######## {t['eleId']} {t['text']}\n"); f.write(section(t)); time.sleep(0.5)
    print("ok")
