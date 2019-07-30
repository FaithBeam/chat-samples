from random import choice
from template import Template
import models.models


class Quotes(Template):
    def __init__(self):
        super().__init__(models.models.Quotes, models.models.QuotesSchema, ("quote",))
        self.data = self.get_all_data()

    def add_quote(self, quote: str) -> str:
        quote = quote.strip()
        if quote == "" or self.contains_quote(quote):
            return "Didn't add quote."
        else:
            self.data.append(quote)
            insert = self.table_schema.load({self.fieldnames[0]: quote}).data
            self.insert_record(insert)
            return f"Added quote at position #{len(self.data)}."

    def contains_quote(self, quote: str) -> bool:
        if quote in self.data:
            return True
        else:
            return False

    def edit_quote(self, number: int, quote: str) -> str:
        if self.exists_quote(number):
            before = self.data[number]
            set = {self.fieldnames[0]: quote}
            self.update_record(self.fieldnames[0], before, set)
            self.data[number] = quote
            return f"Edited quote #{number + 1}."
        else:
            return f"Didn't edit quote #{number + 1}."

    def exists_quote(self, number: int):
        if number < len(self.data):
            return True
        else:
            return False

    def delete_quote(self, number: str):
        number = int(number) - 1
        if len(self.data) > 0 and len(self.data) > int(number):
            self.delete_item(self.data[number])
            del self.data[number]
            return f"Deleted quote #{int(number) + 1}."
        else:
            return f"Didn't delete quote #{int(number) + 1}."

    def get_quote(self, number: int):
        if number == -1:
            return self.get_random_quote()
        elif number > -1 and self.exists_quote(number):
            return f"#{number + 1}/{len(self.data)}: {self.data[number]}"
        else:
            return "No."

    def get_number_quotes(self) -> str:
        return str(len(self.data))

    def get_random_quote(self) -> str:
        if len(self.data) > 0:
            quote = choice(self.data)
            pos = self.data.index(quote) + 1
            return f"#{pos}/{len(self.data)}: {quote}"
        else:
            return "No quotes."
