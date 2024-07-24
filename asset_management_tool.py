import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from bs4 import BeautifulSoup

file_paths = []
graphic_card = ""
monitor_data = ""

def upload_files():
    global file_paths
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        file_list = "\n".join(file_paths)
        label.config(text=f"Files selected:\n{file_list}")

def Submit_files():
    global graphic_card, monitor_data
    
    if not file_paths:
        messagebox.showerror("Error", "No files selected")
        return

    data = []
    for path in file_paths:
        file_name = path.split("/")[-1] 
        Parts = file_name.split('_')
        
        # Extract information from HTML file
        html_file_path = path  # Assuming the HTML file is the uploaded file
        extracted_data = extract_info_from_html(html_file_path)

        # Append data to the list
        data.append({
            "System Name": Parts[0], 
            "Department": Parts[1], 
            "Emp Name": Parts[2], 
            "Location": Parts[3], 
            "Block": Parts[4], 
            "Port": Parts[5].split('.')[0],
            "Operating System": extracted_data.get("Operating System", ""),
            "Processor": extracted_data.get("Processor", ""),
            "Board": extracted_data.get("Main Circuit Board", ""),
            "Drive": extracted_data.get("Drives", ""),
            "RAM": extracted_data.get("Memory Modules", ""),
            "Graphic Card": graphic_card,
            "Monitor": monitor_data
        })

    df = pd.DataFrame(data)

    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if save_path:
        df.to_excel(save_path, index=False)
        messagebox.showinfo("Success", f"File saved: {save_path}")
        root.destroy()  # Close the tkinter window after saving the file

def extract_info_from_html(file_path):
    global graphic_card, monitor_data
    
    # Function definition for extracting data from HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    specific_caption_texts = ["Operating System", "Processor", "Main Circuit Board", "Drives", "Memory Modules", "Display"]
    extracted_data = {}
    
    for specific_caption_text in specific_caption_texts:
        found_caption = None
        captions = soup.find_all('caption')
        
        for caption in captions:
            if specific_caption_text in caption.get_text(strip=True):
                found_caption = caption
                break
        
        if found_caption:
            table_tag = found_caption.find_parent('table')
        
            table_data = []
            rows = table_tag.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = []
                
                for cell in cells:
                    cell_content = cell.get_text(separator="<br>").strip().split('<br>')
                    
                    if specific_caption_text == "Display":
                        if len(cell_content) > 1:
                            graphic_card = cell_content[0].strip()
                            monitor_data = cell_content[1].strip()
                        else:
                            graphic_card = cell_content[0].strip()
                            monitor_data = ""  # Set monitor_data to empty if no second line
                    elif specific_caption_text == "Memory Modules":
                        # Convert MB to GB for RAM field
                        if len(cell_content) > 0:
                            ram_info = cell_content[0].strip()
                            # Find and convert any RAM size from MB to GB
                            ram_gb = convert_mb_to_gb(ram_info)
                            # Extract first two words
                            ram_gb_first_two_words = ' '.join(ram_gb.split()[:2])
                            row_data.append(ram_gb_first_two_words)
                    elif specific_caption_text == "Drives":
                        if len(cell_content) > 0:
                            drive_info = cell_content[0].strip()
                            # Convert to TB if size is greater than 1000 GB
                            drive_tb = convert_gb_to_tb(drive_info)
                            row_data.append(drive_tb)
                    else:
                        row_data.append(cell_content[0].strip())
                
                table_data.append(row_data)
            
            extracted_data[specific_caption_text] = table_data
        else:
            extracted_data[specific_caption_text] = f"Caption tag containing '{specific_caption_text}' not found."
    
    return extracted_data

def convert_mb_to_gb(ram_info):
    import re
    
    # Regex pattern to find numbers followed by 'Megabytes' and remove the last three digits
    pattern = r'(\d+) Megabytes'
    
    match = re.search(pattern, ram_info)
    if match:
        mb_size = int(match.group(1))
        gb_size = mb_size // 1000  # Convert MB to GB
        ram_gb = f"{gb_size} GB"
        return ram_info.replace(f"{mb_size} Megabytes", ram_gb)
    else:
        return ram_info  # Return original if pattern not found

def convert_gb_to_tb(drive_info):
    gb_size = float(drive_info.split()[0])  # Extract the numeric value of GB
    if gb_size > 1000:
        tb_size = gb_size / 1000
        return f"{tb_size:.1f} TB"
    else:
        return drive_info

# GUI Setup
root = tk.Tk()
root.title("Asset Management Tool")
root.geometry("600x400")

# Styling
root.configure(bg="#87CEEB")

# Main Frame
main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE)
main_frame.pack(pady=50, padx=50, fill=tk.BOTH, expand=True)

# Title Label
title_label = tk.Label(main_frame, text="Asset Management Tool", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333333")
title_label.pack(pady=20)

# Labels
label = tk.Label(main_frame, text="No files selected", wraplength=500, bg="#ffffff", fg="#333333")
label.pack(pady=20)

# Buttons
upload_button = tk.Button(main_frame, text="Upload Files", command=upload_files, bg="#4caf50", fg="#ffffff", padx=10, pady=5, relief=tk.RAISED, bd=2)
upload_button.pack(pady=10)

submit_button = tk.Button(main_frame, text="Submit", command=Submit_files, bg="#007bff", fg="#ffffff", padx=10, pady=5, relief=tk.RAISED, bd=2)
submit_button.pack(pady=10)

# Run the application
root.mainloop()
