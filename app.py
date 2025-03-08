import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random string

# Google Sheets setup
def get_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)
    
    # Open the spreadsheet by its title - change 'Book Opinions Survey' to your sheet name
    sheet = client.open('Book Opinions Survey').sheet1
    
    # Check if the headers are already set
    if sheet.row_count == 0 or (sheet.row_count == 1 and sheet.cell(1, 1).value is None):
        # Set headers for the sheet
        headers = [
            'Nombre del Participante',
            'Título del Libro',
            'Valoración General (1-5)',
            'Valoración de la Estructura (1-5)',
            'Valoración de la Historia (1-5)',
            'Comentarios',
            'Fecha de Envío'
        ]
        sheet.append_row(headers)
        
    return sheet

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        participant_name = request.form['participant_name']
        book_title = request.form['book_title']
        overall_rating = int(request.form['overall_rating'])
        structure_rating = int(request.form['structure_rating'])
        story_rating = int(request.form['story_rating'])
        comments = request.form['comments']
        date_submitted = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Connect to Google Sheet and append data
            sheet = get_google_sheet()
            sheet.append_row([
                participant_name,
                book_title,
                overall_rating,
                structure_rating,
                story_rating,
                comments,
                date_submitted
            ])
            flash('¡Gracias por enviar tu opinión!')
            return redirect(url_for('thank_you'))
        except Exception as e:
            flash(f'Error al enviar tu respuesta: {str(e)}')
    
    return render_template('index.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    # Try to initialize the Google Sheet with headers if needed
    try:
        sheet = get_google_sheet()
    except Exception as e:
        print(f"Error al configurar Google Sheet: {str(e)}")
    
    # Run the Flask app
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)