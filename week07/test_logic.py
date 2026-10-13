# test_logic.py
from logic import convert

def run_tests():
    test_cases = [
        # (value, from_unit, to_unit, expected_result, expected_notice)
        ("100", "cm", "m", "1.00", ""),
        ("1", "km", "m", "1000.00", ""),
        ("10", "mm", "cm", "1.00", ""),
        ("0", "°C", "°F", "32.00", ""),
        ("100", "°C", "°F", "212.00", ""),
        ("32", "°F", "°C", "0.00", ""),
        ("10", "cm", "°C", "", "단위가 일치하지 않습니다"),
        ("abc", "cm", "m", "", "숫자가 아닙니다"),
        ("", "cm", "m", "", "숫자가 아닙니다"),
    ]

    passed = 0
    failed = 0

    print("--- 테스트 시작 ---")
    for i, (val, f_unit, t_unit, exp_res, exp_not) in enumerate(test_cases):
        res, noti = convert(val, f_unit, t_unit)
        if res == exp_res and noti == exp_not:
            print(f"Test {i+1}: PASS")
            passed += 1
        else:
            print(f"Test {i+1}: FAIL (Expected: ({exp_res}, '{exp_not}'), Got: ('{res}', '{noti}'))")
            failed += 1
    
    print("------------------")
    print(f"통과: {passed}, 실패: {failed}")
    print("--- 테스트 종료 ---")

if __name__ == "__main__":
    run_tests()
