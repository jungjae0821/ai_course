import re

def format_phone_number(phone_raw):
    # 1. 숫자만 추출
    digits = re.sub(r'\D', '', phone_raw)
    
    if len(digits) < 10:
        return "Invalid"

    prefix = digits[:3]
    length = len(digits)

    # 2. 010 규칙 적용
    if prefix == '010':
        if length == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "Invalid (010 must be 11 digits)"

    # 3. 기타 통신사 규칙 적용
    elif prefix in ['011', '016', '017', '018', '019']:
        if length == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif length == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "Invalid (Length mismatch)"

    else:
        return "Invalid Prefix"

# --- 테스트 ---
test_cases = [
    "01012345678",    # 010 11자리 -> 010-1234-5678
    "0101234567",     # 010 10자리 -> Invalid
    "0111234567",     # 011 10자리 -> 011-123-4567
    "01112345678",    # 011 11자리 -> 011-1234-5678
    "0161234567",     # 016 10자리 -> 016-123-4567
    "0212345678"      # 기타 -> Invalid
]

for case in test_cases:
    print(f"{case} => {format_phone_number(case)}")