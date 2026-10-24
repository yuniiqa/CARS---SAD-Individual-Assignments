### MediCare Clinic Appointment & Record System (CARS)

Course: BIT3134 System Analysis and Design
Assignment: Individual Assignment (Prototype Appendix)
Student Name: [Your Name]
Student ID: [Your ID]

### Project Overview

This repository contains the Python source code for the Clinic Appointment & Record System (CARS) prototype. This system was designed to address the operational bottlenecks of a small clinic transitioning from a manual, paper-based booking system to a digital information system.

This prototype serves as a visual appendix for the written report, demonstrating how the Structured Decision Logic (Task 4) is implemented in a real-world software environment.

### System Requirements

To run this application locally, you need:

· Python 3.8+ installed on your computer.
· The Streamlit and Pandas libraries.

### How to Run the Prototype Locally

If you wish to test the system on your own machine, follow these steps:

1. Clone the repository or download the app.py file.
2. Open your terminal or command prompt.
3. Install the required libraries:
   ```bash
   pip install streamlit pandas
   ```
4. Navigate to the folder containing app.py and run:
   ```bash
   streamlit run app.py
   ```
5. A browser window will automatically open showing the web application.

### Key Feature: Decision Logic Implementation

This prototype specifically demonstrates the Decision Table and Structured English outlined in Section 4.0 of the report.

When you use the "Patient Portal", the system automatically processes the following rules:

· Rule 1: Checks if the patient is registered and if the slot is available (Confirms Booking).
· Rule 2 & 3: If the slot is taken or doctor is off-duty, it offers an alternative.
· Rule 4: If the slot is taken but the user checks the "Emergency" box, the system overrides the standard flow and escalates the case.
· Rule 6: Blocks unregistered patients from booking.

### Repository Contents

· app.py - The main Python code containing the Streamlit UI and decision logic.
· requirements.txt - The list of dependencies required to run the app.
· README.md - This instruction file.

---

Note: This prototype was developed as a supplementary visual aid for the BIT3134 Individual Assignment. All logic, scenarios, and system boundaries strictly follow the written report.
