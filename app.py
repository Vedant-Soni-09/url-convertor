from flask import Flask, render_template, request, jsonify
import requests
import json
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        url = 'https://ekaro-api.affiliaters.in/api/converter'
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Origin': 'https://ek.affiliaters.in',
            'Referer': 'https://ek.affiliaters.in/',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2M2UzNGU3N2NkMWUyODJlMmY5NTRjNzIiLCJlYXJua2FybyI6IjkzMjA4MiIsImlhdCI6MTY5MTY0MTEyMX0.iOUAv99_c27iUPZ_K1sVrMZ3Mg-ch_LQ9Npoc9YY0i0'
        }

        link = request.form['link']
        if not link.startswith("http://") and not link.startswith("https://"):
            link = "https://"+link

        data = {
            'deal': link,
            'convert_option': 'convert_only'
        }

        # Simulate processing delay (remove this line in production)
        # time.sleep(3)

        response = requests.post(url=url, headers=headers, json=data)
        if 'Url not found in post!' in response.text:
            result = 'URL not found!'
        
        else:
            jsondata = json.loads(response.text)
            data = jsondata['data']

            if 'We could not locate an affiliate URL to send. Please verify if the seller is available on the EarnKaro website.' in data:
                result = 'This Seller is not in our list. You can shop as usual on this site.\nThanks for using our converter. <3'
            else:
                result = data

        return jsonify({'result': result})

    return render_template('index.html', result=None)
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')