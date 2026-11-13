# TARS 역산 DCF·시나리오. 기준: 2026-11-12 종가 $76.89, 기본주식 49.3M, 현금+유가증권 $309.6M, 차입 $75M, Alkeus 조건부대가 $85.7M (2026-09-30).
# 가정은 함수 인자로 드러냄(피크 매출·도달 연도·성숙기 EBIT 마진·특허만료(LOE)·WACC). 결과는 추정이며 사실이 아님.
# Reverse DCF for XDEMVY standalone (US). All $M. Assumptions explicit.
import itertools
PRICE=76.89; SH=49.3; CASH=309.6; DEBT=75.0; CONT=85.7
MCAP=PRICE*SH; EV=MCAP-CASH+DEBT
print(f'MktCap {MCAP:,.0f}  EV {EV:,.0f}  EV+contingent {EV+CONT:,.0f}')
for s,n in [(722.5,'2026E guide mid'),(920,'2027 cons'),(1124,'2028 cons')]: print(f'EV/{n} {EV/s:.1f}x')
def npv(peak, peak_year=2031, wacc=0.10, mature_margin=0.50, loe=2038, tax=0.21, nol=1000):
    sales={2026:722.5}
    yrs=range(2027,2046)
    for y in yrs:
        if y<=peak_year:
            # geometric ramp from 2026 to peak
            sales[y]=722.5*(peak/722.5)**((y-2026)/(peak_year-2026))
        elif y<loe: sales[y]=peak
        elif y==loe: sales[y]=peak*0.5
        elif y==loe+1: sales[y]=peak*0.2
        else: sales[y]=peak*0.1*(0.8**(y-loe-2))
    marg={2027:0.15,2028:0.28,2029:0.38,2030:0.45}
    v=0; nolleft=nol
    for i,y in enumerate(yrs, start=1):
        m=marg.get(y,mature_margin)
        ebit=sales[y]*m
        taxable=max(0,ebit-nolleft); nolleft=max(0,nolleft-ebit)
        fcf=ebit-taxable*tax - 0.0*sales[y]
        v+=fcf/(1+wacc)**(i-0.5)  # mid-year from 2027
    return v
print('\nXDEMVY standalone NPV ($M) by peak sales / WACC  (mature EBIT margin 50%, peak 2031, LOE 2038)')
for w in [0.09,0.10,0.11]:
    print(f'WACC {w:.0%}: '+'  '.join(f'peak {p/1000:.1f}B -> {npv(p,wacc=w):,.0f}' for p in [1000,1200,1500,2000,2500]))
# implied peak at market EV (pipeline valued at -X: assume pipeline net = 0, -500 (costs > value))
import math
def implied(target, **kw):
    lo,hi=300,5000
    for _ in range(60):
        mid=(lo+hi)/2
        if npv(mid,**kw)<target: lo=mid
        else: hi=mid
    return mid
for pipe in [0,-500,+500]:
    print(f'pipeline net value {pipe:+}: implied XDEMVY peak (WACC10%) = {implied(EV+CONT-pipe):,.0f}')
print('sensitivity: margin 45% ->',round(implied(EV+CONT,mature_margin=0.45)),' LOE 2035 ->',round(implied(EV+CONT,loe=2035)),' LOE 2032 ->',round(implied(EV+CONT,loe=2032)))

print('\n--- peak timing sensitivity (WACC10%, margin 50%/55%, LOE2038) ---')
NETADJ=CASH-DEBT-CONT
for m in [0.50,0.55]:
    for p,py in [(2000,2035),(2000,2033),(2000,2031),(2300,2031),(2600,2031)]:
        v=npv(p,peak_year=py,mature_margin=m)
        print(f'margin {m:.0%} peak {p} in {py}: XDEMVY NPV {v:,.0f} -> per share (pipeline 0) {(v+NETADJ)/SH:,.1f}')
print('\n--- scenarios ---')
sc={'Bear':dict(p=1300,py=2030,m=0.45,loe=2035,pipe=-600),
    'Base':dict(p=2200,py=2031,m=0.55,loe=2038,pipe=0),
    'Bull':dict(p=2800,py=2032,m=0.55,loe=2038,pipe=800)}
for k,s in sc.items():
    v=npv(s['p'],peak_year=s['py'],mature_margin=s['m'],loe=s['loe'])
    print(k,s,'XDEMVY',round(v),'per share',round((v+s['pipe']+NETADJ)/SH,1))

print('\n--- no-growth floor: sales flat at 2027 level ---')
for m in [0.40,0.45]:
    for loe in [2035,2038]:
        v=npv(955,peak_year=2027,mature_margin=m,loe=loe)
        print(f'flat $955M from 2027, margin {m:.0%}, LOE {loe}: NPV {v:,.0f} -> per share (pipeline 0) {(v+NETADJ)/SH:,.1f}; pipeline -600 -> {(v-600+NETADJ)/SH:,.1f}')
print('\nmarket cap history: Nov-2025 ~', round(79.96*42.6), 'Nov-2026', round(76.89*49.3))
print('EV/annualized quarterly sales: Q3-25', round((79.96*42.6-420+75)/(118.7*4),1),' Q3-26', round(EV/(194.6*4),1))
