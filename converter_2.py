from astropy.time import Time
import tkinter as tk
from tkinter import filedialog, messagebox


class Converter:

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def work_with_file(self):
        try:

            with open(file=self.infile, mode='r', encoding='utf-8') as infile, open(file=self.outfile, mode='w', encoding='utf-8') as outfile:
                outfile.write('Column1 Column2 Column3 Column4 GPS_Time\n')
                for line in infile:
                    columns = line.strip().split()

                    if len(columns) < 4:
                        print(f"Skipping line with less than 4 columns: {line.strip()}")
                        continue

                    minutes_from_1980 = float(columns[0])
                    formatted_time = self.gps_time_to_hhmmss(minutes_from_1980)
                    outfile.write(f'{columns[0]} {columns[1]} {columns[2]} {columns[3]} {formatted_time}\n')

        except FileNotFoundError:
            print(f"Input file '{self.infile}' not found.")
        except IOError as e:
            print(f"Error reading/writing file: {e}")

    def gps_time_to_hhmmss(self, minutes_from_1980):

        gps_time = Time(minutes_from_1980, format='gps')
        utc_time = gps_time.utc

        formatted_time = utc_time.strftime("%H:%M:%S.%f")[:-2]

        return formatted_time

    # def run(self):
    #     self.work_with_file()


def main():
    root = tk.Tk()
    root.title("GPS Time Converter")

    # Input File frame
    input_frame = tk.Frame(root)
    input_frame.pack(padx=10, pady=10)

    tk.Label(input_frame, text="Input File").pack(side=tk.LEFT)
    input_var = tk.StringVar()
    input_entry = tk.Entry(input_frame, textvariable=input_var)
    input_entry.pack(side=tk.LEFT)

    def select_input_file():
        file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text files", "*.txt")])
        if file_path:
            input_var.set(file_path)

    select_button = tk.Button(input_frame, text="Browse", command=select_input_file)
    select_button.pack(side=tk.LEFT)

    # Output File frame
    output_frame = tk.Frame(root)
    output_frame.pack(padx=10, pady=10)

    tk.Label(output_frame, text="Output File").pack(side=tk.LEFT)
    output_var = tk.StringVar()
    output_entry = tk.Entry(output_frame, textvariable=output_var)
    output_entry.pack(side=tk.LEFT)

    def select_output_file():
        file_path = filedialog.asksaveasfilename(title="Select Output File", defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            output_var.set(file_path)

    select_button = tk.Button(output_frame, text="Browse", command=select_output_file)
    select_button.pack(side=tk.LEFT)

    convert_button = tk.Button(root, text="Convert", command=lambda: convert_files())
    convert_button.pack(pady=10)

    def convert_files():
        infile = input_var.get()
        outfile = output_var.get()
        if infile and outfile:
            converter = Converter(infile=infile, outfile=outfile)
            converter.run()
        else:
            messagebox.showerror("Error", "Please select both input and output files.")

    # layout = [
    #     [sg.Text("Input File"), sg.Input(key="-INFILE-"), sg.FileBrowse()],
    #     [sg.Text("Output File"), sg.Input(key="-OUTFILE-"), sg.FileSaveAs()],
    #     [sg.Button("Convert"), sg.Button("Exit")]
    # ]
    #
    # window = sg.Window("GPS Time Converter", layout)
    # while True:
    #     event, values = window.read()
    #     if event == sg.WINDOW_CLOSED or event == "Exit":
    #         break
    #     elif event == "Convert":
    #         infile = values["-INFILE-"]
    #         outfile = values["-OUTFILE-"]
    #         if infile and outfile:
    #             converter = Converter(infile=infile, outfile=outfile)
    #             converter.run()
    #         else:
    #             sg.popup("Please select both input and output files.")
    #
    # window.close()


if __name__ == '__main__':
    # import PySimpleGUI as sg
    main()