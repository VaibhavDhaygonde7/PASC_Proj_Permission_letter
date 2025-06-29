from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from letter_functions import get_context, generating_prompt, generating_output
from pdf_functions import create_pdf
app = Flask(__name__)


## declaring the variables
instructions = """
Please rewrite the above letter's body to make it sound more formal and grammatically correct.
Do not add or change any factual details.
Output only the final polished letter.
Also write the output in a letter's format. Use newlines and indentation whereever necessary"""

variables = {
    'head_in_charge': 'head_in_charge_here',
    'program_name': 'program_name_here',
    'room_no': 'room_no_here',
    'sender_name': 'sender_name_here',
    'date': 'date_here'
}

template = get_context('Context_for_permission_letter.txt')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/submit', methods=['POST'])
def submit():
    global prompt_generated

    head_in_charge = request.form['head_in_charge']
    program_name = request.form['program_name']
    room_no = request.form['room_no']
    sender_name = request.form['sender_name']
    date = request.form['date']

    ## updating the key-value pairs of "variables" 
    variables['head_in_charge'] = head_in_charge
    variables['program_name'] = program_name
    variables['room_no'] = room_no
    variables['sender_name'] = sender_name
    variables['date'] = date 

    return redirect(url_for('result'))


@app.route('/result')
def result():
    prompt = generating_prompt(template, variables, instructions)
    
    prompt_output = generating_output(prompt)

    return render_template('result.html', prompt_output=prompt_output)


@app.route('/api/download_pdf', methods=['POST']) 
def download_pdf(): 
    data = request.json

    letter_str = data['letter_str']
    
    create_pdf(letter_str)

    print(letter_str)

    return "PDF generated!"


@app.route('/download_pdf')
def serve_pdf():
    return send_from_directory('static/files', 'output_letter.pdf', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)