"""
    Author: Ojelle Rogero
    Created on: November 14, 2021
    Modified on: April 8, 2022
    About:
        Converts the Weekly Market Recap section of GSAM Market Monitor
        Parse each asset type and save as a data table in separate sheet
    Modification / Updates:
        Function definition, input and output parameters are added.
"""

import os
import tabula
import pandas as pd


class pdfConvert():

    def __init__(self, file, output):
        self.file = file
        self.output = output


    def readPdf(self, box, pg, strm):
        """
          Reads the table section with its designated bounding box. Parsed the table and returns a dataframe.
            :param box:
              bounding box - list; boundary box or section of the table to parse
            :param pg:
              pdf page - int; the page section of the pdf to parse
            :param strm:
              stream mode - True or False; used to parse tables with whitespaces between cells to simulate table like structure
            :return:
              returns a dataframe output
        """
        box_fc = [box[i] * 28.28 for i in range(0, 4)]
        df = tabula.read_pdf(self.file, pages=pg, area=[box_fc], output_format='dataframe', stream=strm)
        return df


    def indexReturns(self):
        """
          Parse the Index Returns table (page 3 of the pdf)
            :return:
              returns the parsed table as dataframe
        """
        df = self.readPdf([2, 0, 20, 11], 3, True)[0]
        marketType = df.columns.values[0]
        prd = df.iloc[0, :]
        period = [prd[i] for i in range(0, len(prd)) if pd.isnull(prd[i]) == False]
        idxType = df.iloc[:, 0]
        indexType = [idxType[i] for i in range(0, len(idxType)) if pd.isnull(df.iloc[:, 1][i]) == True]
        idx = df[df.iloc[:, 0].isin(indexType)].index

        data = pd.DataFrame()
        for i in range(0, len(idx)):
            if i < len(idx) - 1:
                temp1 = df[idx[i] + 1 : idx[i+1]].reset_index(drop=True)
            else:
                temp1 = df[idx[i] + 1: len(df)].reset_index(drop=True)
            temp1 = pd.concat([pd.DataFrame([marketType] * len(temp1)),
                               pd.DataFrame([indexType[i]] * len(temp1)),
                               temp1], axis=1, ignore_index=True)
            data = data.append(temp1, ignore_index=True)

        data.columns = ["Type", "Asset Type", "Indices", period[0], period[1], period[2], period[3]]
        return data


    def commodities(self):
        """
          Parse the Commodities table (page 3 of the pdf)
            :return:
              return the parsed table as dataframe
        """
        df = self.readPdf([20, 0, 23, 11], 3, True)[0]
        marketType = df.columns.values[0]
        prd = df.iloc[0, :]
        period = [prd[i] for i in range(0, len(prd)) if pd.isnull(prd[i]) == False]

        data =  df[1 : len(df)].reset_index(drop=True)
        data = pd.concat([pd.DataFrame([marketType] * len(data)), data], axis=1, ignore_index=True)

        data.columns = ["Asset Type", "Commodities", period[0], period[1], period[2], period[3]]
        return data


    def currencies(self):
        """
          Parse the Currencies table (page 3 of the pdf)
            :return:
              returns the parsed table as dataframe
        """
        df = self.readPdf([23, 0, 27, 11], 3, True)[0]
        marketType = df.columns.values[0]
        prd = df.iloc[0, :]
        period = [prd[i] for i in range(0, len(prd)) if pd.isnull(prd[i]) == False]

        data = df[1: len(df)].reset_index(drop=True)
        data = pd.concat([pd.DataFrame([marketType] * len(data)), data], axis=1, ignore_index=True)

        data.columns = ["Asset Type", "Currency Pair", period[0], period[1], period[2], period[3]]
        return data


    def ratesSpreads(self):
        """
          Parse the Rates & Spreads table (page 3 of the pdf)
            :return:
              returns the parsed table as dataframe
        """
        df = self.readPdf([2, 11, 13, 22], 3, True)[0]
        marketType = df.columns.values[0]
        prd = df.iloc[0, :]
        period = [prd[i] for i in range(0, len(prd)) if pd.isnull(prd[i]) == False]
        rtType = df.iloc[:, 0]
        rateType = [rtType[i] for i in range(0, len(rtType)) if
                     pd.isnull(df.iloc[:, 1][i]) == True]
        idx = df[df.iloc[:, 0].isin(rateType)].index

        data = pd.DataFrame()
        for i in range(0, len(idx)):
            if i < len(idx) - 1:
                temp1 = df[idx[i] + 1: idx[i + 1]].reset_index(drop=True)
            else:
                temp1 = df[idx[i] + 1: len(df)].reset_index(drop=True)
            temp1 = pd.concat([pd.DataFrame([marketType] * len(temp1)),
                               pd.DataFrame([rateType[i]] * len(temp1)),
                               temp1], axis=1, ignore_index=True)
            data = data.append(temp1, ignore_index=True)

        data.columns = ["Type", "Rate or Spread", "Items", period[0], period[1], period[2], period[3]]
        return data


    def weeklyMarketRecap(self):
        """
          Saves output as an xlsx
        """
        idxRet = self.indexReturns()
        comm = self.commodities()
        curr = self.currencies()
        rtSp = self.ratesSpreads()

        with pd.ExcelWriter(self.output) as writer:
            idxRet.to_excel(writer, sheet_name="index_returns", index=False)
            comm.to_excel(writer, sheet_name="commodities", index=False)
            curr.to_excel(writer, sheet_name="currencies", index=False)
            rtSp.to_excel(writer, sheet_name="rates_spreads", index=False)


if __name__ == '__main__':
    file_path = # path where the pdf file is saved
    input_file = # pdf file name
    out_path = # path where to save the xlsx output
    output_file = # xlsx output file name

    convert = pdfConvert(os.path.join(file_path, input_file), os.path.join(out_path, output_file))
    convert.weeklyMarketRecap()
    print(f'Done converting {input_file}')