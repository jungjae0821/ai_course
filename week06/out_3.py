import re

def format_phone_number(phone_str):
    # 1. 숫자만 남기고 모두 제거
    digits = re.sub(r'\D', '', phone_str)
    length = len(digits)
    
    # 2. 시작 번호 확인
    if digits.startswith('010'):
        # 010은 반드시 11자리여야 함
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
        return "지원하지 않는 식별 번호입니다."

# --- 테스트 ---
print(format_phone_number("01012345678"))   # 010-1234-5678
print(format_phone_number("0111234567"))    # 011-123-4567
print(format_phone_number("01712345678"))   # 017-1234-5678
print(format_phone_number("0101234567"))    # 잘못된 010 번호 형식입니다.
