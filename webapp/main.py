from flask import Flask, render_template
from dataset_reader import GFF3DatasetReader

# reading the human genome
filepath='Homo_sapiens.GRCh38.85.gff3.gz'
reader = GFF3DatasetReader()
human_genome = reader.read(filepath)

# Setting up the application
app = Flask(__name__, static_folder='static')

# making route
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/active_operations')
def active_operations():
    return render_template('active_operations.html')

@app.route('/operation')
def operation():
    return render_template('operation.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')
  
# running application
if __name__ == '__main__':
    app.run(debug=True)