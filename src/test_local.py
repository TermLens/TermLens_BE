import os

from lambda_function import lambda_handler

def create_test_event(url: str, body: str) -> dict:
    """테스트용 event 객체 생성"""
    return {
        'queryStringParameters': {
            'url': url
        },
        'body': body,
    }


def run_test():
    """Lambda 함수 로컬 테스트 실행"""

    # GEMINI_API_KEY 확인
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        print()
        return

    # 테스트 데이터
    test_url = "https://example.com/terms"
    test_body = """
    <html>
        <body>
            <h1>서비스 약관</h1>
            <p>이용자는 본 약관에 동의함으로써 당 서비스를 이용할 수 있습니다.</p>
            <p>당 회사는 이용자의 개인정보를 보호하기 위해 최선을 다합니다.</p>
            <p>서비스 이용 중 발생하는 문제에 대해 당 회사는 책임을 지지 않습니다.</p>
        </body>
    </html>
    """

    # Event와 Context 생성
    event = create_test_event(test_url, test_body)
    context = None

    print("=" * 60)
    print("lambda_function 로컬 테스트 실행")
    print("=" * 60)

    print("요청 데이터:")
    print("-" * 60)
    print(f"URL: {event['queryStringParameters']['url']}")
    print(f"Body 크기: {len(test_body)} bytes")
    print()

    try:
        print("lambda_handler 실행 중...")
        print()
        response = lambda_handler(event, context)

        print("응답 데이터:")
        print("-" * 60)
        print(f"Status Code: {response.get('statusCode')}")
        print()

        print("Body:")
        print(response.get('body'))

        print()
        print("=" * 60)

    except Exception as e:
        print()
        print(f"에러: {type(e).__name__}")
        print(f"   {str(e)}")
        print()
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_test()
