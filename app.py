from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    text = request.form['text']
    # Save the text to a database or file here
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)