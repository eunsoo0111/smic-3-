import json, sys, time, importlib.util
spec = importlib.util.spec_from_file_location("dc", sys.argv[1] + "/scripts/dart_contracts.py"); dc = importlib.util.module_from_spec(spec); spec.loader.exec_module(dc)
p = sys.argv[2]; d = json.load(open(p))
for c in d["contracts"]:
    if not c.get("text"):
        for i in range(3):
            try:
                c["text"] = dc.doc_text(c["rcpNo"]); break
            except Exception as e:
                time.sleep(2)
        time.sleep(0.5)
json.dump(d, open(p, "w"), ensure_ascii=False)
print(sum(1 for c in d["contracts"] if c.get("text")), "of", len(d["contracts"]))
