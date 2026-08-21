#!/usr/bin/env python3
# 监测最新 Actions run：打印每步状态；若失败则读取诊断 issue 的错误日志。
import os, sys, json, time, urllib.request
API="https://api.github.com"; REPO="wx0373163/hrbu-grade-analyzer"
TOKEN=os.environ.get("GITHUB_TOKEN")
H={"Authorization":f"token {TOKEN}","Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"}
def get(p):
    r=urllib.request.Request(f"{API}{p}",headers=H)
    return json.loads(urllib.request.urlopen(r,timeout=60).read().decode())
def main():
    runs=get(f"/repos/{REPO}/actions/runs")["workflow_runs"]
    run=runs[0]; run_id=run["id"]
    print("监测 run:",run_id,"created:",run["created_at"],flush=True)
    deadline=time.time()+26*60
    jobs=[]
    while time.time()<deadline:
        r=get(f"/repos/{REPO}/actions/runs/{run_id}")
        st,con=r["status"],r.get("conclusion")
        try: jobs=get(f"/repos/{REPO}/actions/runs/{run_id}/jobs")["jobs"]
        except Exception: jobs=[]
        summ=" | ".join(f"{j['name'].split()[0]}:{j['status']}/{j.get('conclusion')}" for j in jobs)
        print(f"[{time.strftime('%H:%M:%S')}] {st}/{con} :: {summ}",flush=True)
        if st=="completed":
            print("=== 步骤明细 ===",flush=True)
            for j in jobs:
                print(f"  JOB {j['name']}:",flush=True)
                for s in j.get("steps",[]):
                    mark="OK" if s.get("conclusion")=="success" else ("FAIL" if s.get("conclusion")=="failure" else "?")
                    print(f"    [{mark}] {s['name']}",flush=True)
            if con=="failure":
                try:
                    iss=get(f"/repos/{REPO}/issues?state=all&per_page=15")
                    for i in iss:
                        if i.get("title","").startswith("[CI]"):
                            print(f"\n=== 诊断 ISSUE: {i['title']} ===",flush=True)
                            print(i.get("body","")[:5000],flush=True)
                except Exception as e:
                    print("读取 issue 失败:",e,flush=True)
            print(f"\n运行页面: https://github.com/{REPO}/actions/runs/{run_id}",flush=True)
            sys.exit(0)
        time.sleep(30)
    print("超时未结束，请稍后查看: https://github.com/%s/actions/runs/%s"%(REPO,run_id),flush=True)
if __name__=="__main__": main()
