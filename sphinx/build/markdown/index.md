<!-- Vast.ai documentation master file, created by
sphinx-quickstart on Thu Jan 20 12:32:40 2022.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->
# Welcome to Vast.ai’s documentation!

# Indices and tables


* [Index](genindex.md)


* [Module Index](py-modindex.md)


* [Search Page](search.md)

# Modules

## vast


### vast.apiurl(args: argparse.Namespace, subpath: str, query_args: Dict[KT, VT] = None)
Creates the endpoint URL for a given combination of parameters.


* **Parameters**

    
    * **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – Namespace with many fields relevant to the endpoint.


    * **subpath** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – added to end of URL to further specify endpoint.


    * **query_args** ([*typing.Dict*](https://docs.python.org/3/library/typing.html#typing.Dict)) – specifics such as API key and search parameters that complete the URL.



* **Rtype str**



### vast.change__bid(args: argparse.Namespace)
Alter the bid with id contained in args.


* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Rtype int**



### vast.create__instance(args: argparse.Namespace)
Performs the same action as pressing the “RENT” button on the website at [https://vast.ai/console/create/](https://vast.ai/console/create/).


* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – Namespace with many fields relevant to the endpoint.



### vast.deindent(message: str)
deindent a quoted string. Scans message and finds the smallest number of whitespace characters in any line and
removes that many from the start of every line.


* **Parameters**

    **message** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Message to deindent.



* **Rtype str**



### vast.destroy__instance(args)
Perfoms the same action as pressing the “DESTROY” button on the website at [https://vast.ai/console/instances/](https://vast.ai/console/instances/).


* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



### vast.display_table(rows: list, fields: Tuple)
Basically takes a set of field names and rows containing the corresponding data and prints a nice tidy table
of it.


* **Parameters**

    
    * **rows** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) – Each row is a dict with keys corresponding to the field names (first element) in the fields tuple.


    * **fields** (*Tuple*) – 5-tuple describing a field. First element is field name, second is human readable version, third is format string, fourth is a lambda function run on the data in that field, fifth is a bool determining text justification. True = left justify, False = right justify. Here is an example showing the tuples in action.



* **Rtype None**


(“cpu_ram”, “RAM”, “{:0.1f}”, lambda x: x / 1000, False)


### vast.filter_invoice_items(args: argparse.Namespace, rows: List[T])
This applies various filters to the invoice items. Currently it filters on start and end date and applies the
‘only_charge’ and ‘only_credits’ options.


* **Parameters**

    
    * **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options


    * **rows** (*List*) – The rows of items in the invoice



* **Rtype List**

    Returns the filtered list of rows.



### vast.generate__pdf_invoices(args)
Makes a PDF version of the data returned by the “show invoices” command. Takes the same command line args as that
command.


* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.label__instance(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.list__machine(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.parse_query(query_str: str, res: Dict[KT, VT] = None)
Basically takes a query string (like the ones in the examples of commands for the search__offers function) and
processes it into a dict of URL parameters to be sent to the server.


* **Parameters**

    
    * **query_str** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – 


    * **res** (*Dict*) – 



* **Return Dict**



### vast.remove__defjob(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.scp_url(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.search__offers(args)
Creates a query based on search parameters as in the examples above.


* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



### vast.set__api_key(args)
Caution: a bad API key will make it impossible to connect to the servers.


* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



### vast.set__defjob(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.set__min_bid(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.set_ask(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.show__instances(args)
Shows the stats on the machine the user is renting.
:param argparse.Namespace args: should supply all the command-line options


### vast.show__invoices(args)
Show current payments and charges. Various options available to limit time range and type
of items. Default is to show everything for user’s entire billing history.


* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.show__machines(args)
Show the machines user is offering for rent.
:param argparse.Namespace args: should supply all the command-line options


### vast.show__user(args)
Shows stats for logged-in user. Does not show API key.


* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.ssh_url(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.start__instance(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.stop__instance(args)

* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.unlist__machine(args)
Removes machine from list of machines for rent.


* **Parameters**

    **args** ([*argparse.Namespace*](https://docs.python.org/3/library/argparse.html#argparse.Namespace)) – should supply all the command-line options



* **Return type**

    


### vast.version_string_sort(a, b)
Accepts two version strings and decides whether a > b, a == b, or a < b.
This is meant as a sort function to be used for the driver versions in which only
the == operator currently works correctly. Not quite finished…


* **Parameters**

    
    * **a** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – 


    * **b** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – 



* **Return int**


## vast_pdf


### _class_ vast_pdf.Charge(name: str, quantity: float, rate: float, amount: float, type: str, last4: str, timestamp: float)
This class represents a charge line.


### vast_pdf.blank_row(table: borb.pdf.canvas.layout.table.table.Table, col_num: int, row_num: int = 1)
Just a set of blank rows to act as filler.


* **Parameters**

    
    * **table** – The table we want to modify


    * **col_num** ([*int*](https://docs.python.org/3/library/functions.html#int)) – How many columns in the table?


    * **row_num** ([*int*](https://docs.python.org/3/library/functions.html#int)) – How many blank rows do we need?



* **Rtype None**



### vast_pdf.build_2nd_block_table()
This function creates a Table containing invoice information.
This information spans the page and is the second large block of
text on the page.


* **Rtype FixedColumnWidthTable**

    a Table containing information such as the company address, payment terms, date, and sum of charge_fields/payments.



### vast_pdf.build_billto_table(user_blob: dict)
This function builds a Table containing billing and shipping information
It spans the page using a single wide column.


* **Parameters**

    **user_blob** (*Dict*) – A dict containing the user’s info.



* **Rtype Table**

    a Table containing shipping and billing information



### vast_pdf.build_charge_table(charges: List[vast_pdf.Charge], page_number: int)
This function builds a Table containing itemized billing information


* **Parameters**

    
    * **charges** ([*typing.List*](https://docs.python.org/3/library/typing.html#typing.List)*[**Charge**]*) – the rows on the invoice


    * **page_number** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Current page number.



* **Rtype FlexibleColumnWidthTable**

    Borb Table containing the information.



### vast_pdf.build_invoice_charges_table(rows_invoice: List[Dict[KT, VT]], charges_per_page: int, page_number: int)
This function creates a page of invoice charge_fields and depletes the list of charge_fields by the number it
prints out. Essentially a pop function that removes multiple items at once.


* **Parameters**

    
    * **page_number** ([*int*](https://docs.python.org/3/library/functions.html#int)) – 


    * **rows_invoice** ([*typing.List*](https://docs.python.org/3/library/typing.html#typing.List)*[*[*typing.Dict*](https://docs.python.org/3/library/typing.html#typing.Dict)*]*) – List of rows in the invoice


    * **charges_per_page** ([*int*](https://docs.python.org/3/library/functions.html#int)) – How many rows of charge_fields we put on this page.



* **Rtype FlexibleColumnWidthTable**



### vast_pdf.build_logo_and_invoice_num_table(page_number)
At the top of every page is a table with our logo, the invoice number, and little text reading “page X of Y”.
This function creates that table and returns it.


* **Parameters**

    **page_number** – 



* **Rtype FixedColumnWidthTable**



### vast_pdf.compute_column_sum(rows_invoice: List[Dict[KT, VT]], column_name: str, values_are_negative: bool = False)
Sum over one of the columns in the invoice.


* **Parameters**

    
    * **rows_invoice** ([*typing.List*](https://docs.python.org/3/library/typing.html#typing.List)*[*[*typing.Dict*](https://docs.python.org/3/library/typing.html#typing.Dict)*]*) – List of rows in the invoice


    * **column_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of column to sum over.


    * **values_are_negative** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – are we summing values that are actually negative?



* **Return type**

    [float](https://docs.python.org/3/library/functions.html#float)



### vast_pdf.compute_pages_needed(rows_invoice: List[Dict[KT, VT]])
Function to work out how many pages we need so that the page_count can be filled in at the top of every page.


* **Parameters**

    **rows_invoice** ([*typing.List*](https://docs.python.org/3/library/typing.html#typing.List)*[*[*typing.Dict*](https://docs.python.org/3/library/typing.html#typing.Dict)*]*) – The list of dicts we use elsewhere.



* **Rtype int**



### vast_pdf.field_and_filler(user_blob: Dict[KT, VT], table: borb.pdf.canvas.layout.table.table.Table, fieldname: str)
Adds a field to the table along with a filler cell to span the table.


* **Parameters**

    
    * **fieldname** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – 


    * **user_blob** (*Dict*) – A dict containing the user’s info.


    * **table** (*Table*) – The table to be modified.



* **Rtype None**



### vast_pdf.format_float_val_as_currency(v)
Given a float value, format it as currency. Note that the sign is backwards due to the fact that the charge_fields in
the data that comes back are positive numbers but are written as negative on the invoice. There’s also the fact
that in our format string, if the value is actually negative it will print as “$-x.xx” instead of the correct
“-$x.xx”. I don’t know if this can be fixed with format strings so we rely on this hack.


* **Parameters**

    **v** ([*float*](https://docs.python.org/3/library/functions.html#float)) – 



* **Rtype str**



### vast_pdf.generate_invoice(user_blob: Dict[KT, VT], rows_invoice: List[Dict[KT, VT]], filter_data: Dict[KT, VT])
This is the main function in this library. It calls everything else and makes the invoice page by page. The
resulting invoice is written as a single PDF file.


* **Parameters**

    
    * **filter_data** – Parameters for client side filter.


    * **user_blob** – info about the user


    * **rows_invoice** ([*typing.List*](https://docs.python.org/3/library/typing.html#typing.List)*[*[*typing.Dict*](https://docs.python.org/3/library/typing.html#typing.Dict)*]*) – The list of dicts we use elsewhere.



* **Rtype None**



### vast_pdf.generate_invoice_page(user_blob: Dict[KT, VT], rows_invoice: List[Dict[KT, VT]], page_number: int, date_header_text: str = '')
Makes a single page of the invoice.


* **Parameters**

    
    * **date_header_text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – 


    * **user_blob** (*Dict*) – Dict of info about the user


    * **rows_invoice** ([*typing.List*](https://docs.python.org/3/library/typing.html#typing.List)*[*[*typing.Dict*](https://docs.python.org/3/library/typing.html#typing.Dict)*]*) – List of rows in the invoice


    * **page_number** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The page number for this page.



* **Rtype Page**



### vast_pdf.product_row(charge_fields)
Makes a single row with charge information in it.


* **Parameters**

    **charge_fields** – 



* **Rtype Charge**



### vast_pdf.product_rows(rows_invoice)
Maps a list of invoice dicts to a list of Charge objects using product_row function.


* **Parameters**

    **rows_invoice** – 



* **Rtype typing.List[Charge]**



### vast_pdf.translate_null_strings_to_blanks(d: Dict[KT, VT])
Map over a dict and translate any null string values into ‘ ‘.
Leave everything else as is. This is needed because you cannot add TableCell
objects with only a null string or the client crashes.


* **Parameters**

    **d** (*Dict*) – dict of item values.



* **Rtype Dict**
