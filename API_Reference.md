# API Document

### You will need to change the variables (start with "$") in the request body

- [Find nearby facilities](#find-nearby-facilities)
- [Get appointments](#get-appointments)
- [Find closest appointment](#find-closest-appointment)
- [Book appointment](#book-appointment)
- [Get appointment detail-1](#get-appointment-detail-1)
- [Get appointment detail-2](#get-appointment-detail-2)
- [Cancel appointment](#cancel-appointment)
- [Cancel reasons](#cancel-reasons)

## Find nearby facilities
```
curl --location 'https://tools.usps.com/UspsToolsRestServices/rest/v2/facilityScheduleSearch' \
--header 'Accept: application/json, text/javascript, */*; q=0.01' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'x-requested-with: XMLHttpRequest' \
--header 'sec-ch-ua-mobile: ?0' \
--header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
--data '{
    "city": "",
    "date": "$DATE", // 20230503
    "zip5": "$ZIP_CODE", // 94301
    "numberOfAdults": "1",
    "numberOfMinors": "0",
    "poScheduleType": "PASSPORT",
    "radius": "20",
    "state": ""
}'
```

## Get appointments
You can get appointments from specific facility on specific date
```
curl --location 'https://tools.usps.com/UspsToolsRestServices/rest/v2/appointmentTimeSearch' \
--header 'Accept: application/json, text/javascript, */*; q=0.01' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'x-requested-with: XMLHttpRequest' \
--header 'sec-ch-ua-mobile: ?0' \
--header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
--data '{
    "date":"$DATE", // 20230523
    "productType":"PASSPORT",
    "numberOfAdults":"1",
    "numberOfMinors":"0",
    "excludedConfirmationNumber":[""],
    "fdbId":["$FACILITY_ID"], // 1380637
    "skipEndOfDayRecord":true
}'
```

## Find closest appointment
You can find cloest appointment from specific facility (*not used in the script*)
```
curl --location 'https://tools.usps.com/UspsToolsRestServices/rest/v2/appointmentDateSearch' \
--header 'Accept: application/json, text/javascript, */*; q=0.01' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'x-requested-with: XMLHttpRequest' \
--header 'sec-ch-ua-mobile: ?0' \
--header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
--data '{
    "numberOfAdults":"1",
    "numberOfMinors":"0",
    "fdbId":"$FACILITY_ID", // 1380637
    "productType":"PASSPORT"
}'
```

## Book appointment
You will need to provide name, email and phone number
```
curl --location 'https://tools.usps.com/UspsToolsRestServices/rest/v2/createAppointment' \
--header 'authority: tools.usps.com' \
--header 'accept: application/json, text/javascript, */*; q=0.01' \
--header 'accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7' \
--header 'content-type: application/json;charset=UTF-8' \
--header 'origin: https://tools.usps.com' \
--header 'referer: https://tools.usps.com/rcas.htm' \
--header 'sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"' \
--header 'sec-ch-ua-mobile: ?0' \
--header 'sec-ch-ua-platform: "macOS"' \
--header 'sec-fetch-dest: empty' \
--header 'sec-fetch-mode: cors' \
--header 'sec-fetch-site: same-origin' \
--header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
--header 'x-jfuguzwb-a: rj4p8c433hs6oPt5nTxU6cVzceq0g8Yoj5wX=bB=jv0S3yZgL7PkdZOOhEPWNS_L8nBZI6=Ija=1pq786jv1D0tolDnPO8mAmjBCI_DpjTMKH7dG_KE=v6TDa2nt5eAStcRy4wWw8jlPYNOvRRlGfTls-E21PehAnQanUxOLpWLWj__IThKEAhS_t6RgZmGla4KkGuu8Eu36PQ6YMyMlAAgXyeAdY3pTjf7dCIds8zG5BrcOCoKfIo8GbaM=62t396hkh0LLXmPCTGlIqK=4JWCRFh1Fh6515l4QKojzjwUPfq=Ay=RucglLf7QCH8VplXXhuQI1jdvC5pU25dTYrNqIXSN7w1jbcGwGLJ5TPMEuKtKoJL1RWhODqokLYe7j1=1F5TkAX=qRVw1KsRzo9BpwQ_cpl8K0vq6aqs9kN-IBokFINH4VTKswfXMUxWZWkpqF=1sI7=8IkV3gKwGscskNN8Z0lCXPhk_qftXVE7QkuESIyjQw969hNxVXkGqvfgFqsq3DaVIhgNnpq8Rrj8FgAgwog6_yq2I8btU1dOJx7zXN3AA9IkgU2VtClaV9CkoPtRh1HFzj_Ldp6X6m8A8DJCPSvGqRvuxFcQ0_4wrR1PWwOm8Qw4R9ghR69dgnhgCzN8j3NNfjda0VXV2RqOsArQuDx515YG4U38mr4I2Ha735YtUxx3=mhAzGCjyp1nsrxKckEP1YQxUovczqs3dkGUVu9RTotlZ1gL-lnUDjXc3jxve3o_s=Fxo_kJpG3_PwPGembmRy0HONf7ZmpmJEAvg9bWFrjtao_aAXQPuvuBaU81LOT4G-=mmD-7G3EY0wFzHS1R1EoPcC7xWd-zTfzJnl8qbq--Zv3DsYKWqKnZt3D4-UzJLFy4lgXC3DCjQmsn=NHlcL7Q5kphaxhwkC5ySx3SRB_RpXX882PMGQOVKtVtCHXCKNV2I33RuoQRorOLPuVT_619pQFPKcyFRGcAM7dkXazYfuczPT5EQBGyQ9jg0mKuQfIGe-AEy-7BXMF0TxDf1ZfwjaSUOQHyGY0rX88rgc3MaKULZzBX7AoavIxCLFe_oqec6-svEEwjPcnF5=GWIk30Y5JulDt-jttJvCR6P3k2DnJQRAU9_a863WELZ8OT6DmoM6LrPjlR1cnclEvdS_qr=gb37TN8TIcda1Hx_cLcRCDbHHCF11lMM_7ZuJYZo6=SsbT5fwv71G3VgFz_SsJ5GSNeJQUoqd_MR4ZleJLdQHJ-gwb1Im_b8tSZMYO5fS6ylztbLoWTYcEqow9YSkpVMAB6M_p=rL1za0efZKQwzwRemHpCugmFhT22paITCghJv9tqyT1PDYjPx8bE0v-CjRyMj8CWs8svwB4vF46nzGHMmHSW_9D7CsXKYy6U-=c2Vj2OxljlZIaoFYx4kE9Ka8kZOS3Q5IgZg=aR1MMgwWWaLLfIoeFcuntwOk89rEacXKxYoxZYdphVBJ69XH5cxSfd8M8d1=dyJ787Xze-=ORSClZWDyhz6H2QpVeuNHISQJGWntV40JwhqC6W8lhJwxXVoIB442vae54smBl120VNFMcvzTpW4lztR1Ks-vmfZUyO3WOJ7-2_8trr1n=54PkmO0ucmtoDNWbFvAoHmZs-tyDanU-UwsVhlennt8ffjo6dHybhZPedbyW=z28mv9k25fVvJ=aqzbKF=IKb20EHNpbkZavelrMBb9chZBQ8FtlTnASUxop=7G7CD0yGv0=uVu2ThsnS9LYQDzUnqySkWxbv=DFtPLT4XjsD6doII0=KU1v6uFBjWz194Y8ynGyUGqPEaFWO_GRf_Veg4QY5ntnaIGJMnIwMX-1wsUbm2uXpjPT1VeMAPrg2nk68j0hTp9UWubK6AA7BgOTs5JSumj1-ayhvNs6Wb_N-KwNBeYjHtqeqvqojUAC-Qfy7xa0L-gS5Njg5Am5S=PMxYAv2JS28XKL4UWeWbkWS-=CnIBCyDUZZeVDEhpmEKW8DaHIRBbp2HRsPnpqhMN7OlQkkJVob52spXcGWSBwkx0Uzu8mzO6lhALHgqK3C3qE6cUDnNN6Fab=xf_HYUB04a5rbeFhgJyshycv_ID3DYTrCRh7sPKD65gF=F=0xHSYcracL6DH26s-kb9wMbtuMxaLDPF=Z_cxmAAlj20UTQZ1Yv=J90TNs4wnhzh5a1DDXK0aJprDYXykO=e5yeeuD4qSb70t9BJ=HdzdZXbGL=KvCAmdrA6f6UcTXkFIAFam3K0KdEc9r3Y4xe-ZxOl4n5N5MXsqeWSWIkrhJXCbw5RTt0lyQ9JhcOGPS4L3VWWWE7v=_S8ykRMdH9hjHOR7tc7cWKyuqLJZ61l1X=U7gn1f65nhX_jRGR5mwTI5WT1akVhs9sblWoyHsYqdbUjryXq2KRmxh19djMMjPvOG05Fr-RFPYBjNtkOAH3=Hrb8B-s5KKue28hWP54KkhIYTmk2Erf7zlvIUxwM5g6_5tGg31jmAAVLmX-zC4WszqqNbbOMRbCwEeUs0d6u5vRAJ6qL9cSM18zZXyYmxb5z1Wo43bcM7M6UWCp_QN3qTBzrnNfM23I7TAyqQJcnMrfQhbhQs8r_CUIHpCnIKJP-_bKwTITL1Ry_wvdqGrfOnevEKJrGlARBfVDq9xHWYp=b=XEoq6OH4hpfrEnFFMzhxsAyZ1_eam9VEU9GrhD2OxoK4YXGS6uHQCDhJzRmpAstt7MkY1KK_4k8UTM4TIZRf-tGSg-fApos8yMN4E5MZbYehfUVEqEmnU5N2gF3rNwhzxF=dRqohmFLzNtRbm49wkWCPDLHbGFXTK4Kma4TSEuHKWBFmn7GMYjy_rZYDloApNVncCxblnOJxtKyvA2PIpEhfaZdNBJ48ZjPKhjFw89ktWEndb3DwIOfrXQlxR9U6yuSTG8u035C9vY7CvNdePnt0I8jd2oLIV-_bMoP2uERN=6m0kYyeg2yn2BueNVvIexTAWT6TUW=fX2QdWCboq_8kS_RWpSD56=39KEXF5kzd9cX4n1enMKrlQnoWRRa9XZuWnVLDnrLR45MIc43u0GA2dOzpWX-lZaYltDtlmuqNHneCl0PbWckNsHmRcHlfjbInGfdRb5qJ9WEeUhn_RlnSW9skaEwtRbb4Rc_vMVgFNB6xw=rF097Jo61STHgTPYoz598fXktKAzJCoK8glp=-EJfUxOM5pJrFhXsxhW-pacRlg71_A9Mm-0VzOWWDzr5SMbUZa99KxWSFlUhb9mYtaenOIFVYH48vAyH7R=G3GfbzL8xtmpMutctawf3o5OOXhIPgB=HoLmQvTjn5OTrjjuW-GLn=WfVkQYXS0LJ8XdT0XbGFu4Nbn4HJBGwc=3k=3khJm=v0yyCHBNF0R0ynogYYN_aCCol7hSUz9JHjOT0sJT3XC5MfIUDQksbQX_5ZxaVPY6dDgyVM8RlxGLpzXWNLFFvoETU465Ad0ff=AqWrgEWjv4GLn2jo1WgDLTOo9RRqtmFfFl9uF73h9jnLgF_Hs-0wv_YdqVfIHsste1X9KlT-Rc4BBMUPExF8TyLlM9qaN-3lBjxbU88M-pWfTkp3Qjd4I72GXaUZpEsC5IRqgFWQXtwqx35etK7wT4OGhJGXLk5lWPX6La=QQ8uoH484tnEBgc41Fp7TWaht19cIxnhQx5leK_2tWsUeYPy=Rn1G60awY7AXCyop-4t7Ok9VJJx35ARY85PqUvCrklrAtDAx7JK70Ar9eHf-scw2eqDTN2k9dfBpPGZtRYRrmfgu_YjnAaCQuQQP6wnk4T7AEm_dpvxeAsaBLRF6o1PkQVGtUzCmTPa05NN4_t8_afACfnmRy3AyF3ry-WTs16sNq8W8CgcRuWrNymaNYK-Xnoab_Gh9=u-AfY3gt=CD8ZkbhZ6K2PdPS0jUMhgZoEmoC04uy5te9fH0wXVY5DrBhFENjw7ovf2TI9sLqdNzpXk8tMfd_vNmAsjT-JRxYsSuHRwrYH5B0f7ZKmdopdYJswYrwTwkcHkpkjOBRg4CZ-pon1uPk9hGMMKOL-lVGHCGuqORLSYC5HGQUmShYfM0uAgBDhZWBcGJ2_mwav=eotAE1OR4NPW2hIrRpqmVPqQsM9D4ybawHGx3U9x8SpzqMQTNwh_BMJgeSMw-dxNqLHVL=DXFPbNGhQK86TT=x_FvzD_dkeoPeOr0WCrUU6PMl7U4wIpfZhWB_NvrAoPUg4arbJFsoaDEfoTpu=tbz34w34pdnMmm8S2dahevjIlDFmhdC-OWv6OBvx2yTVdrYbGs0u8Glrzdho=PHjwHz3xLLVEDOzORupdseGxomUdyE-D8jRSJZpm-0KBvrB800TWpUqfbQfBlDC4yTM5eP=qBdvm=ok-_YD49xSO-yvqMNQl_ICE97I5BFBwSPNKrhpHZa_rwbA1UsS9OEdfTKyqQ056ocqujHdggqWXn_6sksU1Uxx9QFN4RTE88eUk8EfH8l-C1g_9ZSmf-JxlvTGKP0S=uYjL4h4Z4lUMP4Eq-EwukMVGvKVyhU74gvEZr3xgcUjVCqRBRgMDm0LrBln7S9FqNw5ynD7yKp6=2P=8ABqhQ4IrA8GZJWAxp634ZlAY106QHUEbakoJejJ7asX_9yJpvKhhVL-bCG85Gy4JHJenNsVqX1fEHjU0pQxnIv6Kmf6cLUZvpNVrZkBtgrjRHhVYl1WMX-dhQJYWTfzWAphMdZN8Zv0kmrjZ_dZ286YVqUvxcsOK0QwvLcQTSDnbAHlUPjlL5nGgfNTK1RYQWtEbALoLbroB5TZCn8jRUXSuRRUuB8EBIRvU0ZWDCI6=1SU3rO7RX7u0clqH2Goj7llEl-zGufdXwC6ySPL8vvyxBdFSgeN6notUw4FLhVvyxTZYZMxVVLvQZo1_aZYYW1YUh7Tw720m_J80v41lPXoO4036Td-nlAtRDzG4OjWymIzjurxZS5cGFaXKbpNHay0JXp-fc4-ZhRbTAM5JPsQpqMmKUUmDUoFKe4kR1tIcc7XCq7065x9Ar9ChyK53MuTjSKe016s-ShkDOpLv4VyO1mTBdfhFFSl2Z_zUNMWUII6TbpXpnaZoR-1elz7h4KlwK6FLFX=EPV8m6ZK0zm9MXfUdT36fpPFAx5IDlB1uEUr7BDuTS6vZcycHrUmtsUnNSfW5wJtyaEywxuJZ4018FR5EW4W9Yp8kzen74UrkBS58kM4DueAIkFGvlFttgrDvwUKdPXuGtQlwHJCG4Fx=Enena9ocxRMd7--nXYKEB1lVvTAb-LnKG6mSmbPYamaCSF7Jk6bRRjsxJ-5-pLLxTqhVM9Anj5O1G9Stb9ZnAPjyp_A7_MQwR-M5qhll7A9JX95xH_2WbrO3EwLMKOGNHh6VB3RtFJGcw8tGkdjhUDgzm-PeHznvZ1APlb_eLDE9uN2jRUzHaX-A0mHWpEHbvOmWowsWsKawJfaelzWQQESMOZcfK6Z6AX4jDt673cHKcnm_P2R0nrnGJj1x_lg-sU_ZEoTmRzNG_GK_zRVgIN65SIvXVK2WdL2UnHhPXutfEbCryklVF9kQLmWL7oMUDLS=M_c8We3rgfaUXVj56fmITmaCwSTGDq_XyIqROugw9ovYVVdLOLQTckoZh=KI9d3qLlW8jmHoanqtnyT3boKqUfNQ1sD0a377HE9xjKR0IEkBHbx25fD55gzwZfrGjyJJlk0zYwPGZJq-50fDRGQPdTKLWpXb8Nrky2aLnSufQB1pMIuREde4FuY4tdNXNgB=mdzS7jqyIENbBUuJQ=0GZ9x18vAoY0O8CqaX-fykc=dApXM2DEn929wKP=A0_cukSTff10RaJJrmT71=v0TlyUmgsG8pUIoekzvqXF6MbHDn3hywOXqkx3q3HQ063VbZ3l8B4SnIxpZ0Phjr1aN3NgpUwN8tddJo3fu3-apulI-WcgE6YVZHH5NMGl-jyXskhHwtcLAYHsqza4VnAYpcJUqljSMfKxJ5b0q62e6xa=HwjpHe3HC0QxV47O-FILRyXsVxWvV9R7UKVo0_nIpKuBondjD6T6MOWtGVk8dHav_Ubo=hLTkI7TSayqShVLrTvpJDJYHI8VnHCsVt9VZGqbu9DuLsYfbAQRhzkWYzqlFQG1x2YC-hdbE_NegS3cBRr-OAqkt-JXS2hm6FT_rEJeGKGZw=5D4EjKeZIQdLnFczxQ3eQTwSPPx8my9sx8E7-5l44790=I4M_XowIezn5CR02UkEwG-wKvVf7VvTUtJN0AeT7=k6wQNmNsIJbsB7FjW3lckUzvsK1wqXaoJQfBBsMUNOSfpP0U_ZJSlq1EcVca64WbY4IO4FKEQxYX970WTqk3bfTaZSjlhczy57u3jdZhdSLdO2JyU8w2ahmn96Sz=J5O25gVPtju1xb8InPSQVuLbXpQbhCypcbLfZCV3jGp2-bgIgqsjJ50tV0CXTlMXNalqB7CxQoYVKeayUdqvbfZTTmH=PIsuSDJla4_OpdcWGGXFVfVIQkpSEg7cD0IBds2wBIKX5qQBEFfoXpLsuCtyRRV4p_zTcAICG7eDCupVL-2Hbu1yUHWrLSaKvI0lz341TL=v9j=2GfhU3yJbchtBomno0qtdH0gg_7a2M0szOmxI51BFqeCW6aEuK5oPZ1p6YQ_xnuRy5oVcEyEkf3rWWx3x4RrlnmLUEVMTfUM5KNzTlYcu_YatJX8CgTusx58-9XzpCW2C2RquuZSaqog0xyewp671FN7QYfbAqxQPERkeSs=wl8nPMC2BQAxpuNy4EZZHT8d2vdNUzgXvDKIF4P2vZl84PpCam706oBoBHRqddcq7_Bk7UQsj9U=ZohByQ_yM_vrzv3vokuL8U=Wc5MsAa-hH2dKHz8MbY_Vl=6AvvC4UdsSR7zmMYxuOsbqoy3aUvljxNdv2D541yIsn0nLJ2n3g71jO4TQQecvPSH321tPdptQetnXHQ2SXN9uGoSfRSRqkeTGRyC1JMkJbTSn-CBwCRrEBMqsQyFtLZAcFr5IdRlHEoVpGsw6lVA87McxuBQ4v-vfsq5KXhosUSE85wMjJVnQbxF8n89gd_jqTqXVZesyWcp1OmROE-CcL7qAqg1Tv0QtmlGnlraScAbmVn_McjdYM0ywGaIH5sSYZOhNUUDXq8-zm__AxUkNor5K-a6na1nnMmWIeDlPO5ldF_qFBb7XrwslmZqOz3vz6bIM265yRTSPesF-5L61zoZbTyhXYPHpMs1XhVXPc1-tPe7Oz8Z5C4jxVG32F4QXWnS_5MXQ3fy85waSlJkDKgdx8f7N5K' \
--header 'x-jfuguzwb-b: -1u0a1k' \
--header 'x-jfuguzwb-c: AOCk-m6IAQAAFYrvrCjicYVdphI6nlJ3xiiF8l5oMjFB_QTLITtibCNBPpkT' \
--header 'x-jfuguzwb-d: ABaChIjBDKGNgUGAQZIQhISi0eIAtJmBDgA7YmwjQT6ZE_____-zYDxSADTRI9oH3bull_PmqGB7R8Q' \
--header 'x-jfuguzwb-f: Az-M_G6IAQAAFUK-h9BMxTIx4rh9Td-iOduSShaYujc8uwi0rhnpE7CqXFtwAWBA7-muchRAwH8AAOfvAAAAAA==' \
--header 'x-jfuguzwb-z: q' \
--header 'x-requested-with: XMLHttpRequest' \
--header 'Cookie: TLTSID=77364c168ae3162d970a00e0ed96ae55; o59a9A4Gx=A_tkOcuHAQAAcwtJiifwqfjX5qsoLMNFrzxMHPZcoK8MC-Qxz5iacJ5Fh1_KAUOhEw2uctk0wH8AAOfvAAAAAA|1|1|5b95f2a8edf5d9a3fe393ca993ade67a2a977235; JSESSIONID=0000n4Xt6U9JUpTV8Y4gKsnazW8:1e8uh364t; NSC_tibqf-ofx=ffffffff3b22250145525d5f4f58455e445a4a42378b; NSC_uppmt-usvf-ofx=ffffffff3b22377f45525d5f4f58455e445a4a4212d3' \
--data-raw '{
   "customer":{
      "firstName":"$YOUR_FIRST_NAME",
      "lastName":"$YOUR_LAST_NAME",
      "regId":""
   },
   "customerEmailAddress": "$YOUR_EMAIL",
   "customerPhone":{
      "areaCode":"$AREA_CODE", // 650
      "exchange":"$EXCHANGE", // 123
      "line":"$LINE", // 4567
      "textable":true
   },
   "date":"$DATE", // 20230524
   "fdbId":"$FACILITY_ID", // 1356376
   "numberOfAdults":"1",
   "numberOfMinors":"0",
   "schedulingType":"PASSPORT",
   "serviceCenter":"Web Service Center",
   "time":"$TIME", // 02:00 pm
   "passportPhotoIndicator":1
}'

```
In the response from above API, you will see confirmation number which is internal. 

```"confirmationNumber": "885V6oaBATo7E0hF32nDvpq=="```

It is different from public facing appointment number (e.g. *WEA247747604*) 

## Get appointment detail-1
You can use confirmation from above API to get appointment detail with public facing confirmation nubmer
```
curl --location 'https://tools.usps.com/UspsToolsRestServices/rest/v2/appointmentByConfirmation' \
--header 'Accept: application/json, text/javascript, */*; q=0.01' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'x-requested-with: XMLHttpRequest' \
--header 'sec-ch-ua-mobile: ?0' \
--header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
--header 'Cookie: TLTSID=247de6898ae3162d9a0500e0ed96ae55; o59a9A4Gx=A_tkOcuHAQAAcwtJiifwqfjX5qsoLMNFrzxMHPZcoK8MC-Qxz5iacJ5Fh1_KAUOhEw2uctk0wH8AAOfvAAAAAA|1|1|5b95f2a8edf5d9a3fe393ca993ade67a2a977235; JSESSIONID=0000aTp65HSMT1QfX7wwWK8iufk:1eo0i0qso; NSC_tibqf-ofx=ffffffff3b22251e45525d5f4f58455e445a4a42378b; NSC_uppmt-usvf-ofx=ffffffff3b462a3f45525d5f4f58455e445a4a4212d3' \
--data '{
    "confirmationNumber":"$CONFIRMATION_NUMBER" // 885V6oaBATo7E0hF32nDvpq==
}'
```

## Get appointment detail-2
You can use public facing confirmation number (e.g. WEA247747604) and email or phone to get appointment detail
```
curl --location 'https://tools.usps.com/UspsToolsRestServices/rest/v2/appointmentByConfirmationPhoneEmail' \
--header 'Accept: application/json, text/javascript, */*; q=0.01' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'x-requested-with: XMLHttpRequest' \
--header 'sec-ch-ua-mobile: ?0' \
--header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
--header 'Cookie: TLTSID=247de6898ae3162d9a0500e0ed96ae55; o59a9A4Gx=A_tkOcuHAQAAcwtJiifwqfjX5qsoLMNFrzxMHPZcoK8MC-Qxz5iacJ5Fh1_KAUOhEw2uctk0wH8AAOfvAAAAAA|1|1|5b95f2a8edf5d9a3fe393ca993ade67a2a977235; JSESSIONID=0000aTp65HSMT1QfX7wwWK8iufk:1eo0i0qso; NSC_tibqf-ofx=ffffffff3b22251e45525d5f4f58455e445a4a42378b; NSC_uppmt-usvf-ofx=ffffffff3b462a3f45525d5f4f58455e445a4a4212d3' \
--data-raw '{   
    "confirmationNumber":"$CONFIRMATION_NUMBER", // WEA247747604
    "customerEmailAddress":"$YOUR_EMAIL", // email or phone
    "customerPhone":""
}'
```

## Cancel appointment
Use internal confirmation number from above API
```
curl --location 'https://tools.usps.com/UspsToolsRestServices/rest/v2/cancelAppointment' \
--header 'authority: tools.usps.com' \
--header 'accept: application/json, text/javascript, */*; q=0.01' \
--header 'accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6' \
--header 'content-type: application/json;charset=UTF-8' \
--header 'cookie: NSC_uppmt-usvf-ofx=ffffffff3b462a2145525d5f4f58455e445a4a4212d3; TLTSID=15f2df9b8ae3162d8f0e00e0ed96ae55; NSC_tibqf-ofx=ffffffff3b461d1745525d5f4f58455e445a4a42378b; o59a9A4Gx=A7q4dKaHAQAABGS4rrM3HfQsd_TujRQy7YMYaPmcBdMRCQseA2O4x2cqp0znAWBA7-muctk0wH8AAOfvAAAAAA|1|1|f8c623357cb63d4206204c6e1f3403cabbc413df; _gcl_au=1.1.782839454.1682291834; _ga=GA1.3.43006258.1682291834; _rdt_uuid=1682291834619.36213974-556b-4af9-af39-3302c355b9f2; _scid=f0a1c33f-86ed-4afe-a6b9-224a1c939b9d; _fbp=fb.1.1682291834897.1579449299; _pin_unauth=dWlkPU1XRm1ORGN6TjJRdE5UQm1OeTAwTXpBMkxUaGpaamd0TVRJeE5qWXdZekUwWWpZdw; _sctr=1%7C1682233200000; mdLogger=false; NSC_uppmt-hp=ffffffff3b22378d45525d5f4f58455e445a4a4212d3; _gid=GA1.2.97217286.1682631820; _gid=GA1.3.97217286.1682631820; mab_usps=79; tmab_usps=36; ln_or=eyI0MzIxNDkwIjoiZCJ9; JSESSIONID=0000M2x_y7bX_k-doNdshQr0neI:1eo0rblp7; _session_UA-80133954-3=true; _uetsid=92b18cb0e54411ed9ee69b25d390831d; _uetvid=fb9d3f40e22c11edbafaef542560c5c7; _scid_r=f0a1c33f-86ed-4afe-a6b9-224a1c939b9d; _derived_epik=dj0yJnU9V0xIYkNveWphUTRTeGxnN1FDcGo5cUJkb1owT0J6NUgmbj0yN0JrS1NwTFpXUHhXQUsyV0dkWThnJm09MSZ0PUFBQUFBR1JNbXRZJnJtPTEmcnQ9QUFBQUFHUk1tdFkmc3A9Mg; kampyleUserSession=1682741974684; kampyleUserSessionsCount=19; kampyleSessionPageCounter=1; _ga=GA1.2.43006258.1682291834; _ga_3NXP3C8S9V=GS1.1.1682741514.12.1.1682742013.0.0.0; TLTSID=247de6898ae3162d9a0500e0ed96ae55; o59a9A4Gx=A_tkOcuHAQAAcwtJiifwqfjX5qsoLMNFrzxMHPZcoK8MC-Qxz5iacJ5Fh1_KAUOhEw2uctk0wH8AAOfvAAAAAA|1|1|5b95f2a8edf5d9a3fe393ca993ade67a2a977235; JSESSIONID=0000aTp65HSMT1QfX7wwWK8iufk:1eo0i0qso; NSC_tibqf-ofx=ffffffff3b22251e45525d5f4f58455e445a4a42378b; NSC_uppmt-usvf-ofx=ffffffff3b462a3f45525d5f4f58455e445a4a4212d3' \
--header 'dnt: 1' \
--header 'origin: https://tools.usps.com' \
--header 'referer: https://tools.usps.com/rcas.htm' \
--header 'sec-ch-ua: "Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"' \
--header 'sec-ch-ua-mobile: ?0' \
--header 'sec-ch-ua-platform: "macOS"' \
--header 'sec-fetch-dest: empty' \
--header 'sec-fetch-mode: cors' \
--header 'sec-fetch-site: same-origin' \
--header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
--header 'x-requested-with: XMLHttpRequest' \
--data '{
    "confirmationNumber":"$CONFIRMATION_NUMBER", // 885V6oaBATo7E0hF32nDvpq==
    "cancelReason":"$CANCEL_REASON" // CHANGEFACILITY
}'
```

## Cancel reasons
```
curl --location --request POST 'https://tools.usps.com/UspsToolsRestServices/rest/v2/cancelReasons' \
--header 'Accept: application/json, text/javascript, */*; q=0.01' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'x-requested-with: XMLHttpRequest' \
--header 'sec-ch-ua-mobile: ?0' \
--header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
--header 'Cookie: TLTSID=247de6898ae3162d9a0500e0ed96ae55; JSESSIONID=0000dsDDmHemQxf6DQEY4hCfueH:1eo0i0qso; NSC_uppmt-usvf-ofx=ffffffff3b462a3f45525d5f4f58455e445a4a4212d3'
```

The reasons are like:
```
[
    {
        "displayName": "No longer need an appointment",
        "name": "DONOTNEED"
    },
    {
        "displayName": "Need to change my post office",
        "name": "CHANGEFACILITY"
    },
    {
        "displayName": "Going to reschedule my appointment",
        "name": "RESCHEDULE"
    },
    {
        "displayName": "Need to gather additional documentation",
        "name": "NOTREADY"
    },
    {
        "displayName": "Cannot make my appointment",
        "name": "UNAVAILABLE"
    }
]
```
