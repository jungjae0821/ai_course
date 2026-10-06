import unittest
import os
import sqlite3
import app

class TodoAppTestCase(unittest.TestCase):
    def setUp(self):
        # Use a temporary database for testing
        self.test_db = 'test_todo.db'
        os.environ['DATABASE_URL'] = self.test_db
        app.DB_PATH = self.test_db
        
        # Initialize the app and database
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        # Remove the temporary database after tests
        if os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except PermissionError:
                pass

    def test_get_index(self):
        """GET /: HTTP 200 및 빈 목록(또는 초기 데이터) 페이지 응답"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Using decode to handle non-ASCII characters
        self.assertIn('할 일 관리', response.data.decode('utf-8'))

    def test_post_add_success(self):
        """POST /add (title="Test Task"): HTTP 302 리다이렉트 및 DB에 데이터 1건 생성 확인"""
        response = self.app.post('/add', data={'title': 'Test Task'}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        # Check if data is in DB
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM todos WHERE title = ?', ('Test Task',))
        row = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[0], 'Test Task')

    def test_post_add_empty(self):
        """POST /add (title=""): HTTP 302 혹은 에러 페이지 및 DB에 데이터 추가 실패 확인"""
        response = self.app.post('/add', data={'title': ''}, follow_redirects=False)
        self.assertIn(response.status_code, [200, 302])
        
        # Check if data is NOT in DB
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM todos WHERE title = ?', ('',))
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 0)

    def test_post_add_whitespace(self):
        """POST /add (title=" "): HTTP 302 혹은 에러 페이지 및 DB에 데이터 추가 실패 확인"""
        response = self.app.post('/add', data={'title': ' '}, follow_redirects=False)
        self.assertIn(response.status_code, [200, 302])
        
        # Check if data is NOT in DB
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM todos WHERE title = ?', (' ',))
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 0)

    def test_post_toggle_existing_todo(self):
        """POST /toggle/1 (존재하는 ID): HTTP 302 및 is_completed 값 반전 확인"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todos (title) VALUES (?)', ('Test Task',))
        conn.commit()
        conn.close()

        response = self.app.post('/toggle/1', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('SELECT is_completed FROM todos WHERE id = 1')
        self.assertEqual(cursor.fetchone()[0], 1)
        conn.close()
        page = self.app.get('/')
        self.assertIn('class="completed">Test Task</span>', page.data.decode('utf-8'))

        response = self.app.post('/toggle/1', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('SELECT is_completed FROM todos WHERE id = 1')
        self.assertEqual(cursor.fetchone()[0], 0)
        conn.close()
        page = self.app.get('/')
        self.assertIn('class="">Test Task</span>', page.data.decode('utf-8'))

    def test_post_toggle_missing_todo(self):
        """POST /toggle/999 (없는 ID): HTTP 404 반환"""
        response = self.app.post('/toggle/999', follow_redirects=False)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
