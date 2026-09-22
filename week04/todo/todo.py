import json
import os
from datetime import datetime

TODO_FILE = 'todo.json'

def load_tasks():
    """todo.json 파일에서 할 일 목록을 불러옵니다."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    """할 일 목록을 todo.json 파일에 저장합니다."""
    try:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def get_sorted_tasks(tasks):
    """마감일 기준으로 정렬된 할 일 목록을 반환합니다. 마감일이 없는 것은 맨 뒤로 보냅니다."""
    return sorted(
        tasks, 
        key=lambda x: (x['deadline'] is None, x['deadline'] if x['deadline'] else "")
    )

def add_task(tasks):
    """새로운 할 일을 추가합니다 (마감일 포함)."""
    task_name = input("추가할 할 일을 입력하세요: ").strip()
    if not task_name:
        print("할 일은 빈 칸일 수 없습니다.")
        return

    deadline_str = input("마감일을 입력하세요 (예: 2023-12-31 또는 그냥 엔터): ").strip()
    
    deadline = None
    if deadline_str:
        try:
            # 날짜 형식 검증
            datetime.strptime(deadline_str, '%Y-%m-%d')
            deadline = deadline_str
        except ValueError:
            print("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해주세요. 마감일 없이 추가합니다.")
            deadline = None

    tasks.append({
        "task": task_name,
        "completed": False,
        "deadline": deadline
    })
    save_tasks(tasks)
    print(f"'{task_name}'이(가) 추가되었습니다.")

def view_tasks(tasks):
    """할 일 목록을 마감일 순으로 보여줍니다."""
    sorted_tasks = get_sorted_tasks(tasks)
    
    if not sorted_tasks:
        print("\n현재 할 일 목록이 비어 있습니다.")
        return []

    print("\n--- 할 일 목록 (마감일 순) ---")
    for i, task in enumerate(sorted_tasks, 1):
        status = "[V]" if task['completed'] else "[ ]"
        deadline_display = f" | 마감일: {task['deadline']}" if task['deadline'] else ""
        print(f"{i}. {status} {task['task']}{deadline_display}")
    print("----------------------------")
    return sorted_tasks

def complete_task(tasks):
    """할 일을 완료 표시합니다."""
    sorted_tasks = view_tasks(tasks)
    if not sorted_tasks:
        return

    try:
        choice = int(input("완료 처리할 번호를 입력하세요: "))
        if 1 <= choice <= len(sorted_tasks):
            target_task = sorted_tasks[choice - 1]
            # 원본 tasks 리스트에서 해당 task 객체를 찾아 수정
            for t in tasks:
                if t is target_task:
                    t['completed'] = True
                    break
            save_tasks(tasks)
            print(f"'{target_task['task']}'을(를) 완료로 표시했습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def delete_task(tasks):
    """할 일을 삭제합니다."""
    sorted_tasks = view_tasks(tasks)
    if not sorted_tasks:
        return

    try:
        choice = int(input("삭제할 번호를 입력하세요: "))
        if 1 <= choice <= len(sorted_tasks):
            target_task = sorted_tasks[choice - 1]
            # 원본 tasks 리스트에서 해당 task 객체를 찾아 삭제
            for i, t in enumerate(tasks):
                if t is target_task:
                    tasks.pop(i)
                    break
            save_tasks(tasks)
            print(f"'{target_task['task']}'이(가) 삭제되었습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def main():
    tasks = load_tasks()

    while True:
        print("\n=== TODO 관리 프로그램 ===")
        print("1. 목록 보기")
        print("2. 할 일 추가")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        
        choice = input("메뉴를 선택하세요 (1-5): ").strip()

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()

import json
import os
from datetime import datetime

TODO_FILE = 'todo.json'

def load_tasks():
    """todo.json 파일에서 할 일 목록을 불러옵니다."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    """할 일 목록을 todo.json 파일에 저장합니다."""
    try:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def get_sorted_tasks(tasks):
    """마감일 기준으로 정렬된 할 일 목록을 반환합니다. 마감일이 없는 것은 맨 뒤로 보냅니다."""
    return sorted(
        tasks, 
        key=lambda x: (x['deadline'] is None, x['deadline'] if x['deadline'] else "")
    )

def add_task(tasks):
    """새로운 할 일을 추가합니다 (마감일 포함)."""
    task_name = input("추가할 할 일을 입력하세요: ").strip()
    if not task_name:
        print("할 일은 빈 칸일 수 없습니다.")
        return

    deadline_str = input("마감일을 입력하세요 (예: 2023-12-31 또는 그냥 엔터): ").strip()
    
    deadline = None
    if deadline_str:
        try:
            # 날짜 형식 검증
            datetime.strptime(deadline_str, '%Y-%m-%d')
            deadline = deadline_str
        except ValueError:
            print("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해주세요. 마감일 없이 추가합니다.")
            deadline = None

    tasks.append({
        "task": task_name,
        "completed": False,
        "deadline": deadline
    })
    save_tasks(tasks)
    print(f"'{task_name}'이(가) 추가되었습니다.")

def view_tasks(tasks):
    """할 일 목록을 마감일 순으로 보여줍니다."""
    sorted_tasks = get_sorted_tasks(tasks)
    
    if not sorted_tasks:
        print("\n현재 할 일 목록이 비어 있습니다.")
        return []

    print("\n--- 할 일 목록 (마감일 순) ---")
    for i, task in enumerate(sorted_tasks, 1):
        status = "[V]" if task['completed'] else "[ ]"
        deadline_display = f" | 마감일: {task['deadline']}" if task['deadline'] else ""
        print(f"{i}. {status} {task['task']}{deadline_display}")
    print("----------------------------")
    return sorted_tasks

def complete_task(tasks):
    """할 일을 완료 표시합니다."""
    sorted_tasks = view_tasks(tasks)
    if not sorted_tasks:
        return

    try:
        choice = int(input("완료 처리할 번호를 입력하세요: "))
        if 1 <= choice <= len(sorted_tasks):
            target_task = sorted_tasks[choice - 1]
            # 원본 tasks 리스트에서 해당 task 객체를 찾아 수정
            for t in tasks:
                if t is target_task:
                    t['completed'] = True
                    break
            save_tasks(tasks)
            print(f"'{target_task['task']}'을(를) 완료로 표시했습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def delete_task(tasks):
    """할 일을 삭제합니다."""
    sorted_tasks = view_tasks(tasks)
    if not sorted_tasks:
        return

    try:
        choice = int(input("삭제할 번호를 입력하세요: "))
        if 1 <= choice <= len(sorted_tasks):
            target_task = sorted_tasks[choice - 1]
            # 원본 tasks 리스트에서 해당 task 객체를 찾아 삭제
            for i, t in enumerate(tasks):
                if t is target_task:
                    tasks.pop(i)
                    break
            save_tasks(tasks)
            print(f"'{target_task['task']}'이(가) 삭제되었습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def main():
    tasks = load_tasks()

    while True:
        print("\n=== TODO 관리 프로그램 ===")
        print("1. 목록 보기")
        print("2. 할 일 추가")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        
        choice = input("메뉴를 선택하세요 (1-5): ").strip()

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()
