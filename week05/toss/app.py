import os
import json
import base64
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# 4. 키 설정
SECRET_KEY = os.environ.get("TOSS_SECRET_KEY", "test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6")

def get_auth_header(secret_key):
    encoded_key = base64.b64encode(f"{secret_key}:".encode("ascii")).decode("ascii")
    return {"Authorization": f"Basic {encoded_key}"}

@app.route("/")
def index():
    # 2. GET / : index.html
    return render_template("index.html")

@app.route("/success")
def success():
    # 20. GET /success : 쿼리의 paymentKey, orderId, amount를 받아 서버에서 결제 승인 API를 호출한다.
    payment_key = request.args.get("paymentKey")
    order_id = request.args.get("orderId")
    amount_str = request.args.get("amount")

    if not all([payment_key, order_id, amount_str]):
        return "Missing parameters", 400

    # 22. 승인 API를 부르기 전에 쿼리의 amount가 1000과 같은지 확인한다.
    try:
        amount = int(amount_str)
    except ValueError:
        return "Invalid amount format", 400

    if amount != 1000:
        return f"Amount mismatch. Expected 1000, got {amount}", 400

    # 토스페이먼츠 결제 승인 API 호출
    # URL: https://api.tosspayments.com/v1/payments/{paymentKey}/confirm
    url = f"https://api.tosspayments.com/v1/payments/{payment_key}/confirm"
    headers = get_auth_header(SECRET_KEY)
    payload = {
        "orderId": order_id,
        "amount": amount
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            # 20. 응답 JSON의 status, orderName, totalAmount, method, approvedAt을 표에 보여 주고, 원본 JSON도 아래에 그대로 보여 준다
            # Display specific fields
            display_data = {
                "status": response_data.get("status"),
                "orderName": response_data.get("orderName"),
                "totalAmount": response_data.get("totalAmount"),
                "method": response_data.get("method"),
                "approvedAt": response_data.get("approvedAt")
            }
            return render_template("success.html", result=display_data, raw_json=json.dumps(response_data, indent=2, ensure_ascii=False))
        else:
            # 실패 시 HTTP 상태와 code, message를 보여준다
            return render_template("fail.html", code=response_data.get("code"), message=response_data.get("message")), response.status_code

    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500

@app.route("/fail")
def fail():
    # 21. GET /fail : 쿼리의 code, message를 보여 준다
    code = request.args.get("code")
    message = request.args.get("message")
    return render_template("fail.html", code=code, message=message)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
