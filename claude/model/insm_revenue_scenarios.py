# Insmed Brinsupri patient-stock / revenue scenario model (assumption-driven)
hist = {"Q3'25":28.1,"Q4'25":144.6,"Q1'26":207.9,"Q2'26":309.1,"Q3'26":400.1}
wac=88000; gtn=0.27
net_q = wac*(1-gtn)/4
print("net price per patient-quarter: $%.0f" % net_q)
prev=None
for k,v in hist.items():
    pe=v*1e6/net_q
    print(f"{k}: rev ${v:.1f}M  patient-equiv {pe:,.0f}  " + (f"q/q +${v-prev:.1f}M" if prev else ""))
    prev=v

def run(name, q4_26, incs, price_up=0.03):
    # incs: list of quarterly increments for Q1'27..Q4'29 (12 quarters) in $M before price
    qs=[q4_26]; base=q4_26
    out={}
    for i,inc in enumerate(incs):
        base=base+inc
        yr=2027+i//4
        price=(1+price_up)**(yr-2026)
        qs.append(base*price)
    y26 = 917.1+q4_26
    y27=sum(qs[1:5]); y28=sum(qs[5:9]); y29=sum(qs[9:13])
    print(f"{name}: 2026 {y26/1000:.2f}B | 2027 {y27/1000:.2f}B | 2028 {y28/1000:.2f}B | 2029 {y29/1000:.2f}B | Q4'29 run-rate {qs[12]*4/1000:.1f}B")
    return y26,y27,y28,y29

# Base: Q4'26 480 (+80), Q1 seasonal +55, others +90
base_incs=[55,90,90,90, 60,90,90,90, 60,90,90,90]
# Bear: increments decay ~15% per quarter from 70
bear_incs=[40]+[70*(0.85**i) for i in range(1,12)]
# Bull: DTC lifts increments to 120 from Q2'27
bull_incs=[70,110,120,120, 90,120,120,120, 90,120,120,120]
B=run("Base",480,base_incs)
R=run("Bear",455,bear_incs,0.02)
U=run("Bull",500,bull_incs,0.04)
print("Street: GS 2027 Brinsupri 2.7B; consensus total rev 2027 2.98B; William Blair 2029 ~3.3B (pre-Q3)")
