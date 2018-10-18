import tabula as tb
df=tb.read_pdf('wcdl201712.pdf',encoding='GB18030',multiple_tables=True,pages='all',pandas_option={'header':0})
for ele in df:
    print(ele)
