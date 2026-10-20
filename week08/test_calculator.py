import unittest
from calculator import calculate_parking_info, parse_time

class TestParkingCalculator(unittest.TestCase):
    def test_parse_time_valid(self):
        self.assertEqual(parse_time("10:00").hour, 10)
        self.assertEqual(parse_time("10:00").minute, 0)

    def test_parse_time_invalid(self):
        with self.assertRaises(ValueError):
            parse_time("25:00")
        with self.assertRaises(ValueError):
            parse_time("abc")

    def test_calculate_parking_info_free(self):
        # 25분 주차 (30분 미만)
        duration, fee = calculate_parking_info("10:00", "10:25")
        self.assertEqual(duration, 25)
        self.assertEqual(fee, 0)

    def test_calculate_parking_info_boundary_free(self):
        # 30분 주차 (30분 미만이 아님)
        duration, fee = calculate_parking_info("10:00", "10:30")
        self.assertEqual(duration, 30)
        self.assertEqual(fee, 0)

    def test_calculate_parking_info_paid(self):
        # 31분 주차 (30분 초과, 1분 추가 -> 10분 1회 적용)
        duration, fee = calculate_parking_info("10:00", "10:31")
        self.assertEqual(duration, 31)
        self.assertEqual(fee, 500)

        # 40분 주차 (30분 초과, 10분 추가 -> 10분 1회 적용)
        duration, fee = calculate_parking_info("10:00", "10:40")
        self.assertEqual(duration, 40)
        self.assertEqual(fee, 500)

        # 41분 주차 (30분 초과, 11분 추가 -> 10분 2회 적용)
        duration, fee = calculate_parking_info("10:00", "10:41")
        self.assertEqual(duration, 41)
        self.assertEqual(fee, 1000)

    def test_calculate_parking_info_max_fee(self):
        # 매우 긴 주차 시간
        duration, fee = calculate_parking_info("10:00", "20:00")
        self.assertEqual(fee, 20000)

    def test_calculate_parking_invalid_range(self):
        # 출차 시간이 입차 시간보다 빠른 경우
        with self.assertRaises(ValueError):
            calculate_parking_info("11:00", "10:00")

if __name__ == "__main__":
    unittest.main()
