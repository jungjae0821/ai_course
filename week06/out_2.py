import re

def format_phone_number(phone_str):
    # 1. 숫자 이외의 모든 문자 제거 (하이픈, 공백 등 제거)
    digits = re.sub(r'\D', '', phone_str)
    length = len(digits)
    
    # 2. 시작 번호 확인
    if digits.startswith('010'):
        # 010은 11자리일 때만 처리
        if length == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 010 번호 형식입니다."

    elif digits.startswith(('011', '016', '017', '018', '019')):
        # 10자리인 경우 (3-3-4)
        if length == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        # 11자리인 경우 (3-4-4)
        elif length == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 번호 길이입니다."
            
    else:
        return "지원하지 않는 시작 번호입니다."

# --- 테스트 코드 ---
test_cases = [
    "01012345678",  # 010 (11자리) -> 010-1234-5678
    "0111234567",   # 011 (10자리) -> 011-123-4567
    "01712345678",  # 017 (11자리) -> 017-1234-5678
    "0191234567",   # 019 (10자리) -> 019-123-4567
    "0101234567",   # 010 (10자리) -> 에러
    "0212345678"    # 기타 -> 에러
]

for case in test_cases:
    print(f"{case}  =>  {format_phone_number(case)}")
