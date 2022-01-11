#!/usr/bin/env python3

# vast_pdf: Library of functions to create PDF reports of various type.
# Currently only makes invoices.

import datetime
import math
import time
import random
from decimal import Decimal

import typing

import PIL.Image
from borb.pdf.canvas.color.color import HexColor, X11Color
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.table.table import Table, TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

## Globals
num_rows_first_page = 10
num_rows_subsequents_pages = 25
invoice_total = 0
invoice_number = random.randint(1000, 10000)
page_count = 0



def build_2nd_block_table() -> Table:
    """
    This function builds a Table containing invoice information.
    This information spans the page and is the second large block of
    text on the page.

    :return:    a Table containing invoice information
    """
    global invoice_total
    now = datetime.datetime.now()
    table_001 = FixedColumnWidthTable(number_of_rows=5, number_of_columns=3)

    table_001.add(Paragraph("Vast.ai Inc."))
    table_001.add(Paragraph("Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year), horizontal_alignment=Alignment.RIGHT))

    table_001.add(Paragraph("100 Van Ness Ave."))
    table_001.add(Paragraph("Payment Terms:", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("Charged - Do Not Pay", horizontal_alignment=Alignment.RIGHT))

    table_001.add(Paragraph("San Francisco CA 94102"))

    table_001.add(
        Paragraph("Total", font="Helvetica-Bold", font_size=Decimal(20), horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph(f'-${invoice_total:.2f}', font="Helvetica-Bold", font_size=Decimal(20),
                            horizontal_alignment=Alignment.RIGHT))

    table_001.add(Paragraph("fixme@vast.ai"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.add(Paragraph("https://vast.ai/"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def blank_row(table, col_num, row_num=1):
    """Just a set of blank rows to act as filler.
    :param table: The table we want to modify
    :param int col_num: How many columns in the table?
    :param int row_num: How many blank rows do we need?
    """
    for j in range(row_num):
        for i in range(col_num):
            table.add(Paragraph(" "))


def field_and_blank_line(user_blob, table, fieldname):
    table.add(Paragraph(str(user_blob[fieldname])))
    table.add(Paragraph(" "))


def build_billto_table(user_blob) -> Table:
    """
    This function builds a Table containing billing and shipping information
    It spans the page and uses blank cells to pad the right side of the page
    :param Dict user_blob: A dict containing the user's info.
    :return:    a Table containing shipping and billing information
    """
    table_001 = FixedColumnWidthTable(number_of_rows=6, number_of_columns=2)
    table_001.add(Paragraph("BILL TO", font="Helvetica-Bold"))
    table_001.add(Paragraph(" ", font="Helvetica-Bold"))

    field_ids = ["fullname", "billaddress_line1", "billaddress_line2"]
    print(list(map(lambda fieldname: field_and_blank_line(user_blob, table_001, fieldname), field_ids)))

    table_001.add(Paragraph("%s, %s" % (user_blob["billaddress_city"], user_blob["billaddress_zip"])))  # BILLING
    table_001.add(Paragraph(" "))  # SHIPPING
    table_001.add(Paragraph(" "))  # BILLING
    table_001.add(Paragraph(" "))  # SHIPPING
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


class Charge:
    """
    This class represents a charge line.
    """

    def __init__(self, name: str, quantity: float, rate: float, amount: float):
        self.name: str = name
        assert quantity >= 0
        self.quantity: int = quantity
        assert rate >= 0
        self.price_per_sku: float = rate
        assert amount >= 0
        self.amount: float = amount


def build_charge_table(products: typing.List[Charge] = [],
                       sums: typing.Dict[str, int] = {"quantity": 0, "rate": 0, "amount": 0}):
    """
    This function builds a Table containing itemized billing information
    :param:     List products: the rows on the invoice
    :param:     Dict sums: Dict of fields that can be summed
    :return:    a Table containing itemized billing information
    """
    global invoice_total
    num_rows = len(products)
    table_001 = FlexibleColumnWidthTable(number_of_rows=(num_rows + 3), number_of_columns=4)

    for h in ["Item", "Quantity", "Rate", "Amount"]:
        table_001.add(
            TableCell(
                Paragraph(h, font_color=X11Color("White")),  # vertical_alignment=Alignment.MIDDLE),
                background_color=HexColor("0b3954"), padding_top=Decimal(8), padding_bottom=Decimal(8)
            )
        )

    odd_color = HexColor("BBBBBB")
    even_color = HexColor("FFFFFF")
    for row_number, item in enumerate(products):
        c = even_color if row_number % 2 == 0 else odd_color
        table_001.add(TableCell(Paragraph(item.name, font="Helvetica-Bold"), background_color=c))
        table_001.add(TableCell(Paragraph("     {:10.2f}".format(item.quantity),  # font="Helvetica-Bold",
                                          horizontal_alignment=Alignment.RIGHT), background_color=c))
        table_001.add(TableCell(Paragraph("     -${:10.2f}".format(item.price_per_sku),  # font="Helvetica-Bold",
                                          horizontal_alignment=Alignment.RIGHT), background_color=c))
        table_001.add(
            TableCell(Paragraph("-${:10.2f}".format(item.amount),  # font="Helvetica-Bold",
                                horizontal_alignment=Alignment.RIGHT), background_color=c))

    # Optionally add some empty rows to have a fixed number of rows for styling purposes
    # for row_number in range(len(products), 10):
    #     c = even_color if row_number % 2 == 0 else odd_color
    #     for _ in range(0, 4):
    #         table_001.add(TableCell(Paragraph(" "), background_color=c))

    # total
    # total: float = sum([x.price_per_sku * x.quantity for x in products])
    table_001.add(
        TableCell(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT, ), col_span=3, ))
    table_001.add(TableCell(Paragraph(" ", horizontal_alignment=Alignment.RIGHT)))


    table_001.add(
        TableCell(Paragraph("Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3, ))
    table_001.add(TableCell(Paragraph("-${:10.2f}".format(invoice_total), horizontal_alignment=Alignment.RIGHT)))
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(5), Decimal(2), Decimal(5))
    table_001.no_borders()
    return table_001


def main():
    print("Script called from command line - probably not what we want.")


def product_row(charges):
    """Makes a single row with charge information in it."""
    return Charge(charges["description"], float(charges["quantity"]), float(charges["rate"]),
                  float(charges["amount"]))


def product_rows(rows_invoice=None):
    """Makes a page worth of rows of charges."""
    if rows_invoice is None:
        rows_invoice = []
    return list(map(lambda charges: product_row(charges), rows_invoice))


def build_invoice_charges_table(rows_invoice, charges_per_page=5):
    """This function creates a page of invoice charges and depletes
    the list of charges by the number it prints out."""
    rows_invoice_chunk = rows_invoice[0:charges_per_page]
    sums = {"amount": compute_column_sum(rows_invoice, "amount", True)}
    del rows_invoice[0:charges_per_page]
    return build_charge_table(product_rows(rows_invoice_chunk), sums)


def compute_column_sum(rows_invoice, column_name, values_are_negative=False):
    """Sum over one of the columns in the invoice."""
    s = 0
    for row in rows_invoice:
        if values_are_negative:
            s = s - float(row[column_name])
        else:
            s = s + float(row[column_name])
    return s


def generate_invoice_page(user_blob, rows_invoice, page_number):
    global invoice_number

    if page_number == 1:
        rows_per_page = num_rows_first_page
    else:
        rows_per_page = num_rows_subsequents_pages



    page: Page = Page()

    # set PageLayout
    page_layout: PageLayout = SingleColumnLayout(page,
                                                 vertical_margin=page.get_page_info().get_height() * Decimal(0.02))
    f = r'./vast.ai-logo.png'
    logo_img = PIL.Image.open(f)


    # add corporate logo

    now = datetime.datetime.now()
    table_logo_and_invoice_num = FixedColumnWidthTable(number_of_rows=5, number_of_columns=4)
    table_logo_and_invoice_num.add(
        TableCell(
            Image(
                logo_img,
                width=Decimal(72),
                height=Decimal(105),
            ), row_span=2)
    )
    table_logo_and_invoice_num.add(Paragraph("Page %d of %d" % (page_number, page_count), font="Helvetica", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph("Invoice", font="Helvetica", font_size=Decimal(50),
                                             horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph("# %d" % invoice_number, font="Helvetica",
                                             font_size=Decimal(20), horizontal_alignment=Alignment.RIGHT))
    blank_row(table_logo_and_invoice_num, 4, 3)

    table_logo_and_invoice_num.no_borders()
    page_layout.add(table_logo_and_invoice_num)

    if page_number == 1:
        # Invoice information table
        page_layout.add(build_2nd_block_table())

        # Empty paragraph for spacing
        page_layout.add(Paragraph(" "))

        # Billing and shipping information table
        page_layout.add(build_billto_table(user_blob))
        page_layout.add(Paragraph(" "))

    # rows_per_page = 10
    table_invoice_rows = build_invoice_charges_table(rows_invoice, rows_per_page)
    page_layout.add(table_invoice_rows)
    return page


def compute_pages_needed(rows_invoice):
    num_rows_invoice = len(rows_invoice)
    num_rows_invoice = num_rows_invoice - num_rows_first_page
    page_count: int = math.ceil(num_rows_invoice / num_rows_subsequents_pages) + 1
    return page_count



def generate_invoice(user_blob, rows_invoice):
    # create Document
    pdf: Document = Document()
    global page_count
    page_count = compute_pages_needed(rows_invoice)
    global invoice_total
    invoice_total = compute_column_sum(rows_invoice, "amount")
    page_number = 1
    while (len(rows_invoice) > 0):
        if page_number == 1:
            page = generate_invoice_page(user_blob, rows_invoice, page_number)
        else:
            # if len(rows_invoice) < num_rows_subsequents_pages:
            #     print("There are ", str(len(rows_invoice)), " rows left!")
            #     break
            page = generate_invoice_page(user_blob, rows_invoice, page_number)

        print("Adding page ", str(page_number))
        pdf.append_page(page)
        page_number += 1





    # page = generate_invoice_page(user_blob, rows_invoice, True)
    # pdf.append_page(page)
    # page = generate_invoice_page(user_blob, rows_invoice, False)
    # pdf.append_page(page)

    with open("borb_invoice_example.pdf", "wb") as out_file_handle:
        PDF.dumps(out_file_handle, pdf)


if __name__ == "__main__":
    main()
