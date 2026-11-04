# Insmed valuation scenarios (all assumptions labeled)
price=104.44; mcap=22.91; ev=22.50; sh_now=219.3
def scen(name, brin27, brin28, exus27, exus28, arik27, arik28, gm, opex27, opex28, sbc, tax, sh28, pe, ke=0.10):
    rev27=brin27+exus27+arik27; rev28=brin28+exus28+arik28
    ebit27=rev27*gm-opex27; ebit28=rev28*gm-opex28
    ni27=(ebit27+sbc)*(1-tax); ni28=(ebit28+sbc)*(1-tax)
    eps27=ni27/0.228; eps28=ni28/sh28
    tp=eps28*pe/(1+ke)
    print(f"{name}: rev27 {rev27:.2f}B rev28 {rev28:.2f}B | EBIT27 {ebit27:.2f} EBIT28 {ebit28:.2f} | nonGAAP EPS27 ${eps27:.2f} EPS28 ${eps28:.2f} | PE {pe}x -> TP ${tp:.0f} ({tp/price-1:+.0%})")
    return tp
b=scen("Base",2.76,4.24,0.05,0.15,0.56,0.72,0.87,2.60,2.80,0.23,0.15,0.232,25)
u=scen("Bull",3.09,5.15,0.07,0.20,0.60,0.85,0.88,2.70,2.95,0.23,0.15,0.232,28)
# Bear: valued on EV/Sales 4.5x 2027E
rev27_bear=2.35+0.03+0.52
tp_bear=(rev27_bear*4.5+0.4)/0.228
print(f"Bear: rev27 {rev27_bear:.2f}B x4.5 EV/S -> TP ${tp_bear:.0f} ({tp_bear/price-1:+.0%})")
# Floor: run-rate only, 4x EV/S
rr=(400.1+124.4)*4/1000
floor=(rr*4+0.4)/0.220
print(f"Floor (no growth, run-rate {rr:.2f}B x4): ${floor:.0f} ({floor/price-1:+.0%})")
pw=0.25*tp_bear+0.5*b+0.25*u
print(f"Prob-weighted (25/50/25): ${pw:.0f} ({pw/price-1:+.0%})")
# market-implied
print(f"EV/consensus 2027 sales: {ev/2.98:.1f}x ; P/E on our base 2028 NI: {mcap/((( (4.24+0.15+0.72)*0.87-2.80)+0.23)*0.85):.1f}x")
# sensitivity: P/E 20/25/30 on base EPS28
eps28=(((4.24+0.15+0.72)*0.87-2.80)+0.23)*0.85/0.232
for pe in (20,25,30):
    print(f"  PE {pe}x: ${eps28*pe/1.1:.0f}")
# EPS sensitivity: +$100M revenue
print(f"+$100M rev -> +${0.1*0.87*0.85/0.232:.2f} EPS (2028 basis)")
