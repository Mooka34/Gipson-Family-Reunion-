from flask import Flask, render_template, request
from .utilities.price_calculator import (
    REG_HAIRSTYLES_PRICES,
    WEAVE_HAIRSTYLES_PRICES,
    BRAIDS_AND_LOCS_PRICES,
    HAIRCUT_STYLES_PRICES,
    calculate_total_price
)

app = Flask(__name__)

# Day availability and times dictionary
availability_day = {
    "Monday": {
        "Shanice": ["9:00 am", "11:00 am", "1:00 pm", "4:00 pm"],
        "Jamil": ["10:00 am", "12:00 pm", "2:00 pm", "4:00 pm"]
    },
    "Tuesday": {
        "Arrinana": ["10:00 am", "2:00 pm", "3:00 pm", "6:00 pm"],
        "Cherish": ["11:00 am", "4:00 pm", "5:00 pm", "6:00 pm"]
    },
    "Wednesday": {
        "Arrinana": ["9:00 am", "12:00 pm", "3:00 pm", "5:00 pm"],
        "Jamil": ["10:00 am", "5:00 pm"],
        "Cherish": ["11:00 am", "4:30 pm"],
    },
    "Thursday": {
        "Shanice": ["9:00 am", "3:00 pm", "4:00 pm", "5:00 pm"],
        "Jamil": ["9:00 am", "3:00 pm", "4:00 pm", "5:00 pm"],
        "Cherish": ["10:00 am", "5:00 pm"]
    },
    "Friday": {
        "Shanice": ["10:00 am", "12:00 pm", "2:00 pm", "5:00 pm"],
        "Jamil": ["10:00 am", "3:00 pm", "4:00 pm", "6:00 pm"],
        "Cherish": ["10:00 am", "5:00 pm"],
    },
    "Saturday": {
        "Shannice": ["10:00 am", "12:00 pm", "2:00 pm", "4:00 pm"],
        "Jamil": ["9:00 am", "4:00 pm"],
        "Cherish": ["10:00 am", "4:00 pm"],
    },
    "Sunday": {
        "Jamil": [],
        "Cherish": [],
        "Shannice": [],
        "Arrianna": []
    }
}


@app.route('/')
def appointment_form():
    # Pass service options to the template
    services = list(REG_HAIRSTYLES_PRICES.keys()) + list(WEAVE_HAIRSTYLES_PRICES.keys()) + list(
        BRAIDS_AND_LOCS_PRICES.keys()) + list(HAIRCUT_STYLES_PRICES.keys())
    return render_template("Index.html", services=services, availability=availability_day)


@app.route('/submit_appointment', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        services_input = request.form['services']
        selected_services = [service.strip() for service in services_input.split(',')]
        day = request.form['day']
        time = request.form['time']
        hairdresser = request.form['hairdresser']

        # Check if day is Sunday
        if day == "Sunday":
            return render_template('Error.html', results={'error_message': 'Sorry, we are closed on Sundays. Please select another day'})

        # Check if the selected services are provided
        if not all(service in REG_HAIRSTYLES_PRICES or service in WEAVE_HAIRSTYLES_PRICES or
                   service in BRAIDS_AND_LOCS_PRICES or service in HAIRCUT_STYLES_PRICES for service in selected_services):
            return render_template('Error.html', results={'error_message': 'One or more selected services are not provided.'})

        # Check if hairdresser is available on the selected day
        if hairdresser not in availability_day.get(day, {}):
            return render_template('Error.html', results={'hairdresser_not_available': True})

        # Check if the selected time is available for the chosen hairdresser on this day
        if time not in availability_day[day].get(hairdresser, []):
            available_times = ", ".join(availability_day[day].get(hairdresser, []))
            return render_template('Error.html', results={'time_not_available': True, 'available_times': available_times})

        # Calculate total price for selected services
        total_price = calculate_total_price(selected_services)

        # Render appointment confirmation page with the appointment details
        return render_template('Appointment_details.html', day=day, time=time, total_price=total_price,
                               hairdresser=hairdresser, selected_services=selected_services)
    else:
        # Initial GET request, render the form
        return render_template('index.html', availability=availability_day)


if __name__ == '__main__':
    app.run(debug=True)
