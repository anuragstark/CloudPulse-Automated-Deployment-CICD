from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    env = os.environ.get('ENVIRONMENT', 'development')
    return render_template('index.html', environment=env)

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)