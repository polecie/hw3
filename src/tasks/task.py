import datetime
import json

import pandas as pd

from .worker import celery


@celery.task
def save_menu(menus):
    menus = json.loads(menus)
    df = pd.DataFrame(columns=["A", "B", "C", "D", "E", "F"])
    for id, item in enumerate(menus, 1):
        df = df.append(
            {"A": id, "B": item["title"], "C": item["description"]},
            ignore_index=True,
        )
        for id_sub, sub_item in enumerate(item["submenus"], 1):
            df = df.append(
                {
                    "B": id_sub,
                    "C": sub_item["title"],
                    "D": sub_item["description"],
                },
                ignore_index=True,
            )
            for id_dishes, descript in enumerate(sub_item["dishes"], 1):
                df = df.append(
                    {
                        "C": id_dishes,
                        "D": descript["title"],
                        "E": descript["description"],
                        "F": descript["price"],
                    },
                    ignore_index=True,
                )
    date = datetime.datetime.utcnow()
    name = "menu" + "-" + str(date.date()) + "-" + str(date.time())
    df.to_excel(f"{name}.xlsx", header=False, index=False)
    return f"{name}.xlsx"
