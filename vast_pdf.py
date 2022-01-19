#!/usr/bin/env python3

# vast_pdf: Library of functions to create PDF reports of various type.
# Currently only makes invoices.
import argparse
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
num_rows_first_page: int = 15
num_rows_subsequents_pages: int = 25
invoice_total: float = 0
now = datetime.date.today()
invoice_number: int = now.year * 12 + now.month - 1
page_count: int = 0
no_table_borders = False
no_table_borders = True

# def Paragraph_wr(text: str, *args, **kwargs):
#     """This is just a wrapper for the Paragraph function that prevents the text from being the null string "".
#
#      :param str text: The text to be checked for null.
#      """
#     if text == "":
#         text = " "
#     return Paragraph(text, *args, **kwargs)


def build_2nd_block_table() -> FixedColumnWidthTable:
    """
    This function builds a Table containing invoice information.
    This information spans the page and is the second large block of
    text on the page.

    :return Table:    a Table containing invoice information
    """
    global invoice_total, now

    # now = datetime.datetime.now()
    table = FixedColumnWidthTable(number_of_rows=3, number_of_columns=3)

    table.add(Paragraph("Vast.ai Inc."))
    table.add(Paragraph("Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year), horizontal_alignment=Alignment.RIGHT))

    table.add(Paragraph("100 Van Ness Ave."))
    table.add(Paragraph("Payment Terms:", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph("Charged - Do Not Pay", horizontal_alignment=Alignment.RIGHT))

    table.add(Paragraph("San Francisco CA 94102"))

    table.add(
        Paragraph("Total", font="Helvetica-Bold", font_size=Decimal(20), horizontal_alignment=Alignment.RIGHT))
    table.add(Paragraph(format_float_val_as_currency(invoice_total), font="Helvetica-Bold", font_size=Decimal(20),
                        horizontal_alignment=Alignment.RIGHT))

    # table.add(Paragraph("fixme@vast.ai"))
    # table.add(Paragraph(" "))
    # table.add(Paragraph(" "))
    # table.add(Paragraph(" "))

    # table.add(Paragraph("https://vast.ai/"))
    # table.add(Paragraph(" "))
    # table.add(Paragraph(" "))
    # table.add(Paragraph(" "))

    table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    if no_table_borders: table.no_borders()
    return table


def blank_row(table: Table, col_num: int, row_num: int = 1) -> None:
    """Just a set of blank rows to act as filler.
    :param table: The table we want to modify
    :param int col_num: How many columns in the table?
    :param int row_num: How many blank rows do we need?
    """
    for j in range(row_num):
        for i in range(col_num):
            table.add(Paragraph(" "))


def field_and_filler(user_blob: typing.Dict, table: Table, fieldname: str):
    """Adds a field to the table along with a filler cell to span the table.

    :param str fieldname:
    :param Dict user_blob: A dict containing the user's info.
    :param Table table: The table to be modified.
    """
    table.add(Paragraph(str(user_blob[fieldname])))
    #table.add(Paragraph(" "))
    return


def build_billto_table(user_blob: dict) -> FixedColumnWidthTable:
    """
    This function builds a Table containing billing and shipping information
    It spans the page and uses blank cells to pad the right side of the page
    :param Dict user_blob: A dict containing the user's info.
    :return Table:    a Table containing shipping and billing information
    """
    table = FixedColumnWidthTable(number_of_rows=5, number_of_columns=1)
    table.add(Paragraph("BILL TO", font="Helvetica-Bold"))
    #table.add(Paragraph(" ", font="Helvetica-Bold"))

    field_ids = ["fullname", "billaddress_line1", "billaddress_line2"]
    list(map(lambda fieldname: field_and_filler(user_blob, table, fieldname), field_ids))

    table.add(Paragraph("%s, %s" % (user_blob["billaddress_city"], user_blob["billaddress_zip"])))  # BILLING
    #table.add(Paragraph(" "))  # SHIPPING
    #table.add(Paragraph(" "))  # BILLING
    #table.add(Paragraph(" "))  # SHIPPING
    table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    if no_table_borders: table.no_borders()
    return table


class Charge:
    """
    This class represents a charge line.
    """

    def __init__(self, name: str, quantity: float, rate: float, amount: float):
        self.name: str = name
        # assert quantity >= 0
        self.quantity: float = quantity
        # assert rate >= 0
        self.price_per_sku: float = rate
        # assert amount >= 0
        self.amount: float = amount


def format_float_val_as_currency(v):
    if v > 0:
        return "     -${:10.2f}".format(v)
    else:
        return "     ${:10.2f}".format(-v)



def build_charge_table(charges: typing.List[Charge], page_number: int) -> FlexibleColumnWidthTable:
    """
    This function builds a Table containing itemized billing information
    :param:     List charges: the rows on the invoice
    :param      int page_number: The page we are on
    :return:    a Table containing itemized billing information
    """
    global invoice_total
    num_rows = len(charges)
    table = FlexibleColumnWidthTable(number_of_rows=(num_rows + 3), number_of_columns=4)

    for h in ["Item", "Quantity", "Rate", "Amount"]:
        table.add(
            TableCell(
                Paragraph(h, font_color=X11Color("White")),  # vertical_alignment=Alignment.MIDDLE),
                background_color=HexColor("0b3954"), padding_top=Decimal(8), padding_bottom=Decimal(8)
            )
        )

    odd_color = HexColor("BBBBBB")
    even_color = HexColor("FFFFFF")
    for row_number, item in enumerate(charges):
        c = even_color if row_number % 2 == 0 else odd_color
        table.add(TableCell(Paragraph(item.name, font="Helvetica-Bold"), background_color=c))
        table.add(TableCell(Paragraph("     {:10.2f}".format(item.quantity),  # font="Helvetica-Bold",
                                      horizontal_alignment=Alignment.RIGHT), background_color=c))
        table.add(TableCell(Paragraph(format_float_val_as_currency(item.price_per_sku),  # font="Helvetica-Bold",
                                      horizontal_alignment=Alignment.RIGHT), background_color=c))
        table.add(
            TableCell(Paragraph(format_float_val_as_currency(item.amount),  # font="Helvetica-Bold",
                                horizontal_alignment=Alignment.RIGHT), background_color=c))

    if page_number == page_count:
        table.add(
            TableCell(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT, ), col_span=3, ))
        table.add(TableCell(Paragraph(" ", horizontal_alignment=Alignment.RIGHT)))

        table.add(
            TableCell(Paragraph("Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3, ))
        table.add(TableCell(Paragraph(format_float_val_as_currency(invoice_total), horizontal_alignment=Alignment.RIGHT)))
    else:
        blank_row(table, 4, 2)
    table.set_padding_on_all_cells(Decimal(2), Decimal(5), Decimal(2), Decimal(5))
    if no_table_borders: table.no_borders()
    return table


# def main():
#     print("Script called from command line - probably not what we want.")


def product_row(charges):
    """Makes a single row with charge information in it."""
    description = charges["description"] if "description" in charges else "Add Credit"
    amount = float(charges["amount"]) if "amount" in charges else 0.0
    quantity = float(charges["quantity"]) if "quantity" in charges else 1.0
    rate = float(charges["rate"]) if "rate" in charges else amount

    return Charge(description, quantity, rate, amount)


def product_rows(rows_invoice=None):
    """Makes a page worth of rows of charges."""
    if rows_invoice is None:
        rows_invoice = []
    return list(map(lambda charges: product_row(charges), rows_invoice))


def build_invoice_charges_table(rows_invoice: typing.List[typing.Dict],
                                charges_per_page: int, page_number: int) -> FlexibleColumnWidthTable:
    """This function creates a page of invoice charges and depletes
    the list of charges by the number it prints out.
    :param typing.List[typing.Dict] rows_invoice: List of rows in the invoice
    :param int charges_per_page: How many rows of charges we put on this page.
    """
    rows_invoice_chunk = rows_invoice[0:charges_per_page]
    # sums = {"amount": compute_column_sum(rows_invoice, "amount", True)}
    del rows_invoice[0:charges_per_page]
    return build_charge_table(product_rows(rows_invoice_chunk), page_number)


def compute_column_sum(rows_invoice: typing.List[typing.Dict],
                       column_name: str,
                       values_are_negative: bool = False) -> float:
    """Sum over one of the columns in the invoice.
    :rtype: float
    :param typing.List[typing.Dict] rows_invoice: List of rows in the invoice
    :param str column_name: Which column to sum over.
    :param bool values_are_negative: are we summing values that are actually negative?
    """
    s: float = 0
    for row in rows_invoice:
        v: float = math.floor(float(row[column_name]) * 100) / 100
        # v = round(float(row[column_name]) * 100) / 100
        if values_are_negative:
            s = s - v
        else:
            s = s + v
    return math.floor(s * 100) / 100
    # return round(s * 100) / 100


def generate_invoice_page(user_blob: typing.Dict,
                          rows_invoice: typing.List[typing.Dict],
                          page_number, date_header_text="") -> Page:
    """Makes a single page of the invoice.

    :param date_header_text:
    :param Dict user_blob: Dict of info about the user
    :param typing.List[typing.Dict] rows_invoice: List of rows in the invoice
    :param int page_number: The page number for this page.
    """
    global invoice_number

    if page_number == 1:
        rows_per_page = num_rows_first_page
    else:
        rows_per_page = num_rows_subsequents_pages

    page: Page = Page()

    # set PageLayout
    page_layout: PageLayout = SingleColumnLayout(page,
                                                 vertical_margin=page.get_page_info().get_height() * Decimal(0.02))
    table_logo_and_invoice_num = build_logo_and_invoice_num_table(page_number)
    page_layout.add(table_logo_and_invoice_num)

    page_layout.add(Paragraph(" "))


    if page_number == 1:
        # Invoice information table
        page_layout.add(build_2nd_block_table())

        # Empty paragraph for spacing
        page_layout.add(Paragraph(" "))

        # Billing and shipping information table
        page_layout.add(build_billto_table(user_blob))

    page_layout.add(Paragraph(date_header_text + " "))

    if len(rows_invoice) == 0:
        # If we don't handle this case the client crashes with no output.
        page_layout.add(Paragraph("NO DATA"))
    else:
        table_invoice_rows = build_invoice_charges_table(rows_invoice, rows_per_page, page_number)
        page_layout.add(table_invoice_rows)
    return page


def build_logo_and_invoice_num_table(page_number):
    f = r'./vast.ai-logo.png'
    logo_img = PIL.Image.open(f)
    # add corporate logo
    now = datetime.datetime.now()
    table_logo_and_invoice_num = FixedColumnWidthTable(number_of_rows=2, number_of_columns=4)
    table_logo_and_invoice_num.add(
        TableCell(
            Image(
                logo_img,
                width=Decimal(72),
                height=Decimal(105),
            ), row_span=2)
    )
    table_logo_and_invoice_num.add(
        Paragraph("Page %d of %d" % (page_number, page_count), font="Helvetica", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph("Invoice", font="Helvetica", font_size=Decimal(50),
                                             horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph("# %d" % invoice_number, font="Helvetica",
                                             font_size=Decimal(20), horizontal_alignment=Alignment.RIGHT))
    # blank_row(table_logo_and_invoice_num, 4, 3)
    if no_table_borders: table_logo_and_invoice_num.no_borders()
    return table_logo_and_invoice_num


def compute_pages_needed(rows_invoice: typing.List[typing.Dict]) -> int:
    """Simple function to work out how many pages we need so that the page_count can be filled in at the top of every
    page.
    :param typing.List[typing.Dict] rows_invoice: The list of dicts we use elsewhere.
    """
    num_rows_invoice = len(rows_invoice)
    num_rows_invoice = num_rows_invoice - num_rows_first_page
    page_count: int = math.ceil(num_rows_invoice / num_rows_subsequents_pages) + 1
    return page_count


def translate_null_strings_to_blanks(d: typing.Dict) -> typing.Dict:
    """Map over a dict and translate any null string values into ' '.
    Leave everthing else as is."""

    # Beware: locally defined function.
    def translate_nulls(s):
        if s == "":
            return " "
        return s

    new_d = {k: translate_nulls(v) for k, v in d.items()}
    return new_d


def generate_invoice(user_blob: typing.Dict, rows_invoice: typing.List[typing.Dict], filter_data: typing.Dict):
    """This is the main function in this file. It calls everything else
    and makes the invoice page by page.


    :param user_blob: info about the user
    :param typing.List[typing.Dict] rows_invoice: The list of dicts we use elsewhere.
    """

    # create Document
    pdf: Document = Document()
    global page_count
    page_count = compute_pages_needed(rows_invoice)
    global invoice_total
    invoice_total = compute_column_sum(rows_invoice, "amount")
    page_number = 1

    if len(rows_invoice) == 0:
        page = generate_invoice_page(user_blob, rows_invoice, page_number, filter_data["header_text"])
        print("Adding Empty page ", str(page_number))
        pdf.append_page(page)
    else:
        while len(rows_invoice) > 0:
            page = generate_invoice_page(user_blob, rows_invoice, page_number, filter_data["header_text"])
            print("Adding page ", str(page_number))
            pdf.append_page(page)
            page_number += 1

    with open("latest-invoice.pdf", "wb") as debug_file_handle:
        PDF.dumps(debug_file_handle, pdf)
    debug_file_handle.close()

    with open(filter_data["pdf_filename"], "wb") as users_file_handle:
        PDF.dumps(users_file_handle, pdf)
    users_file_handle.close()


if __name__ == "__main__":
    main()
