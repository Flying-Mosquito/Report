# -*- coding: utf-8 -*-
from FMosquito.protocol import localdata
from FMosquito.localdata import LDManager
from FMosquito.error import DBAccessError
import logging

def get_localdata(dbpool, locale):
	# localdata 에서 최신 data를 가져옴
	with dbpool.scoped_get_group("common", readonly=True) as db:
		rs = db.query("select version, country, localdata from localdata  where country=%s and mdate=(select MAX(mdate) from localedata where country=%s)", (locale, locale,))
	if not rs:
		raise DBAccessError("get_localedata not found error")

	for ld in rs:
		localedata_version, country, localedata = ld
	if country == locale:
		localedata_pb = localedata_pb2.LocaleData()
		localedata_pb.ParseFromString(localedata)
            
		LDManager.set_localedata_with_key(localedata_pb, (localedata_version, country)) 
		logging.notice("localedata load complete version: %s  country: %s", localedata_version, country)
		return (localedata_version, country) 
    
