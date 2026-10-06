import re

def format_phone_number(phone_str):
    # 숫자만 남기기 (하이픈이나 공백 제거)
    digits = re.sub(r'\D', '', phone_str)
    
    # 1. 010으로 시작하는 경우
    if digits.startswith('010'):
        if len(digits) == 11:
            # 3-4-4 형식
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 010 번호 형식입니다."

    # 2. 011, 016, 017, 018, 019로 시작하는 경우
    elif digits.startswith(('011', '016', '017', '018', '019')):
        if len(digits) == 10:
            # 3-3-4 형식
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11:
            # 3-4-4 형식
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 번호 자릿수입니다."
            
    else:
        return "지원하지 않는 식별 번호입니다."

# --- 테스트 케이스 ---
test_cases = [
    "01012345678",    # 010 (11자리) -> 010-1234-5678
    "0101234567",     # 010 (10자리) -> 에러
    "0111234567",     # 011 (10자리) -> 011-123-4567
    "01112345678",    # 011 (11자리) -> 011-1234-5678
    "0161234567",     # 016 (10자리) -> 016-123-4567
    "01712345678",    # 017 (11자리) -> 017-1234-5678
    "019123456789",   # 잘못된 자릿수
    "021234567"       # 지원하지 않는 번호
]

print(f"{'입력값':<15} | {'결과'}")
print("-" * 30)
for tc in test_cases:
    print(f"{tc:<15} | {format_phone_number(tc)}")
