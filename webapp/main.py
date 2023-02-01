from flask import Flask, render_template
  
# Setting up the application
app = Flask(__name__, static_folder='static')

# making route
@app.route('/')
def home():
    return render_template('Homepage.html')

@app.route('/activeoperations')
def active_operations():
    return render_template('actops.html')

@app.route('/operations')
def operations():
    return render_template('ops.html')

@app.route('/projectdocumentation')
def proj_documentation():
    return render_template('projdoc.html')
  
  
# running application
if __name__ == '__main__':
    app.run(debug=True)