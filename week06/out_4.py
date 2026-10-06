import re

def format_phone_number(phone_str):
    # 1. 숫자 이외의 문자 제거 (하이픈, 공백 등 제거)
    digits = re.sub(r'\D', '', phone_str)
    length = len(digits)
    
    # 2. 시작 번호 확인
    if digits.startswith('010'):
        # 010은 무조건 11자리여야 함
        if length == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 010 번호 형식입니다."

    elif digits.startswith(('011', '016', '017', '018', '019')):
        # 011 계열은 10자리 또는 11자리 허용
        if length == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif length == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 번호 자릿수입니다."
            
    else:
        return "휴대폰 번호가 아닙니다."

# --- 테스트 케이스 ---
test_cases = [
    "01012345678",    # 010 (11자리) -> 010-1234-5678
    "0101234567",     # 010 (10자리) -> 오류
    "0111234567",     # 011 (10자리) -> 011-123-4567
    "01112345678",    # 011 (11자리) -> 011-1234-5678
    "0161234567",     # 016 (10자리) -> 016-123-4567
    "01912345678",    # 019 (11자리) -> 019-1234-5678
    "0212345678"      # 기타 -> 오류
]

for tc in test_cases:
    print(f"{tc}  =>  {format_phone_number(tc)}")