"""Runner test suite: parser, confidence semantics, resume, dedup, call cap.
No API calls - a fake client returns canned responses.
"""
import sys, json, types, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import investigator as I
import analyze as A

fails = []
def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  -- {detail}" if detail and not cond else ""))
    if not cond: fails.append(name)

print("=== §4 confidence semantics ===")
# A high-confidence "no" must map to a LOW probability of yes.
check("high-confidence 'no' -> low P(yes)",
      abs(A.to_prob({"answer":"no","confidence":90}) - 0.10) < 1e-9,
      f"got {A.to_prob({'answer':'no','confidence':90})}")
check("high-confidence 'yes' -> high P(yes)",
      abs(A.to_prob({"answer":"yes","confidence":90}) - 0.90) < 1e-9)
check("insufficient_evidence -> abstention score, ignoring confidence",
      A.to_prob({"answer":"insufficient_evidence","confidence":97}, 0.5) == 0.5)
check("a confident wrong 'no' is scored as a BAD forecast",
      A.brier([A.to_prob({"answer":"no","confidence":90})], [1]) > 0.7,
      f"brier={A.brier([A.to_prob({'answer':'no','confidence':90})],[1]):.3f}")

print("\n=== §4 parser / clamping ===")
ans = I._clamp({"A":{"told":{"answer":"yes","confidence":150}},
                "attribution":{"A":70,"B":70,"none":0},"episode":{}}, ["A"])
check("confidence clamped to 100", ans["A"]["told"]["confidence"] == 100)
check("attribution renormalised to 100", sum(ans["attribution"].values()) == 100)
z = I._clamp({"attribution":{"A":0,"B":0,"none":0},"episode":{}}, ["A","B"])
check("all-zero attribution -> all mass on 'none'", z["attribution"]["none"] == 100)
sch = I._schema(["A","B"])
check("no minimum/maximum in schema (API rejects them)",
      "minimum" not in json.dumps(sch) and "maximum" not in json.dumps(sch))
check("three-way answer enum preserved",
      set(sch["properties"]["A"]["properties"]["told"]["properties"]["answer"]["enum"])
      == {"yes","no","insufficient_evidence"})

print("\n=== §4 cache gating ===")
import inspect
check("cache_control only when reps>1", "if n_reps > 1" in inspect.getsource(I.ask))

print("\n=== §5 retries, duplicates, resumption ===")
calls = {"n": 0}
def fake_client(fail_times=0, always_fail=False):
    c = types.SimpleNamespace()
    def create(**kw):
        calls["n"] += 1
        if always_fail or calls["n"] <= fail_times:
            raise RuntimeError("schema error 400")
        body = json.dumps({
            "A":{k:{"answer":"yes","confidence":80} for k,_ in I.AGENT_ITEMS},
            "B":{k:{"answer":"no","confidence":70} for k,_ in I.AGENT_ITEMS},
            "attribution":{"A":80,"B":10,"none":10},
            "episode":{k:{"answer":"no","confidence":60} for k,_ in I.EPISODE_ITEMS}})
        u = types.SimpleNamespace(input_tokens=100, output_tokens=50,
                                  cache_read_input_tokens=0, cache_creation_input_tokens=0)
        return types.SimpleNamespace(
            content=[types.SimpleNamespace(type="text", text=body)], usage=u)
    c.messages = types.SimpleNamespace(create=create)
    return c

t = I.CallTracker()
calls["n"] = 0
rs = I.run_package(fake_client(), "m", "e1", "V1", "pkg", ["A","B"], 3, t)
check("k=3 produces exactly 3 observations", len(rs) == 3, f"got {len(rs)}")
check("rep ids are 0,1,2 and unique", sorted(r.rep for r in rs) == [0,1,2])
check("all attached to the right episode/view",
      all(r.episode_id=="e1" and r.view=="V1" for r in rs))

calls["n"] = 0
rs = I.run_package(fake_client(fail_times=1), "m", "e2", "V1", "pkg", ["A","B"], 1, t)
check("transient failure then success = ONE observation, not two", len(rs) == 1)
check("retry did not duplicate the observation", bool(rs[0].answers))

calls["n"] = 0
rs = I.run_package(fake_client(always_fail=True), "m", "e3", "V1", "pkg", ["A","B"], 1, t)
check("systematic failure recorded as missing, not silently valid",
      len(rs) == 1 and not rs[0].answers)
check("retries bounded at MAX_RETRIES+1 attempts", calls["n"] == I.MAX_RETRIES + 1,
      f"{calls['n']} attempts")

calls["n"] = 0
rs = I.run_package(fake_client(), "m", "e4", "V1", "pkg", ["A","B"], 3, t, reps=[2])
check("resume fills ONLY the missing rep", len(rs)==1 and rs[0].rep==2)

print("\n=== §5 dedup / resumption via the manifest ===")
import run_judgement as RJ
tmp = Path(tempfile.mkdtemp())
f = tmp/"out.jsonl"
f.write_text("\n".join(json.dumps({"episode_id":"e1","view":"V1","model":"m","rep":0,
             "answers":{"A":{}},"usage":{},"cached":False}) for _ in range(1)) + "\n" +
             json.dumps({"episode_id":"e1","view":"V1","model":"m","rep":1,
                         "answers":{},"usage":{"error":"x"},"cached":False}) + "\n")
have = RJ.existing_cells([f])
check("valid cell counted as collected", ("e1","V1","m",0) in have)
check("MALFORMED cell NOT counted as collected", ("e1","V1","m",1) not in have)
dupe = f.read_text() + f.read_text()
f2 = tmp/"dupe.jsonl"; f2.write_text(dupe)
check("duplicate lines collapse to one cell", len(RJ.existing_cells([f2])) == 1)

print("\n=== §7 clustering ===")
check("bootstrap clusters by episode",
      "clusters" in inspect.signature(A.bootstrap_ci).parameters)
check("paired_difference pairs within episode",
      "episode" in inspect.getsource(A.paired_difference))

print(f"\n{len(fails)} failure(s)" + (": " + ", ".join(fails) if fails else ""))
sys.exit(1 if fails else 0)
