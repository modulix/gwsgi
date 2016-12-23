#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python script for GWSGI server
import sys
import os
import json
import logging
from jinja2 import Environment, PackageLoader
from couchdb import Server
from datetime import datetime

def index(environ):
    logger = logging.getLogger()
    logger.debug("database.index(%s)", environ)
    cdb = Server(url='http://couchdb.modulix.net/')["xpm"]
    # Getting eventual args
    try:
        m_year = environ["wsgi_query"]["m_year"]
    except:
        m_year = "all"
    menu_years = [{"value": "all", "txt": "All", "selected": False}]
    stat_glob = []
    stat_pie = []
    stat_month = [
        {"name":"Jan", "data":[0]*10},
        {"name":"Feb", "data":[0]*10},
        {"name":"Mar", "data":[0]*10},
        {"name":"Avr", "data":[0]*10},
        {"name":"May", "data":[0]*10},
        {"name":"Jun", "data":[0]*10},
        {"name":"Jul", "data":[0]*10},
        {"name":"Aug", "data":[0]*10},
        {"name":"Sep", "data":[0]*10},
        {"name":"Oct", "data":[0]*10},
        {"name":"Nov", "data":[0]*10},
        {"name":"Dec", "data":[0]*10},
        ]
    # List of all availables years (max 10)
    next_year = datetime.now().year + 1
    year_records = cdb.view("_design/block/_view/by_date", group=True, group_level=1, startkey=[1970], endkey=[next_year], limit=10)
    for year_rec in year_records:
        cur_year = year_rec.key[0]
        stat_glob.append({"year": cur_year, "data":[], "name":[]})
        menu_years.append({"value": str(cur_year), "txt": str(cur_year), "selected": False})
    # Setting selected item "year" in menu
    for item in menu_years:
        if item["value"] == m_year:
            item["selected"] = True
            break
    logger.debug("database.menu:%s:%s", m_year, menu_years)
    idx = 0
    if m_year == "all":
        # Getting stats by month for each year
        logger.debug("database.ALLYEARS")
        prev_month = 0
        for stat_glob_year in stat_glob:
            cur_year = stat_glob_year["year"]
            #print("YEAR:%d" % cur_year)
            if prev_month:
                stat_glob_year["data"] = [""] * prev_month
            records = cdb.view("_design/block/_view/by_date", group=True, group_level=2, startkey=[cur_year, 0], endkey=[cur_year+1, 0], limit=12)
            year_total = 0
            for rec in records:
                #logger.debug("database.record:%s", rec)
                prev_month += 1
                year_total += rec.value["count"]
                stat_glob_year["data"].append(rec.value["count"])
                stat_glob_year["name"].append("%s-%s" % (rec.key[0], rec.key[1]))
                stat_month[rec.key[1] - 1]["data"][idx] += rec.value["count"]
            stat_pie.append({"year": cur_year, "data": year_total})
            idx += 1
    else:
        logger.debug("database.ONEYEAR:%s", m_year)
        for stat_glob_year in stat_glob:
            cur_year = stat_glob_year["year"]
            if m_year == str(cur_year):
                records = cdb.view("_design/block/_view/by_date", group=True, group_level=3, startkey=[cur_year, 0, 0], endkey=[cur_year+1, 0, 0], limit=360)
                year_total = 0
                for rec in records:
                    #logger.debug("database.record:%s", rec)
                    year_total += rec.value["count"]
                    stat_glob_year["data"].append(rec.value["count"])
                    stat_glob_year["name"].append("%s-%s-%s" % (rec.key[0], rec.key[1], rec.key[2]))
                    stat_month[rec.key[1] - 1]["data"][0] += rec.value["count"]
                stat_pie.append({"year": cur_year, "data": year_total})
    # Creating a recaputilative record with all years
    recap = {"year": "all", "data":[], "name":[]}
    for stat_glob_year in stat_glob:
        for val in stat_glob_year["data"]:
            if val:
                recap["data"].append(val)
        for val in stat_glob_year["name"]:
            if val:
                recap["name"].append(val)
    stat_glob.append(recap)

    logger.debug("database.stat_glob:%s", stat_glob)
    logger.debug("database.stat_month:%s", stat_month)
    logger.debug("database.stat_pie:%s", stat_pie)

    tpl_env = Environment(loader=PackageLoader('example.database', 'template'))
    if os.path.isfile("example/template/stats.%s" % environ["wsgi_mime"]):
        template = tpl_env.get_template('stats.%s' % environ["wsgi_mime"])
        output = template.render(title="GWSGI:Database (couchdb) example", environ=environ, menu_years=menu_years, stats_glob=stat_glob, stat_month=stat_month, stat_pie=stat_pie)
    else:
        environ["wsgi_status"] = "404"
        environ["wsgi_header"] = [("Content-type", "text/plain")]
        output = "Sorry, the requested MIME type (%s) is not available..." % environ["wsgi_mime"]
    return([output.encode("utf-8")])

# To use directly from bash, you need to cd $HTTP_DIR and try:
# REQUEST_METHOD=GET wsgi_mime=txt ./example/database.py
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(index(os.environ))
