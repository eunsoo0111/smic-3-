# copper_mine V0 차이표 — 무하네스 초안 vs 레포(03·04번 문서)

- 무하네스 초안: 레포 문서를 보기 전, "광산을 처음부터 짓는다면"으로 5단계(탐사·개발·채굴·선광·판매), 입력 30개를 먼저 적었다.
- 레포: 이 레포에는 체인 yaml(core/valuechain)이 없다. 대조 대상은 03·04번 문서의 종목 표 17종목이다.

## 무하네스에만 있던 칸 (03·04에 종목이 없던 자리)

| 칸 | 왜 중요한가 | 메이커(상장 접근로) |
|---|---|---|
| 분쇄 매체(강철 볼) | 선광비의 21.5%. 처리하는 돌의 양에 비례해 닳는다. 품위 하락의 가장 직접적 수혜 | Moly-Cop(사모), ME Elecmetal(칠레 비상장), Magotteaux(Sigdo Koppers 소유, 산티아고 상장) |
| 밀 라이너 | 교체 주기마다 밀이 멈춘다 | Metso, Weir, FLSmidth, ME Elecmetal |
| 부선 시약 | 처리 물량 비례 | Syensqo, Clariant, Orica, Nouryon(사모) |
| 초대형 타이어 | 석유계 원가 항목 | Bridgestone, Michelin |
| 자율 운전 소프트웨어 | 장비에 묶여 팔림 | Caterpillar, Komatsu, Epiroc |
| 자원 모델링 소프트웨어 | 구독형 반복 매출 | Micromine(Weir), Seequent(Bentley), Datamine(Constellation) |
| EPCM 엔지니어링 | 신규 광산 건설의 첫 돈 | Worley, Fluor, Hatch·Bechtel(비상장) |
| 제련소(고객) | TC/RC 역전의 피해자 | 중국 제련사, JX, Aurubis, LS MnM(LS 자회사), 고려아연 |
| 쇼벨 | 03·04에는 트럭(Komatsu)만 | Hitachi CM, Liebherr(비상장) |

## 레포에만 있던 것

- Perenti: 03에서는 "광산 운영"으로 넣었다. 이 BOM은 노천 광산 기준이라 지하 채굴 용역을 `없음` 행으로 두고, Perenti는 시추 메이커로만 남겼다.
- Bureau Veritas: 03에 있었다. 광물 비중이 작아 시료 분석 메이커의 일부로 둔다.

## 시사점

- 03·04는 장비와 서비스만 봤고, 소모품 칸(분쇄 매체·라이너·시약·타이어)이 통째로 비어 있었다.
- "광석이 가난해질수록 같은 구리에 더 많은 돌을 간다"는 논리의 직접 수혜는 소모품이다.
- 분쇄 매체 1위권은 사모·비상장이라 상장 접근로가 약하다. Sigdo Koppers가 화약(Enaex)과 분쇄 매체(Magotteaux)를 함께 가진 구조인지 확인할 가치가 있다(③, 미확인).
