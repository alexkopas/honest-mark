import logging
from goods import Item
from typing import List
from lxml import etree
from pathlib import Path


logger = logging.getLogger(__name__)


class XMLParser:

    def __init__(self):
        self.xml_files: List[str] = []
        self.items: List[Item] = []

    def to_list(self) -> List[str]:
        res = []
        for i in self.items:
            res += i.to_list()
        return res

    def parse(self, xml_files: (Path, List[Path])) -> None:
        if isinstance(xml_files, Path):
            xml_files = [xml_files]

        self.xml_files = xml_files
        logger.debug(self.xml_files)

        for file in self.xml_files:
            items = self.parse_one(file)
            if items:
                self.items += items

    @staticmethod
    def parse_one(filename: Path) -> List[Item]:
        root = etree.parse(str(filename))
        # logger.debug(etree.tostring(root, pretty_print=True, encoding="UTF-8").decode())
        items = []

        acc_data = root.xpath(Item.xpath["acc_data"])[0]
        acc_num = root.xpath(Item.xpath["acc_num"])[0]
        acc_org_name = root.xpath(Item.xpath["acc_org_name"])[0]

        goods = root.xpath(Item.xpath["goods"])

        for good in goods:
            row_num = int(good.xpath(Item.xpath["row_num"])[0])
            name = good.xpath(Item.xpath["name"])[0]
            price = float(good.xpath(Item.xpath["price"])[0])
            amount = float(good.xpath(Item.xpath["amount"])[0])

            id_marks = good.xpath(Item.xpath["id_mark"])

            # if id_marks:
            item = Item(acc_data=acc_data,
                        acc_num=acc_num,
                        acc_org_name=acc_org_name,
                        row_num=row_num,
                        name=name,
                        price=price,
                        amount=amount,
                        id_marks=id_marks)

            items.append(item)
            logger.debug(str(item))

        return items




