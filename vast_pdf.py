#!/usr/bin/env python3

# vast_pdf: Library of functions to create PDF reports of various type.
# Currently only makes invoices.

import datetime
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

## Globals: Probably shouldn't use globals but this is fast.
template_gpu_charge = "Instance %d GPU charge: hours * $/hr"
template_storage_charge = "Instance %d storage charge: hours * $/hr"


def _build_invoice_information(invoice_total = 0) -> Table:
    """
    This function builds a Table containing invoice information
    :return:    a Table containing invoice information
    """
    now = datetime.datetime.now()
    table_001 = FixedColumnWidthTable(number_of_rows=5, number_of_columns=3)

    table_001.add(Paragraph("Vast.ai Inc."))
    table_001.add(Paragraph("Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year), horizontal_alignment=Alignment.RIGHT))

    table_001.add(Paragraph("100 Van Ness Ave."))
    table_001.add(Paragraph("Payment Terms:", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("Charged - Do Not Pay", horizontal_alignment=Alignment.RIGHT))

    table_001.add(Paragraph("San Francisco CA 94102"))

    table_001.add(Paragraph("Total", font="Helvetica-Bold", font_size=Decimal(20), horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph(f'-${invoice_total:.3f}', font="Helvetica-Bold", font_size=Decimal(20), horizontal_alignment=Alignment.RIGHT))

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
    for j in range(row_num):
        for i in range(col_num):
            table.add(Paragraph(" "))


def field_and_blank_line(user_blob, table, fieldname):
    table.add(Paragraph(str(user_blob[fieldname])))
    table.add(Paragraph(" "))


def maptest(fieldname):
    print(str(fieldname))


def _build_billing_and_shipping_information(user_blob) -> Table:
    """
    This function builds a Table containing billing and shipping information
    :return:    a Table containing shipping and billing information
    """
    table_001 = FixedColumnWidthTable(number_of_rows=6, number_of_columns=2)
    table_001.add(
        Paragraph(
            "BILL TO",
            font="Helvetica-Bold"
            # background_color=HexColor("263238"),
            # font_color=X11Color("White"),
        )
    )
    table_001.add(
        Paragraph(
            " ",
            font="Helvetica-Bold"
            # background_color=HexColor("263238"),
            # font_color=X11Color("White"),
        )
    )

    field_ids = ["fullname", "billaddress_line1", "billaddress_line2"]
    # , "billaddress_line1", "billaddress_line2",
    #          "billaddress_city", "billaddress_zip", "billaddress_country"]
    # time.sleep(5)
    # print(list(map(lambda fieldname: maptest(fieldname), field_ids)))
    # time.sleep(5)
    print(list(map(lambda fieldname: field_and_blank_line(user_blob, table_001, fieldname), field_ids)))

    print("USER_BLOB: ", user_blob)
    # table_001.add(Paragraph(str(user_blob["fullname"])))  # BILLING
    # table_001.add(Paragraph(" "))  # SHIPPING
    # table_001.add(Paragraph("[Company Name]"))  # BILLING
    # table_001.add(Paragraph(" "))  # SHIPPING
    # table_001.add(Paragraph(user_blob["billaddress_line1"]))  # BILLING

    # if user_blob["billaddress_line2"]:
    #     table_001.add(Paragraph(user_blob["billaddress_line2"]))  # BILLING

    # table_001.add(Paragraph(" "))  # SHIPPING
    table_001.add(Paragraph("%s, %s" % (user_blob["billaddress_city"], user_blob["billaddress_zip"])))  # BILLING
    table_001.add(Paragraph(" "))  # SHIPPING
    # table_001.add(Paragraph("[Phone]"))  # BILLING
    table_001.add(Paragraph(" "))  # BILLING
    table_001.add(Paragraph(" "))  # SHIPPING
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))

    table_001.no_borders()
    return table_001


class Product:
    """
    This class represents a purchased product
    """

    def __init__(self, name: str, quantity: int, price_per_sku: float, amount: float):
        self.name: str = name
        assert quantity >= 0
        self.quantity: int = quantity
        assert price_per_sku >= 0
        self.price_per_sku: float = price_per_sku
        assert amount >= 0
        self.amount: float = amount


def _build_itemized_description_table(products: typing.List[Product] = [],
                                      sums={"quantity": 0, "rate": 0, "amount": 0}):
    """
    This function builds a Table containing itemized billing information
    :param:     products
    :return:    a Table containing itemized billing information
    """
    table_001 = FlexibleColumnWidthTable(number_of_rows=13, number_of_columns=4)

    for h in ["Item", "Quantity", "Rate", "Amount"]:
        table_001.add(
            TableCell(
                Paragraph(h, font_color=X11Color("White")),  # vertical_alignment=Alignment.MIDDLE),
                background_color=HexColor("0b3954"), padding_top=Decimal(8), padding_bottom=Decimal(8)
            )
        )
    # products = products[0]
    # FIXME: ^^^ no idea why this is necessary. The products list somehow becomes
    # FIXME: the first element in another outer list when passed into this function.
    # FIXME: I tried taking the typing information out but it still does this.

    odd_color = HexColor("BBBBBB")
    even_color = HexColor("FFFFFF")
    for row_number, item in enumerate(products):
        c = even_color if row_number % 2 == 0 else odd_color
        table_001.add(TableCell(Paragraph(item.name, font="Helvetica-Bold"), background_color=c))
        table_001.add(TableCell(Paragraph("     {:10.3f}".format(item.quantity),  # font="Helvetica-Bold",
                                          horizontal_alignment=Alignment.RIGHT), background_color=c))
        table_001.add(TableCell(Paragraph("     -${:10.3f}".format(item.price_per_sku),  # font="Helvetica-Bold",
                                          horizontal_alignment=Alignment.RIGHT), background_color=c))
        table_001.add(
            TableCell(Paragraph("-${:10.3f}".format(item.amount),  # font="Helvetica-Bold",
                                horizontal_alignment=Alignment.RIGHT), background_color=c))

    # Optionally add some empty rows to have a fixed number of rows for styling purposes
    for row_number in range(len(products), 10):
        c = even_color if row_number % 2 == 0 else odd_color
        for _ in range(0, 4):
            table_001.add(TableCell(Paragraph(" "), background_color=c))

    # subtotal
    subtotal: float = sum([x.price_per_sku * x.quantity for x in products])
    table_001.add(
        TableCell(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT, ), col_span=3, ))
    table_001.add(TableCell(Paragraph(" ", horizontal_alignment=Alignment.RIGHT)))

    # discounts
    # table_001.add(
    #     TableCell(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT, ), col_span=3, ))
    # table_001.add(TableCell(Paragraph(" ", horizontal_alignment=Alignment.RIGHT)))

    # taxes
    taxes: float = subtotal * 0.06
    # table_001.add(
    #    TableCell(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3, ))
    # table_001.add(TableCell(Paragraph(" ", horizontal_alignment=Alignment.RIGHT)))

    # total
    total: float = subtotal

    table_001.add(
        TableCell(Paragraph("Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3, ))
    table_001.add(TableCell(Paragraph("-${:10.3f}".format(-sums["amount"]), horizontal_alignment=Alignment.RIGHT)))
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(5), Decimal(2), Decimal(5))
    table_001.no_borders()
    return table_001


def main():
    print("Script called from command line - probably not what we want.")


def make_random_instance_charge(products: typing.List[Product] = []):
    random_instance_id = random.randint(2125000, 2126000)
    random_quantity_gpu = random.random() * 10
    random_rate_gpu = random.random() * -0.5
    random_quantity_storage = random.random() * 10
    random_rate_storage = random.random() * -0.5

    products.append(Product(template_gpu_charge % random_instance_id, random_quantity_gpu, random_rate_gpu))
    products.append(Product(template_storage_charge % random_instance_id, random_quantity_storage, random_rate_storage))


def product_row(charges):
    return Product(charges["description"], float(charges["quantity"]), float(charges["rate"]),
                   float(charges["amount"]))


def product_rows(rows_invoice=None):
    if rows_invoice is None:
        rows_invoice = []
    return list(map(lambda charges: product_row(charges), rows_invoice))


def build_invoice_charges_table(rows_invoice, max_rows=5):
    rows_invoice_chunk = rows_invoice[0:max_rows]
    sums = {"amount" : compute_column_sum(rows_invoice, "amount", True)}
    del rows_invoice[0:max_rows]
    return _build_itemized_description_table(product_rows(rows_invoice_chunk), sums)


def random_instance_charges(n):
    products = []
    for x in range(n):
        make_random_instance_charge(products)

    return _build_itemized_description_table([
        products
        # Product("Labor", 14, 60)
    ])


# def random_instance_charges_old():
#     random_instance_id = random.randint(2125000, 2126000)
#     random_quantity_gpu = random.random() * 10
#     random_rate_gpu = random.random() * -0.5
#     random_quantity_storage = random.random() * 10
#     random_rate_storage = random.random() * -0.5
#     return _build_itemized_description_table([
#         Product(template_gpu_charge % random_instance_id, random_quantity_gpu, random_rate_gpu),
#         Product(template_storage_charge % random_instance_id, random_quantity_storage, random_rate_storage),
#         # Product("Labor", 14, 60)
#     ])

def compute_column_sum(rows_invoice, column_name, values_are_negative=False):
    s = 0
    for row in rows_invoice:
        if values_are_negative:
            s = s - float(row[column_name])
        else:
            s = s + float(row[column_name])
    return s


def generate_invoice(user_blob, rows_invoice):
    # create Document
    pdf: Document = Document()

    # add Page
    page: Page = Page()
    pdf.append_page(page)

    # set PageLayout
    page_layout: PageLayout = SingleColumnLayout(page,
                                                 vertical_margin=page.get_page_info().get_height() * Decimal(0.02))
    f = r'./vast.ai-logo.png'
    logo_img = PIL.Image.open(f)

    invoice_total = compute_column_sum(rows_invoice, "amount")
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
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph("Invoice", font="Helvetica", font_size=Decimal(50),
                                             horizontal_alignment=Alignment.RIGHT))
    # table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(Paragraph(" ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.add(
        Paragraph("# %d" % random.randint(1000, 10000), font="Helvetica", font_size=Decimal(20),
                  horizontal_alignment=Alignment.RIGHT))
    blank_row(table_logo_and_invoice_num, 4, 3)
    #
    # table_logo_and_invoice_num.add(Paragraph("Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    # table_logo_and_invoice_num.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year), horizontal_alignment=Alignment.RIGHT))
    table_logo_and_invoice_num.no_borders()
    page_layout.add(table_logo_and_invoice_num)

    # Invoice information table
    page_layout.add(_build_invoice_information(invoice_total))

    # Empty paragraph for spacing
    page_layout.add(Paragraph(" "))

    # Billing and shipping information table
    page_layout.add(_build_billing_and_shipping_information(user_blob))

    # Empty paragraph for spacing
    page_layout.add(Paragraph(" "))

    # template_gpu_charge = "Instance %d GPU charge: hours * $/hr"
    # random_instance_id = random.randint(2125000, 2126000)
    # random_quantity_gpu = random.random() * 10
    # random_rate_gpu = random.random() * 0.5
    # random_quantity_storage = random.random() * 10
    # random_rate_storage = random.random() * 0.5

    # invoices = user_blob["invoices"]
    # Itemized description
    max_rows = 8
    table_invoice_rows = build_invoice_charges_table(rows_invoice, max_rows)
    #    page_layout.add(random_instance_charges(4))

    page_layout.add(table_invoice_rows)

    # store
    with open("borb_invoice_example.pdf", "wb") as out_file_handle:
        PDF.dumps(out_file_handle, pdf)


if __name__ == "__main__":
    main()
