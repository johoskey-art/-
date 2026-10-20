#!/usr/bin/env python3
import csv, math, pathlib
root=pathlib.Path(__file__).resolve().parent
rows=list(csv.DictReader((root/"CYCLE_MASTER.csv").open(encoding="utf-8")))
def q(a,p):
 a=sorted(a); z=(len(a)-1)*p; i=int(z); return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(z-i)
def st(a): return [len(a),sum(a)/len(a),q(a,.5),q(a,.25),q(a,.75),min(a),max(a)]
def main():
 grid=[["cycle_id","sample_origin","stock_name","ticker","k","j","low_date","low_adj_close","peak_date","peak_adj_close","R_total","stage_ratio_R_pow_j_over_k","stage_price"]]
 for i,r in enumerate(rows,1):
  for k in (5,7):
   for j in range(k+1):
    g=float(r["R_total"])**(j/k); grid.append([i,r["sample_origin"],r["stock_name"],r["ticker"],k,j,r["corrected_low_date"],r["adjusted_low_close"],r["corrected_peak_date"],r["adjusted_peak_close"],r["R_total"],g,float(r["adjusted_low_close"])*g])
 with (root/"LOG_5_7_ALL_STAGES.csv").open("w",newline="",encoding="utf-8") as f: csv.writer(f).writerows(grid)
 h=["sample_origin","weighting","k","j","cycle_count","stage_ratio_mean","stage_ratio_median","stage_ratio_p25","stage_ratio_p75","stage_ratio_min","stage_ratio_max","adjacent_step_mean","notes"]; out=[h]
 groups={"LEGACY38":[r for r in rows if r["sample_origin"]=="LEGACY_SELECTED_SAMPLE"],"SEMICONDUCTOR_REAUDIT_2":[r for r in rows if r["sample_origin"]=="NEW_SEMICONDUCTOR_REAUDIT"],"EXPANDED40_PROVISIONAL":rows}
 for lab,rs in groups.items():
  for w in ("cycle_equal","company_equal"):
   for k in (5,7):
    for j in range(k+1):
     v=[float(r["R_total"])**(j/k) for r in rs]
     if w=="company_equal":
      d={}
      for r,x in zip(rs,v): d.setdefault(r["ticker"],[]).append(x)
      v=[sum(x)/len(x) for x in d.values()]
     out.append([lab,w,k,j,*st(v),sum(float(r["R_total"])**(1/k) for r in rs)/len(rs),"same-stage metric; do not exponentiate adjacent mean"])
 with (root/"STAGE_AVERAGES.csv").open("w",newline="",encoding="utf-8") as f: csv.writer(f).writerows(out)
 print("reproduced",len(rows),"cycles")
if __name__=="__main__": main()
