from astropy.time import Time


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

    def run(self):
        self.work_with_file()


def main():
    layout = [
        [sg.Text("Input File"), sg.Input(key="-INFILE-"), sg.FileBrowse()],
        [sg.Text("Output File"), sg.Input(key="-OUTFILE-"), sg.FileSaveAs()],
        [sg.Button("Convert"), sg.Button("Exit")]
    ]

    window = sg.Window("GPS Time Converter", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Convert":
            infile = values["-INFILE-"]
            outfile = values["-OUTFILE-"]
            if infile and outfile:
                converter = Converter(infile=infile, outfile=outfile)
                converter.run()
            else:
                sg.popup("Please select both input and output files.")

    window.close()

    # infile = '1.txt'
    # outfile = '1_new.txt'
    # converter = Converter(infile=infile, outfile=outfile)
    # converter.run()


if __name__ == '__main__':
    import PySimpleGUI as sg
    main()