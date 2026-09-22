def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! 0으로 나눌 수 없습니다."
    return x / y

def calculator():
    print("--- 파이썬 계산기 ---")
    print("연산 선택:")
    print("1. 더하기 (+)")
    print("2. 빼기 (-)")
    print("3. 곱하기 (*)")
    print("4. 나누기 (/)")
    print("5. 종료")

    while True:
        choice = input("\n원하는 연산 번호를 입력하세요 (1/2/3/4/5): ")

        if choice == '5':
            print("계산기를 종료합니다.")
            break

        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("첫 번째 숫자를 입력하세요: "))
                num2 = float(input("두 번째 숫자를 입력하세요: "))
            except ValueError:
                print("잘못된 입력입니다. 숫자를 입력해주세요.")
                continue

            if choice == '1':
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                print(f"{num1} / {num2} = {divide(num1, num2)}")
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    calculator()
