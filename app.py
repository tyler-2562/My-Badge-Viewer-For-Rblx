from flask import Flask, render_template, request, jsonify
import requests, os, json

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/badgestest')
def badgestest():
    json_path = os.path.join('json','tyler.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return render_template('badgestest.html', data=data)


# 

# Route to handle badge request via AJAX
@app.route('/badges', methods=['POST'])
def badges():
    user_id = request.form['user_id']  # Get the user ID from the form input
    
    # Call the Roblox API to get badges for the user
    url = f'https://badges.roblox.com/v1/users/{user_id}/badges?limit=100&sortOrder=Asc'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        badges_data = response.json()
        
        if 'data' in badges_data and badges_data['data']:
            return jsonify(badges_data['data'])
        else:
            return jsonify({'message': 'No badges found for this user.'})
    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Failed to fetch badges.'})

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
