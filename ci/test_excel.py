import xlsxwriter as xw

def export_to_xl(distance_data, cadence_data, time_data):

    workbook = xw.Workbook('test.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Distance data')
    worksheet.write('B1', 'Cadence data')
    worksheet.write('C1', 'Time data')

    for data in range(1,len(time_data)):
        worksheet.write(data, 0, distance_data[data])
        worksheet.write(data, 1, cadence_data[data])
        worksheet.write(data, 2, time_data[data])

    workbook.close()
