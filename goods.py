class Item:

    attributes = {
        "acc_data": {"column": "ДатаСчФ", "width": 10},
        "acc_num": {"column": "НомерСчФ", "width": 15},
        "acc_org_name": {"column": "НаимЭконСубСост", "width": 50},
        "id_mark": {"column": "КИЗ", "width": 40},
        "row_num": {"column": "НомСтр", "width": 8},
        "name": {"column": "НаимТов", "width": 40},
        "price": {"column": "ЦенаТов", "width": 10},
        "amount": {"column": "КолТов", "width": 7}
    }

    columns = [{"header": v["column"]} for k, v in attributes.items()]

    xpath = {
        "acc_data": "//Файл/Документ/СвСчФакт/@ДатаСчФ",
        "acc_num": "//Файл/Документ/СвСчФакт/@НомерСчФ",
        "acc_org_name": "//Файл/Документ/@НаимЭконСубСост",
        "goods": "//Файл/Документ/ТаблСчФакт/СведТов",
        "row_num": "@НомСтр",
        "name": "@НаимТов",
        "price": "@ЦенаТов",
        "amount": "@КолТов",
        "id_mark": "ДопСведТов/НомСредИдентТов/КИЗ/text()"
    }

    def __init__(self,
                 acc_data,
                 acc_num,
                 acc_org_name,
                 row_num,
                 name,
                 price,
                 amount,
                 id_marks):

        self.acc_data = acc_data
        self.acc_num = acc_num
        self.acc_org_name = acc_org_name
        self.row_num = row_num
        self.name = name
        self.price = price
        self.amount = amount
        self.id_marks = id_marks

    def __str__(self):
        attrs = [str(self.__getattribute__(name)) for name in self.attributes.keys() if name != "id_mark"]
        attrs.append(str(self.id_marks))
        return ", ".join(attrs)

    def to_list(self):
        res = []
        attrs = []

        for k, v in self.attributes.items():
            if k != "id_mark":
                attrs.append(self.__getattribute__(k))
            else:
                attrs.append(k)

        if self.id_marks:
            for mark in self.id_marks:
                row = [el if el != "id_mark" else mark for el in attrs]
                res.append(row)
        else:
            row = [el if el != "id_mark" else "" for el in attrs]
            res.append(row)

        return res
