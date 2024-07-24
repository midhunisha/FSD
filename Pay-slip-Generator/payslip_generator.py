import os
import pandas as pd
from tkinter import Tk, filedialog, Button, Label, Entry, messagebox, Frame
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# Global variables
selected_file_path = ""
df = None  # This will hold the dataframe after reading the Excel file

def read_excel(file_path):
    return pd.read_excel(file_path)

def format_date(date):
    if pd.isnull(date):
        return ""
    return date.strftime('%d-%m-%Y')

def create_pdf_with_reportlab(row, output_dir):
    pdf_name = str(row.iloc[0])  # Assuming the first column contains the PDF name
    output_path = os.path.join(output_dir, f'{pdf_name}.pdf')

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Convert date format
    date_of_joining = format_date(pd.to_datetime(row.iloc[3]))

    # Title
    title_lines = [
        "SYMBIOSYS TECHNOLOGIES",
        "Plot No 1&2, Hill no-2, IT Park,",
        "Rushikonda, Visakhapatnam-45",
        "Ph: 2550369, 2595657"
    ]
    
    c.setFont('Helvetica-Bold', 12)
    text_height = height - 50
    for line in title_lines:
        c.drawCentredString(width / 2, text_height, line)
        text_height -= 18  # Adjusting vertical spacing between lines
    
    # Heading below title
    heading_text = "SALARY STATEMENT FOR THE MONTH OF JULY 2024"
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(width / 2, text_height - 30, heading_text)
    text_height -= 80  # Adjusting vertical spacing after heading
    
    # Table 1: Employee details
    table1_data = [
        ['Employee Code', 'Employee Name', 'Designation'],
        [str(row.iloc[0]), row.iloc[1], row.iloc[2]]
    ]
    table1 = Table(table1_data, colWidths=150)
    table1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header row
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Regular font for data rows
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    table1.wrapOn(c, width, height)
    table1.drawOn(c, width / 2 - table1._width / 2, text_height - 30)
    
    text_height -= 50  # Adjusting vertical spacing after table 1

    # Table 2: Employment details
    table2_data = [
        ['Date of Joining', 'Employment Status', 'Statement for the month'],
        [date_of_joining, row.iloc[4], "JULY"]
    ]
    table2 = Table(table2_data, colWidths=150)
    table2.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header row
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Regular font for data rows
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    table2.wrapOn(c, width, height)
    table2.drawOn(c, width / 2 - table2._width / 2, text_height - 30)
    
    text_height -= 100  # Adjusting vertical spacing after table 2

    # Convert numeric columns to floats
    for col in range(5, 17):
        row.iloc[col] = pd.to_numeric(row.iloc[col], errors='coerce')

    # Table 3: Income and Deductions
    table3_data = [
        ['Classified Income', 'Amount (Rs.)', 'Deductions', 'Amount (Rs.)'],
        ['Basic Pay', f"Rs. {row.iloc[6]:.2f}", 'Professional Tax', f"Rs. {row.iloc[12]:.2f}"],
        ['House Rent Allowance', f"Rs. {row.iloc[7]:.2f}", 'Income Tax', f"Rs. {row.iloc[13]:.2f}"],
        ['City Compensatory Allowance', f"Rs. {row.iloc[8]:.2f}", 'Provident Fund', f"Rs. {row.iloc[14]:.2f}"],
        ['Travel Allowance', f"Rs. {row.iloc[9]:.2f}", 'ESI', f"Rs. {row.iloc[15]:.2f}"],
        ['Food Allowance', f"Rs. {row.iloc[10]:.2f}", 'Leaves-Loss of Pay', f"Rs. {row.iloc[16]:.2f}"],
        ['Performance Incentives', f"Rs. {row.iloc[11]:.2f}", 'Others', f"Rs. {row.iloc[17]:.2f}"]
    ]
    table3 = Table(table3_data)
    table3.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header row
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Regular font for data rows
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    table3.wrapOn(c, width, height)
    table3.drawOn(c, width / 2 - table3._width / 2, text_height - 70)

    text_height -= 90  # Adjusting vertical spacing after table 3

    # Table 4: Gross Pay, Deductions, Net Pay
    table4_data = [
        ['Gross Pay', 'Deductions', 'Net Pay'],
        [f"Rs. {row.iloc[18]:.2f}", f"Rs. {row.iloc[19]:.2f}", f"Rs. {row.iloc[20]:.2f}"]
    ]
    table4 = Table(table4_data, colWidths=150)
    table4.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header row
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Regular font for data rows
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    table4.wrapOn(c, width, height)
    table4.drawOn(c, width / 2 - table4._width / 2, text_height - 30)

    # Adding text below Table 4
    text_height -= 100  # Move further down below Table 4
    c.setFont('Helvetica-Bold', 10)
    c.drawString(50, text_height, "AUTHORISED SIGNATORY")
    sign = ["Durga Prasad",
            "H.R Executive"]
    text_height -= 50
    for line in sign:
        c.drawString(50, text_height, line)
        text_height -= 15
    text_height -= 10
    c.setFont('Helvetica', 8) 
    c.drawString(50, text_height, "We request you to verify employment details with our office on email: hr@symbiosistech.com. (+91-0891-2550369)")

    # Save PDF
    c.save()

def select_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if selected_file_path:
        lbl_file_selected.config(text=f"Selected File: {os.path.basename(selected_file_path)}")
        # Read the Excel file into the global variable df
        global df
        df = read_excel(selected_file_path)
        # Enable the search entry and button
        entry_search.config(state="normal")
        btn_search.config(state="normal")
    else:
        lbl_file_selected.config(text="No file selected")
        # Disable search entry and button if no file selected
        entry_search.config(state="disabled")
        btn_search.config(state="disabled")

def search_employee():
    if not df.empty:
        employee_id = entry_search.get().strip()
        if employee_id.isdigit():
            employee_id = int(employee_id)
            row = df[df.iloc[:, 0] == employee_id]  # Assuming employee ID is in the first column
            if not row.empty:
                row = row.iloc[0]  # Take the first matching row (should be unique)
                output_dir = filedialog.askdirectory()
                if output_dir:
                    create_pdf_with_reportlab(row, output_dir)
                    messagebox.showinfo("Success", f"Payslip for Employee ID {employee_id} created successfully")
                    entry_search.delete(0, 'end')  # Clear the search entry
                    app.destroy()
                else:
                    messagebox.showerror("Error", "No output directory selected")
            else:
                messagebox.showerror("Error", f"No employee found with Employee ID {employee_id}")
        else:
            messagebox.showerror("Error", "Please enter a valid Employee ID (numeric)")
    else:
        messagebox.showerror("Error", "No Excel file loaded or empty data")

# Initialize Tkinter app
app = Tk()
app.title("Payslip Generator")
app.geometry("400x350")
app.configure(bg="#f0f0f0")

# Create a frame for the content
frame = Frame(app, bg="#e6e6e6", bd=2, relief="groove")
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Instructions label
lbl_instruction = Label(frame, text="Select an Excel file to convert to PDF files:", bg="#e6e6e6", font=("Arial", 12, "bold"))
lbl_instruction.pack(pady=10)

# Select file button
btn_select_file = Button(frame, text="Select File", command=select_file, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), relief="raised", bd=2)
btn_select_file.pack(pady=10)

# Selected file label
lbl_file_selected = Label(frame, text="No file selected", bg="#e6e6e6", font=("Arial", 10, "italic"))
lbl_file_selected.pack(pady=5)

# Entry for employee ID search
entry_search = Entry(frame, width=30, state="disabled", font=("Arial", 10))
entry_search.pack(pady=10)

# Search button
btn_search = Button(frame, text="Search Employee", command=search_employee, bg="#008CBA", fg="white", font=("Arial", 10, "bold"), relief="raised", bd=2, state="disabled")
btn_search.pack(pady=10)

# Start the Tkinter main loop
app.mainloop()
