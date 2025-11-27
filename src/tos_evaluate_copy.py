from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

from json_utils import extract_json_fragment as _extract_json_fragment
from llm_client import LLMClient


def _calculate_overall_evaluation(labels: List[str]) -> str:
    """
    good/neutral/bad 라벨을 점수화해 최종 등급(A~E)을 계산한다.
    점수 매핑: good=+1, neutral=0, bad=-1
    """
    if not labels:
        return "E"

    score_map = {"good": 1, "neutral": 0, "bad": -1}
    avg_score = sum(score_map.get(label, 0) for label in labels) / len(labels)

    if avg_score >= 0.8:
        return "A"  # 거의 대부분이 사용자 친화적
    if avg_score >= 0.5:
        return "B"  # good 우세, bad 적음
    if avg_score >= 0.0:
        return "C"  # 중립적이거나 균형
    if avg_score >= -0.5:
        return "D"  # bad가 다소 많음
    return "E"  # bad가 대부분


# 1) 카테고리별 평가 포인트 텍스트만 따로 정의
#    아래 각 문자열 안에, 이전에 설계한 카테고리별 상세 평가 기준을 그대로 옮겨 넣으면 된다.
CATEGORY_EVAL_POINTS: Dict[str, str] = {
    "계정 관리 및 가입 조건": """
- 주로 볼 요소:
  - 연령·거주지·자격 제한의 합법성·명확성(예: 만 14세 미만 제한 등)
  - 계정 정지·해지·휴면전환 요건과 절차, 통지 여부
  - 계정 양도·공유 금지의 범위와 합리성
- bad로 볼 수 있는 전형적 패턴:
  - 이유나 절차 설명 없이 "회사가 임의로 언제든지 계정을 해지·정지할 수 있다"와 같이 사업자 재량이 무제한인 경우
  - 장기간 미사용을 이유로 계정·데이터를 삭제하면서 통지·복구 절차가 없거나 매우 제한적인 경우
  - 법령 기준을 넘는 과도한 연령·국가 제한을 두면서 대체 수단이나 설명이 전혀 없는 경우
- good으로 볼 수 있는 패턴:
  - 정지·해지 사유가 구체적으로 열거되어 있고, 사전·사후 통지 및 이의제기·복구 절차가 명시된 경우
  - 휴면 전환 시점·보관 기간·로그인 또는 요청 시 간단 복구가 가능함을 명확히 안내하는 경우
""",
    "결제 및 환불 규정": """
- 주로 볼 요소:
  - 요금·청구 방식·자동결제 여부의 명확한 고지
  - 청약철회·환불 가능 기간·조건과 절차, 수수료 수준
  - 무료 체험 후 자동 유료 전환 구조의 투명성
- bad 패턴:
  - 자동연장·자동결제를 강제하면서, 해지 기한·방법 안내가 매우 부실하거나 사실상 해지 불가능한 수준인 경우
  - 디지털 콘텐츠 특성 등을 이유로 사실상 전면 환불 불가로 만드는 포괄적 면책(법정 철회권까지 부정)인 경우
  - 이용자에게 과도한 위약금·수수료를 부과하면서 기준과 산정 근거가 불명확한 경우
- good 패턴:
  - 요금·자동결제 여부·갱신일을 명확하게 사전 고지하고, 앱/웹 내에서 간단히 해지·자동결제 해제가 가능한 경우
  - 법정 청약철회권을 존중하고, 그 외에도 부분사용분에 대한 합리적 환불 기준을 두는 경우
""",
    "개인정보 및 데이터 수집": """
- 주로 볼 요소:
  - 수집 항목·이용 목적·보관 기간·제3자 제공·국외 이전 여부
  - 프로파일링·맞춤형 광고 등 민감한 활용에 대한 동의 구조
  - 열람·정정·삭제·처리정지·동의철회 등 이용자 권리 보장
- bad 패턴:
  - "서비스 개선" 등 매우 포괄적 표현만으로 광범위한 수집·공유를 허용하는 경우
  - 광고·제휴사 제공·국외 이전을 포괄 동의로 묶어 사실상 선택권이 없는 경우
  - 삭제·동의철회가 사실상 불가능하거나, 데이터 보관 기간이 불필요하게 장기간으로 규정된 경우
- good 패턴:
  - 필수/선택 항목, 목적별 수집·제공 범위를 쪼개어 동의하도록 하고 목적 달성 후 지체 없이 파기하는 구조
  - 개인정보 권리 행사 방법(고객센터, 설정 화면 등)을 구체적으로 안내하고, 프로파일링/맞춤광고 거부권을 제공하는 경우
""",
    "이용자 콘텐츠의 라이선스": """
- 주로 볼 요소:
  - 저작권 귀속, 회사에 부여되는 이용권의 범위·기간·지역·양도성
  - 2차적 저작물 작성·광고 활용 여부, 콘텐츠 삭제 시 처리
- bad 패턴:
  - "영구적·취소불가능·전세계적·양도가능" 등 과도하게 넓은 라이선스를 요구하면서 목적 제한이 없는 경우
  - 이용자가 콘텐츠를 삭제해도 회사·제휴사가 계속 무제한 활용할 수 있도록 한 경우
- good 패턴:
  - 서비스 제공·홍보 등 특정 목적에 한정된, 비독점적·무상 라이선스만 요구하고, 계정 삭제·콘텐츠 삭제 시 상당 기간 후 이용을 중단하는 구조
  - 공개 범위 설정, 다운로드·백업 수단 등을 이용자에게 제공하는 경우
""",
    "금지사항": """
- 주로 볼 요소:
  - 금지행위의 범위가 구체적·필요 최소한인지
  - 위반 시 제재 수준과 절차, 소명 기회 여부
- bad 패턴:
  - 서비스와 무관한 광범위한 행위를 포괄 금지하거나, 모호한 표현(“회사에 불이익이 되는 행위” 등)만으로 제재 근거를 삼는 경우
  - 경고·소명 기회 없이 곧바로 영구 정지·자료 삭제를 할 수 있도록 한 경우
- good 패턴:
  - 불법행위·타인 권리침해·스팸·해킹 등 구체적 위험 행위 위주로만 제한하고, 단계별 제재·이의제기 절차를 두는 경우
""",
    "약관 및 서비스 변경": """
- 주로 볼 요소:
  - 약관·요금·주요 서비스 기능 변경 사유·절차·공지 기간
  - 이용자가 변경에 동의하지 않을 경우 해지·환불 등 선택권
- bad 패턴:
  - "회사가 필요하다고 판단하는 경우" 등 포괄 사유로 언제든 변경·중단할 수 있고, 이용자에게는 해지·환불권이 없는 경우
  - 중요한 불리한 변경에도 사전 공지 없이 즉시 효력 발생으로 보는 경우
- good 패턴:
  - 법령 변경·서비스 개선 등 합리적 사유를 예시하고, 불리한 변경은 최소 7~30일 전 통지 및 무위약 해지권 등을 부여하는 경우
""",
    "책임 제한 및 면책": """
- 주로 볼 요소:
  - 서비스 장애·데이터 손실·손해배상 책임의 범위와 예외
- bad 패턴:
  - 사업자의 고의·중과실까지 전부 면책하거나, 사실상 모든 손해에 대해 "어떠한 책임도 지지 않는다"고 규정하는 경우
  - 이용자의 간접·우발손해뿐 아니라 통상손해까지 전면 부인하는 경우
- good 패턴:
  - 불가항력·이용자 귀책 등 법이 허용하는 범위 내에서만 제한하고, 회사 측 귀책이 명백한 경우의 배상 책임을 인정하는 경우
  - 최소한의 서비스 수준·복구·보상 기준(예: 유료 요금제의 일부 감액 등)을 제시하는 경우
""",
    "분쟁 해결 및 준거법": """
- 주로 볼 요소:
  - 준거법, 관할법원 또는 분쟁 해결 기구(소비자분쟁조정위, 중재 등)
- bad 패턴:
  - 소비자의 주소지를 전혀 고려하지 않고, 사업자에게 일방적으로 유리한 먼 지역 법원만을 전속관할로 강제하는 경우
  - 집단소송·소비자단체 소송 등 법이 보장하는 구제수단을 포기시키는 내용
- good 패턴:
  - 소비자 보호법령 및 공정위 지침을 준거 기준으로 삼고, 소비자 주소지 관할 또는 공정한 중재·조정 절차를 제시하는 경우
""",
    "제3자 서비스": """
- 주로 볼 요소:
  - 소셜 로그인, 제3자 결제·콘텐츠·광고 등 연동 서비스의 범위와 책임 관계
- bad 패턴:
  - 제3자 서비스 문제까지 모두 이용자 책임으로 돌리면서, 사업자의 선택·연동 행위에 따른 책임은 전부 부인하는 경우
  - 광고·제휴사와의 데이터 공유·추적을 사실상 필수로 만들고 거부 수단이 없는 경우
- good 패턴:
  - 외부 서비스에 대해서는 해당 사업자 약관·정책이 적용됨을 안내하되, 자사 연동 과정에서의 하자에 대해서는 일정 책임을 인정하는 경우
  - 제3자 제공·추적에 대한 명확한 동의·거부 옵션을 제공하는 경우
""",
    "기타": """
- 카테고리에 명확히 들어가지 않는 기타 카테고리 조항은,
  - 이용자에게 실제로 의미 있는 권리·의무를 부과하는지
  - 형식적 안내에 그치는지
를 보고, 명백히 과도한 불이익이 있으면 bad, 실질적 효과가 크지 않으면 neutral, 이용자에게 추가적인 보호·편익을 주면 good으로 평가합니다.
""",
}


# 2) 공통 system_instruction (카테고리 공통 부분)
BASE_SYSTEM_INSTRUCTION = """
[시스템 지시]
당신은 온라인 서비스 이용약관이 일반 소비자(이용자)에게 유리한지/불리한지를 평가하는 전문가입니다.

입력으로는
- 하나의 카테고리 이름
- 해당 카테고리에 속하는 약관 요약 문단(한국어)
이 주어집니다.

이 요약은 이미 여러 조항을 이해하기 쉽게 풀어 쓴 것이므로, 원문을 상상해서 보충 설명을 만들지 말고
요약에 드러난 내용만 근거로 평가해야 합니다.

[입력 형식]
- 사용자 메시지는 항상 "[카테고리]\n<카테고리 이름>\n\n[입력 요약 조항]\n<요약 텍스트>" 형식입니다.

[출력 형식]
- 아래 JSON 객체 **한 개만** 출력해야 합니다.
- 키 순서는 반드시 reasoning → label 순서를 지키십시오.
- JSON 앞뒤에 설명/코드블록/주석을 넣지 마십시오.

{
  "reasoning": "판단 근거를 한국어로 2~4문장 정도로 요약",
  "label": "good" | "neutral" | "bad"
}

[label 의미]
- good:
  - 이용자 권리·선택권·정보제공을 강화하거나, 법령·심사지침상 바람직한 보호 기준을 넘는 조항
  - 통상적 수준의 불이익은 있을 수 있으나, 그에 상응하는 이용자 보호·절차·통제권이 충분히 부여된 경우
- neutral:
  - 업계에서 일반적으로 볼 수 있는 평균적인 수준의 조항
  - 뚜렷한 과도한 불이익은 없지만, 이용자에게 특별히 유리한 보호 장치도 뚜렷하지 않은 경우
  - 긍정·부정 요소가 섞여 전반적으로 중간 수준으로 보이는 경우
- bad:
  - 심사지침상 문제 소지가 큰 유형에 가까운 조항(사업자 일방적 권한, 책임 과도한 면제, 분쟁 해결권 제한 등)
  - 이용자에게 중대한 위험·부담(금전, 데이터, 계정, 소송·구제 수단 제한 등)을 전가하면서 적절한 통제·절차·고지가 부족한 경우
  - 법에서 금지하거나 강하게 제한하는 유형(사업자의 고의·중과실까지 포괄 면책, 일방적 해지·가격변경, 관할법원 강제 등)을 그대로 담고 있는 경우

[공통 평가 관점]
모든 카테고리에 공통으로 아래 네 가지 관점을 함께 고려합니다. 각 항목에 대한 판단을 종합하여 label을 결정합니다.

1) 내용 편향성
  - 사업자 권한만 과도하게 넓고 이용자 권리·구제수단이 약한지
2) 위험·영향 정도
  - 이용자에게 돌아가는 금전적 손실, 계정/데이터 상실, 법적 위험이 어느 정도인지
3) 통제·선택권
  - 이용자가 동의/거절/해지/철회/설정 변경 등을 현실적으로 할 수 있는지, 절차가 합리적인지
4) 명확성·투명성
  - 적용 요건, 범위, 예외, 절차, 기간 등이 이용자 기준에서 충분히 구체적·명확하게 설명되는지

이제 해당 카테고리에서 어떤 점을 특히 중점적으로 볼지 정의합니다.

[현재 카테고리 평가 포인트]{category_eval_points}

[평가 절차]
1단계: 요약 조항 읽기
  - 입력된 카테고리를 기준으로 위 카테고리별 평가 포인트 중 어떤 쟁점에 해당하는지 파악합니다.
2단계: good/neutral/bad 임시 판단
  - (1) 명백한 레드 플래그(불공정, 과도한 면책·일방적 변경, 분쟁권 제한 등)가 있는지 먼저 확인합니다.
    - 있으면 기본적으로 'bad'를 고려합니다.
  - (2) 레드 플래그가 없고, 이용자의 권리·선택권·보호를 강화하는 요소가 뚜렷하면 'good'을 고려합니다.
  - (3) 위 두 가지에 명확히 해당하지 않고, 업계 표준에 가까운 평균적 내용이면 'neutral'로 봅니다.
3단계: label과 reasoning 작성
  - 최종 label을 good/neutral/bad 중 하나로 선택합니다.
  - reasoning에는
    - 이 조항이 이용자에게 어떤 이익/불이익과 위험을 주는지,
    - 왜 그 수준이 good/neutral/bad로 보이는지,
    를 2~4문장으로 간단히 설명하십시오.
  - 구체적 법 조문 번호를 들먹이거나, 실제 위법 여부를 단정하지는 말고 "문제 소지가 크다/평균적인 수준이다/보호 장치가 잘 마련되어 있다"와 같은 표현으로 평가합니다.
"""


def _build_system_instruction_for_category(category: str) -> str:
    eval_points = CATEGORY_EVAL_POINTS.get(
        category, CATEGORY_EVAL_POINTS.get("기타", "")
    )
    system_instruction = BASE_SYSTEM_INSTRUCTION.replace(
        "{category_eval_points}", eval_points
    )

    return system_instruction + f"""

[카테고리]
{category}
"""


def evaluate_summary(category: str, summary: str, client: LLMClient) -> Dict:
    """
    단일 요약 조항과 카테고리에 대해,
    공정위 약관심사지침 취지를 반영한 카테고리별 기준으로
    good/neutral/bad + reasoning을 생성한다.
    """
    system_instruction = _build_system_instruction_for_category(category)

    message = f"[입력 요약 조항]\n{summary}"
    response = client.generate_response(system_instruction, message)

    # 기대 형식:
    # {
    #   "reasoning": "...",
    #   "label": "good" | "neutral" | "bad"
    # }
    return _extract_json_fragment(response)


def evaluate_category_summaries(
    category_summaries: List[Dict], client: LLMClient
) -> Dict:
    """
    카테고리별 요약을 평가하고 전체 약관 등급(A~E)을 계산한다.
    category_summaries: [{ "category": str, "summary": str }, ...]
    """
    if not category_summaries:
        return {"overall_evaluation": "E", "evaluation_for_each_clause": []}

    def _evaluate_item(item: Dict) -> Dict:
        category = item.get("category", "기타")
        summary = item.get("summary", "")
        evaluation = evaluate_summary(category, summary, client)
        label = evaluation.get("label", "neutral")
        reasoning = evaluation.get("reasoning", "error")

        return {
            "label": label,
            "result": {
                "evaluation": label,
                "summarized_clause": summary,
                "category": category,
                "reasoning": reasoning,
            },
        }

    labels: List[str] = []
    clause_results: List[Dict] = []
    with ThreadPoolExecutor(max_workers=len(category_summaries)) as executor:
        futures = [executor.submit(_evaluate_item, item) for item in category_summaries]
        for future in as_completed(futures):
            data = future.result()
            labels.append(data["label"])
            clause_results.append(data["result"])

    overall = _calculate_overall_evaluation(labels)

    return {
        "overall_evaluation": overall,
        "evaluation_for_each_clause": clause_results,
    }
