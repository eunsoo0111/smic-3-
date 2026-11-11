import sys; sys.path.insert(0, "_contracts")
from v0_helpers import *
A = "범주라 단가·수량 축이 성립하지 않음"
N = [
 P("stack", "엔터프라이즈 소프트웨어 스택", "기업 1곳이 업무를 소프트웨어(와 AI 에이전트)로 처리하는 데 사는 것 전체. 층마다 과금 단위(좌석/사용량/거래)가 다르다"),
 S("stack.infra", "stack", "인프라·런타임", "앱과 에이전트가 도는 곳. 사용량 과금. AI Capex와 가장 가깝다"),
 I("stack.infra.iaas", "stack.infra", "service_ip", "클라우드 IaaS", "컴퓨트·스토리지. 사용량 과금. GPU 임대 포함 → AI Capex 직결(주제에서 제외 대상)"),
 I("stack.infra.edge", "stack.infra", "service_ip", "엣지·CDN·네트워크", "트래픽 전달·봇 관리·엣지 컴퓨트. 요청량 과금. 에이전트 트래픽이 늘면 Q 증가"),
 I("stack.infra.data", "stack.infra", "service_ip", "데이터베이스·데이터 플랫폼", "운영 DB, 웨어하우스, 스트리밍. 사용량 과금"),
 I("stack.infra.obs", "stack.infra", "service_ip", "관측(옵저버빌리티)", "로그·메트릭·트레이스. 수집량 과금"),
 S("stack.dev", "stack", "개발·배포", "코드를 만들고 배포하는 도구. AI가 코드 생산량을 늘리면 좌석은 줄고 산출물은 는다"),
 I("stack.dev.scm", "stack.dev", "service_ip", "소스·CI/CD·아티팩트 관리", "저장소, 빌드, 바이너리 저장. 좌석+사용량 혼합"),
 I("stack.dev.design", "stack.dev", "service_ip", "디자인·제품 협업", "UI 디자인, 프로토타입. 좌석+AI 크레딧"),
 I("stack.dev.codegen", "stack.dev", "service_ip", "AI 코딩 도구", "코드 생성 에이전트. 토큰·좌석 과금. 모델 회사와 직접 경쟁"),
 S("stack.sec", "stack", "보안", "공격 표면이 늘수록 지출이 는다. AI가 취약점을 더 빨리 찾으면 수요 증가"),
 I("stack.sec.endpoint", "stack.sec", "service_ip", "엔드포인트·XDR", "단말·워크로드 보호. 단말 수 과금"),
 I("stack.sec.network", "stack.sec", "service_ip", "네트워크 보안·SASE", "방화벽, 제로트러스트 접속. 사용자·대역폭 과금"),
 I("stack.sec.identity", "stack.sec", "service_ip", "신원·접근 관리", "사람과 기계(에이전트) 신원. 신원 수 과금 → 에이전트가 늘면 Q 증가"),
 I("stack.sec.vuln", "stack.sec", "service_ip", "취약점·앱 보안", "스캔, 코드 보안. 자산 수 과금"),
 S("stack.sor", "stack", "수평 기록 시스템", "전사 데이터의 원본. 교체 비용이 큼. 과금은 대부분 좌석"),
 I("stack.sor.erp", "stack.sor", "service_ip", "ERP·재무", "회계 원장, 구매, 재고. 좌석·모듈 과금"),
 I("stack.sor.crm", "stack.sor", "service_ip", "CRM·마케팅", "고객 기록, 영업·마케팅 자동화. 좌석 과금 → 에이전트 대체 우려의 중심"),
 I("stack.sor.hcm", "stack.sor", "service_ip", "HCM·급여", "인사·급여. 직원 수 과금 → 고용이 줄면 Q 감소"),
 I("stack.sor.itsm", "stack.sor", "service_ip", "ITSM·워크플로", "IT 요청·업무 흐름 자동화. 좌석+에이전트 과금"),
 S("stack.collab", "stack", "협업·생산성", "문서, 메신저, 프로젝트 관리. 순수 좌석 과금이라 AI 성공 시 가장 취약"),
 I("stack.collab.suite", "stack.collab", "service_ip", "오피스·협업 도구", "문서·메일·화상·프로젝트 관리. 좌석 과금"),
 S("stack.vert", "stack", "산업 특화 기록 시스템", "규제·현장 산업용. 대체재가 적고 결제가 붙는 경우가 많다"),
 I("stack.vert.health", "stack.vert", "service_ip", "헬스케어·생명과학", "임상·규제 문서, 영업, EHR. 좌석+모듈"),
 I("stack.vert.fin", "stack.vert", "service_ip", "금융·보험 코어", "은행 코어, 보험 계약·청구. 계약 규모(보험료·자산) 연동"),
 I("stack.vert.gov", "stack.vert", "service_ip", "공공·건설·현장", "지자체 행정, 건설 관리, 현장 서비스. 계약·공사 규모 연동"),
 I("stack.vert.smb", "stack.vert", "service_ip", "매장·소상공인 운영+결제", "POS, 예약, 급여 + 결제 수수료. 거래액 과금"),
 I("stack.vert.eng", "stack.vert", "service_ip", "설계·엔지니어링(CAD·PLM·EDA)", "제품 설계 도구. 좌석·토큰. EDA는 AI 칩 설계와 연동(주제에서 주의)"),
 S("stack.agent", "stack", "에이전트 계층", "새로 생긴 층. 일의 양으로 과금"),
 I("stack.agent.model", "stack.agent", "service_ip", "기반 모델 API", "토큰 과금. 비상장 모델 회사와 하이퍼스케일러 → AI Capex 직결(주제에서 제외 대상)"),
 I("stack.agent.platform", "stack.agent", "service_ip", "에이전트 플랫폼", "기록 시스템 위에서 일을 수행. 대화·작업 건당 과금"),
 I("stack.agent.seat", "stack.agent", "service_ip", "좌석 과금 에이전트", "에이전트를 좌석으로 파는 모델", absent="에이전트는 사람 수가 아니라 작업량으로 과금되는 방향(검증 필요)"),
 I("stack.onprem", "stack.sor", "service_ip", "신규 온프레미스 영구 라이선스", "설치형 일시불 판매", absent="신규 판매는 대부분 구독으로 전환(검증 필요)"),
]
for n in N:
    if n["kind"] == "input" and n["makers"] == V1:
        n["qty_per_unit"] = n["price"] = f"없음 — {A}"
dump("software_stack/work/v0_blind.json", "software_stack", "엔터프라이즈 소프트웨어 스택", "기업 소프트웨어 지출 100(범주별 비중)", N)
