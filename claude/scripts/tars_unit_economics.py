# TARS 병당 경제학·환자 퍼널. 2024~2025 병 수는 회사 공시, 2026E~2027E는 (가정) 병당 순가격으로 역산.
# Unit economics & funnel. $M, bottles in thousands. (가정) marked.
yrs=['2024','2025','2026E','2027E']
rev={'2024':180.1,'2025':451.4,'2026E':722.5,'2027E':955}
btl={'2024':163,'2025':400}
netpb_26=1.170  # $K per bottle (가정: 2025 Q4 $1.167K, GTN 43-45%, WAC +1~2%)
btl['2026E']=rev['2026E']/netpb_26
netpb_27=1.200  # (가정)
btl['2027E']=rev['2027E']/netpb_27
cogs={'2024':12.8,'2025':30.7,'2026E':0.07*722.5,'2027E':0.07*955}
sga={'2024':237.3,'2025':427.3,'2026E':612.5-40,'2027E':650-25}  # ex Alkeus/iRenix SG&A (가정: 2026 40M, 2027 25M)
print('year  bottles(k)  net/btl  sga/btl  cogs/btl  contrib/btl')
for y in yrs:
    b=btl[y]; print(f'{y:6} {b:8.0f}  {rev[y]/b*1000:7.0f}  {sga[y]/b*1000:7.0f}  {cogs[y]/b*1000:7.0f}  {(rev[y]-cogs[y]-sga[y])/b*1000:7.0f}')
# Medicare share
med={'2023':3.693,'2024':61.184,'2025':174.236}
print('Medicare claims share of bottles: 2024',round(61.184/163,3),' 2025',round(174.236/400,3))
print('Medicare claims growth 2025:',round(174.236/61.184,2),'x ; total bottles growth',round(400/163,2),'x')
print('bottles per Medicare bene 2025',round(174236/160278,3),' 2024',round(61184/57626,3))
# patients
bpp=1.087
for y in ['2025','2026E']: print(y,'patients ~',round(btl[y]/bpp),'k')
# Part D enrollment ~ 54.4M (2024 states sum)
print('Medicare benes 2025 / PartD enrollees(~55M):',round(160278/55e6*100,2),'%')
# 2031 requirement for $2.2B and $2.0B
for peak in [2000,2200]:
    for g in [0.03,0.05]:
        npb=1.170*(1+g)**5
        b=peak/npb; pts=b/bpp; new=pts*0.8
        print(f'peak {peak} net price growth {g:.0%}/yr: net/btl ${npb*1000:,.0f}, bottles {b:,.0f}k, patients {pts:,.0f}k, new pts {new:,.0f}k/yr')
# cumulative new patients 2023-2031 if new starts grow geometrically from 2026 (~0.8*patients) to 2031 target
new26=btl['2026E']/bpp*0.8
cum_hist=(15+163+400)/bpp*0.85 + new26
for tgt in [1076,1200]:
    r=(tgt/new26)**(1/5); cum=cum_hist+sum(new26*r**k for k in range(1,6))
    print(f'new starts 2026 {new26:,.0f}k -> 2031 {tgt}k: CAGR {r-1:.1%}, cumulative unique pts thru 2031 ~{cum/1000:,.1f}M = {cum/25000:.0%} of 25M, {cum/9000:.0%} of 9M')
