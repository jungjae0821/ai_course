import base64, json, re
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    total_amount = None
    people_count = None
    items = None
    error_message = None

    if request.method == 'POST':
        # Case 1: Image upload via OCR
        if 'receipt_image' in request.files and request.files['receipt_image'].filename != '':
            image_file = request.files['receipt_image']
            image_bytes = image_file.read()
            
            prompt = "영수증에서 각 항목 이름과 금액을 추출하여 JSON 형식으로 응답해줘. 형식은 [{'item': '항목명', 'price': 금액}, ...] 와 같아야 해. 오직 JSON만 출력해."
            
            try:
                ai_response = ask(prompt, image_bytes)
                items_data = parse_json(ai_response)
                
                if items_data:
                    items = items_data
                    total_amount = sum(item['price'] for item in items_data)
                else:
                    error_message = "읽지 못했습니다"
            except Exception as e:
                print(f"Error: {e}")
                error_message = "읽지 못했습니다"
                
        # Case 2: Manual input calculation
        elif 'total_amount' in request.form:
            try:
                total_amount = int(request.form.get('total_amount', 0))
                people_count = int(request.form.get('people_count', 0))
                
                if people_count > 0:
                    result = total_amount / people_count
                else:
                    result = 0
            except (ValueError, ZeroDivisionError):
                result = 0

    return render_template('index.html', 
                           result=result, 
                           total_amount=total_amount, 
                           people_count=people_count, 
                           items=items,
                           error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
