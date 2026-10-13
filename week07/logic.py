# logic.py

def convert(value_str: str, from_unit: str, to_unit: str) -> tuple[str, str]:
    """
    단위를 변환하는 함수.
    
    Args:
        value_str: 입력받은 숫자 문자열
        from_unit: 변환 전 단위 (mm, cm, m, km, °C, °F)
        to_unit: 변환 후 단위 (mm, cm, m, km, °C, °F)
        
    Returns:
        tuple[str, str]: (변환 결과값, 에러/안내 문구)
    """
    # 1. 숫자 검사
    try:
        val = float(value_str)
    except ValueError:
        return "", "숫자가 아닙니다"

    # 단위 카테고리 정의
    length_units = ['mm', 'cm', 'm', 'km']
    temp_units = ['°C', '°F']

    from_is_length = from_unit in length_units
    from_is_temp = from_unit in temp_units
    to_is_length = to_unit in length_units
    to_is_temp = to_unit in temp_units

    # 2. 단위 일치 여부 검사 (길이와 온도가 섞이는 경우 방지)
    if (from_is_length and to_is_temp) or (from_is_temp and to_is_length):
        return "", "단위가 일치하지 않습니다"
    
    # 정의되지 않은 단위가 들어온 경우
    if not (from_is_length or from_is_temp) or not (to_is_length or to_is_temp):
        return "", "알 수 없는 단위입니다"

    # 3. 변환 로직
    result = 0.0

    if from_is_length:
        # 길이를 m 기준으로 통일 (mm, cm, m, km -> m)
        to_m = {
            'mm': 0.001,
            'cm': 0.01,
            'm': 1.0,
            'km': 1000.0
        }
        val_in_m = val * to_m[from_unit]
        # m를 대상 단위로 변환 (m -> target)
        result = val_in_m / to_m[to_unit]
    
    elif from_is_temp:
        # 온도를 °C 기준으로 통일
        if from_unit == '°C':
            val_in_c = val
        else:  # °F -> °C
            val_in_c = (val - 32) * 5 / 9
        
        # °C를 대상 단위로 변환
        if to_unit == '°C':
            result = val_in_c
        else:  # °C -> °F
            result = (val_in_c * 9 / 5) + 32

    return f"{result:.2f}", ""

