from fpdf import FPDF
import pandas as pd
import os

class PdfWritter():

    def __init__(self, Datapath, BasePath):
        """
        :param Datapath: Input CSV file path
        :param BasePath of current folder
        """
        self.path=Datapath
        self.Basepath=BasePath

    def pdf_generate(self,ref_no,account_no,garrentee_no,name,address,date,Email_id):
        """
        This Function gives pdf output in a OutputData folder
        :param ref_no
        :param account_no
        :param garrentee_no
        :param name name
        :param address
        :param date is date of birth
        :param Email_id
        """
        pdf = FPDF(format='A4',unit='in')
        pdf.set_margins(1.0,0.0,0.8)
        pdf.add_page()
        pdf.set_font('arial', '', 10)
        column_width = 6.5
        column_spacing = 0.15
        ybefore = pdf.get_y()
        pdf.set_xy(column_width + pdf.l_margin + column_spacing, ybefore)
        pdf.cell(column_width,1, txt="", ln=1)
        pdf.cell(column_width,0.2, txt=("Ref No.  : "+str(ref_no)), ln=1)
        pdf.cell(column_width,0.2, txt=("Account No.: "+str(account_no)), ln=1)
        pdf.cell(column_width,0.2, txt="", ln=1, align="L")
        pdf.set_font("arial", 'B', 12)
        pdf.cell(column_width,0.2, txt="Python Script to Write pdf".rjust(60,' '), ln=1, align="L")
        pdf.cell(column_width,0.2, txt="", ln=1, align="L")
        pdf.set_font("arial", size=10)
        pdf.cell(column_width,0.2, txt=("Name :  "+name), ln=1, align="L")
        pdf.cell(column_width,0.2, txt="", ln=1, align="C")
        pdf.cell(column_width,0.2, txt=("Address : ".ljust(7)+address), ln=1, align="L")
        pdf.cell(column_width,0.2, txt=("Date of birth : "+str(date)), ln=1, align="L")
        pdf.cell(column_width,0.2, txt="", ln=1, align="L")
        pdf.cell(column_width,0.2, txt="Email Id : "+Email_id, ln=1, align="L")
        pdf.image(self.Basepath+'/InputImage/sign.jpg', x=1.0, y=3.3, w=2.5)
        pdf.line(3.4, 4.05, 1.1, 4.05)
        pdf.set_line_width(1)
        pdf.set_draw_color(255, 255, 255)
        pdf.cell(column_width, 0.91, txt="", ln=1, align="L")
        pdf.cell(column_width, 0.2, txt="Authorized Signature",ln=1, align="L")
        pdf.ln(0.1)
        pdf.cell(column_width, 0.4, txt="Visualizing Tabuler data in pdf all formate : "+str(garrentee_no),ln=1, align="L")
        pdf.ln(0.4)
        pdf.set_font("arial", 'B', 11)
        data = [['City No ', 'Work Permit To ', 'City No ', 'Work Permit To']]
        spacing = 1.5
        col_width = pdf.w / 5.5
        row_height = pdf.font_size
        for row in data:
            for item in row:
                pdf.cell(col_width, row_height * spacing,
                         txt=item, border=1)
            pdf.ln(row_height * spacing)
        pdf.set_font("arial", '', 11)
        work_permit_no = ['Mum 43712-', 'bang 3712-', 'Hyd 43712-', 'Pune 171-', 'delhi 371-', 'US 743-', 'UK 743712-']
        df = pd.DataFrame({'City No': [], 'Work Permit To': [], 'City No.': [], 'Work Permit To.': []})
        for i, item in enumerate(work_permit_no):
            j='{:d}'.format(i+1).zfill(3)
            if (i+1) % 2 == 0:
                df = df.append({'City No ': j, 'Work Permit To ': item}, ignore_index=True)
            else:
                df = df.append({'City No': j, 'Work Permit To': item}, ignore_index=True)
        df1 = df.dropna(subset=['City No'], how='all')
        df2 = df.dropna(subset=['City No '], how='all')
        result1 = pd.concat([df1['City No'], df1['Work Permit To']], axis=1, sort=False)
        result2 = pd.concat([df2['City No '], df2['Work Permit To ']], axis=1, sort=False)
        result1.reset_index(drop=True, inplace=True)
        result2.reset_index(drop=True, inplace=True)
        result = pd.concat([result1, result2], axis=1)
        result=result.to_string(justify='left',index=False,header=False,col_space=30,na_rep='',float_format="%d")
        pdf.multi_cell(column_width, 0.30, result)
        data = os.path.isdir(self.Basepath+'\\'+'OutputData')
        if data is False:
            os.mkdir(self.Basepath+'\\'+'OutputData')
        pdf.output(self.Basepath+'/OutputData/pdf.pdf', 'F')

    def get_data(self):
        """
         CSV file Data as parameters to pdf_generate function and this function calls pdf_generate function
        """
        try:
            sheet = pd.read_csv(self.path)
            for index, row in sheet.head().iterrows():
                print(row['ref_no'])
                PdfWritter.pdf_generate(self,row['ref_no'],row['account_no'],row['garrentee_no'],row['name'],row['address'],row['date of birth'],row['Email_id'])
        except Exception as e:
          print(e)

if __name__=="__main__":
    BasePath = os.getcwd()
    obj = PdfWritter(BasePath+'/InputData/data.csv',BasePath)
    obj.get_data()











