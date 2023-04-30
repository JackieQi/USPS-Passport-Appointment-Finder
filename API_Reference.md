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
--header 'accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6' \
--header 'content-type: application/json;charset=UTF-8' \
--header 'sec-ch-ua: "Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"' \
--header 'sec-ch-ua-mobile: ?0' \
--header 'sec-ch-ua-platform: "macOS"' \
--header 'sec-fetch-dest: empty' \
--header 'sec-fetch-mode: cors' \
--header 'sec-fetch-site: same-origin' \
--header 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
--header 'x-jfuguzwb-a: -K-2r0=-SY-TCgpTZVlL8rzHNDHdvtD8qVQgOwf2jbs5koj9BiRhx=pSnnbn2gqwtTjNW9WNrTskYsIa6YZ1vhRoXWd-0ERw6_N9OxmhF8kPg3pSPHRRUQz2Dhpszzs40aUEbpUdBIxWXHFViM7v6lR-wytTQCd-bM4DMXgUUJ8rmKEmBhT0QAJQ2yzunrpviEbqLzXbk5r06gmQ4aM2HYsUfvY5KBdqWE8rVonm9OuiGgFoU0jmdBYxnMvTjOzbo0MxZZX-kXAP6NbzrcVzcu82t2MYMIsXOUOnqmwi4LRij=znZr4rVYWNhLsgZE3oo3PDdwx49SorwmczsxCbzEh3AmKQhoi29LcRDdNR2EVViwJVi3S9A3ZRzv5ccWIxAT2IXN0tFYxAnZVUponY_i8Oj5Po3RRmbVF_YVQ_0H_GGcfb0wM9QzvnxWYv4cuNJ9iUPkGgphr2AuronL2ROGXw7pN1v9PfW1GBC=aO2JaxDhtIczmtpsdv4KXLbvw9aTCEOkEHJFHlfOvgQ7BRxzvHJM5nROswVZ4wXakph69s=dU3wGt7RhbU4YtTSQiqk_TR0bFi3X51DF=Lb=qBZPQya2H0qPEJBHff4X0nppzvmjl-lcUWEy6uKyGvtIa10_Pui36XC0_wJyLA2PdXQ1d8PTO9KxWOjq9tOv5bMnTDRD=pGKYAa51kazfhmx2OOqgPQhxSoGI37i7nRjiqJMzD9sQqJiYoCJuc6WNS5xGlYSkkbFjPpIiidmnnmxg8mXQhtS2Bv=jY-toGgbqyUqAKV8oGQkiS73iW-bq4DxthjotJFs0r9am_d2pBo8i-FJUUsp9j5szb9MMJYNDBwzjAkhYymQM1akZT9T6I_U08BhgL81uh0_A_SIGaQZMLipnBg=ybE3mg0UMJ5bqkf-TJXdbPDZu2Ok0PhstSzOwAif2wLE-W0xBOGUvGFiSfENkb7ilwnE5Dtjw3Dw_kXqfXky5FjiBfRTww521zhXGjbZRi18rIqjzgzw_Zjm=jYWGXdWn5P8CdPCqrrc3BlGhpa-d4mAhG400qRjycAF1Q8sZt-ZI93gfYhOd0-rpyPFWx8wP4jtR7XO7M24zwE3mp5OQ3kapUdSTzhOREQ7Q4wmghdNB-E7ZEYbakZoFI0mbKDt8v8DyATtxJUojtUDbX9x2g=QycRMoJx6yPc0Ad=d405v-InDAuYEYrJ3M9OD0pUQmmBMDQswi76X8iWKgF7-QEPQYW7-v1zIC=HmaNHVOHVKJfoZ2RgAj=mlhinsYfkIsA=vFz2LydpXxqbXlK91ZD8N7lTWkYjk73Uf02vzn-LkEnd47kZ8lknpZwtnm8=t1L8GHsWvt_4YXDjjP7uqdBqm6zAq91aXkOR60MummU22GpusDY31aaRL22QwJjy4xqwLcot9-XCrpy14hrt87l0Il=YFTub_=dtblmYAFwa0FstXIq4LJNBGHlgfzzgg-73UCyhgd1yYEsmE=oVXjEn2VNGiajOVw4BurQd4ud9EItQNusA7FPHwwcxXL5JYQsOVwSSC6jVDM2iit4OjanzmK6GXsY3QmIRKVEPtL71himZMX24s8LrrwXDjXRtTRNJJAducEgVnglSbsKgiyFG1AP4FM2UVpW-cp1t2QFv6ON=4XJSsN0AL057JSKuWd2C5O_4jF-dzXDOpZyQMkNUrygAI=PkYnKXZJfhyNma-RvR9qOYzmkf-X0lI0xRpJFw8bR45PtpQpaS=g6atfp4SdVXOb_8x974O9TMlSpf3Y75noorqwR47Z9YRzNtVIiCCVYikd9=fGoYA_ZWlPHMm7oFx8VN-f-rBdXUvK7ZZKnXlW1YxQCSJlPDJf_z-B=vkjBAi3cVVKBCKobOJ0FmnxFH_LhNppngCR2Hf7rHB_pU0QvQnSc3_M=laxVPnfUFyGnOJaZRiM2xo=WVZVB0dEkC1XfT7Rcdvi5ukbrQ=JNPgIr7dOMx7gHpWyH1AST0RDHXVu5bPlx=jwtJFcwn=fv3vYZgNfwGKhvDrUmWO0alSRr59utlz95jj8TVkot6aVGb=dzarWROdECasuMfYuywB2kli-70nvK0TW2FOiHbmz1Nq1Zi0IJOjZ3d_l4LLW4nOVKPdE7VL92=RSGAizaAytPjfu4FPKMnLSq7AmEmYO88mcxqbZjwTilUITvDKtfwtWnXkXaoV_f-5msBS7wM7v5gRpBISyCEnOmFB0rHvTy1y=MJRuL4F08zZYO=CC5Qbc3aWQz3UqCLpxJl=7_fA2tjkO9IMaWUS=JG6kWz27gHrMSVhUNdNtcD7NAkBTC2r_DBMkrTF6ApPxdWt1tAUy__-knM5PD-y14UDzBsViWAybGPp7VIaFN56z8BDjLw4lKGaUgyZz_2_sUHWV4w-isr6fiuIjVis6YpccDuRXMqdbFngRAjwQGkhhuQEFEKQMfiBP2IPMv80aWrOgkYkon2KyoSnuT32Fc364wE0qrJW1Wchht21XxcFPbd45kvF=Sm1tP4=oyb=QwsO-cVCcCrQWhS_hPAS3pYbc_BxYXLialc=LSRVjYU7tqxZOqbR=l7mWnR2AhFmlCg7XMbTqgV4Imd8Exqp5dGrIZO7xj1p1C4imF9ELO7hcmbjYAd4_iW_PQUOLzoztFPnTMQ1puBwcaAXjnJhD2CThqKXu5ci6UtVxDErXhLLAk9wapM=ajAzQmS0tCKFAdvEVcgxLImwsIXZ8fSpTUuff3QOtNo0OE6Kdr3sSPk51DZGIFKcHqo7bfZpAnDNnW-6ffyQ20NCi9lErPyTYnBj9I4ouKG07RTZfiWYMo0pqrAEJAd8HygvwvIrEI51RFA0i6ktCd=6Nn6H2pOs0i2tbhQyr0Ikhao01GwGxpLc1SgpNzX=nc0fEoNgmAYiwT7JMVsa57dAGfT5Lt20StO4ip8lYaDK=IXhnYgT1PxwAhS_uJ_8IC_CHGkwsnWgZtMfc_tR-4Kg9HmbbYK66cqrNxZaRXDzNninbppdWNFTl5ITDSnEq5BPzrx8dgulN2w7PoK0gCJ7pCC7cRNC1smgsqnkPOAiG1i7SGQYb8iMCFcfAayXqckUTBg8=JNTq1Ob7K4vdoWkEwQMNNq8kS7Tv1M9ukncEjbDkyfqQZn1-StqcE4qP98iRTcVn-IDYOvxCRZ79ht1IYmm_fB35KSCARf0lkfJiKB1D7WWWAtgFtJwnplMTnCjRlMrA0IuNYOXtAoIx3lrwO3jaI4SjWnUqBzbJwBWRtnWuTrPcIoQ4u9BlANNiXNtm31ZLPWtJF49l3ABTZ4dbMcd1YuBm0PNoXToQml0a5kWg9Bcv_BEpJ7aJE-g3a6Jg09pwm=8EgaXKctdtifUap7mrtEwuvZA=yK-CdrSiE5dlqqxDaMwJzM=PaZzWfjdn_3A29=fYhxVphWOj4M-i-CZfclxr33NRYNKkcKxWBjJfxF0m5Bb_tusCaP7W-VnFGANLHCu_iZTilzNLlG73OOrMFCIUZTFKuIgfXZjzD7nDmMS-fLYg8zZgL0KBNTNiFU9RZDfnF1jvIp2DbdHXoHT-oS=5As3pPXpO_GxqDA6YHxl=xM-uDSubfMTakPC65o0H-KyFlEnO4KgKydUbBsOSCBRiwVSd4kanGj9ToPC46qI-9kJpIx70lFBxk6RiTNNznB4zH5tma0-iUn-kF=rZFfE-TvwDrcErKjSnDci7FIE0z=unqMuG8dDUs4qGRSz6U8O0QZxV8SrKNy=nnax9sn3bWHf1ukwpty2Md5lHoaUUf64KcdkmEAZS4NNn70=Eaa6NmO8TfJfGi4XGOntWf_Lstwp9l1TNXrUJYsnOzusEKN1sk=uPpn_LlTFLVhbcpNDxuRYim7h1MCzxAtRgBXHBo822S7hkLiOKuUloub6w8Qirt2tKCV9CTzpZcPzSZcJXUQKtliVKUFrdc45HYXComjjXDqAh8ZDIaCUT8JNxIB1CEkbxVtyHRcwyoC9zawbNDJGOcsDG1jm0rT_Z86dR_tkq09VUC4PvAFHcqDURXrx57o9aSoNSN38W1LPnqDfxpIXUTm7P-8KLVABHKmfxAT=_9gRym6h4Ps28-lmXik01fi81-dN_OxNEdD81oxxtflxfbyNQuPcFPMYU7QQh1Pgrp4bSiunlmA59qSEbb-bn6uQ54m8PoaVf5IcyLzrTNlii9Cv1yWADZZC9Bt9buYySIi1giKKfbV2T6xL=_dzHLn72=tT4GGCn6L9SAzA_cGhHQGBf1Nm7jgcwkZxyUEi0ZzhFuq7oiPNgj1WW3Jgrp95IAxayBI6FiP=mMCGnF2f1Lo-9YXwjP6tS8_ChZmKrFTPR4CsnA52BCGNprLDktZxcM8LVdS_mWT4YPstB_mMTOJ1VW5a5s1LZtz_VdJibgVEbIVqRKVoHxYKBPWoY_dqM2EqAyc9VAQxp3w0DSFyO29tN-5OpFjJLrj7lV=UM4Ay3DAz=MQ6jT7oQSEzRwumyGO-Ycq1aJOwn1xJHvDxphW1Wv3pio4xs4Ngm3Q8tzWH46ul7D0FJpunq67NkaV=Y=MY92S0CNCKMJHN2m-0gdZ5ob-X33D7RLKR_qxiXmEonUZKtl4malBTTmEPXQqs8xQDdw80y1Gg1nTnQ2sbP2zWwWKOCuxZ3zhPTx2nMDRfhjXvBLXu4iX3Ax2xifW1O5gQvSbq7ZxnUNpyBRWMysVupzaRG6gx5wGBV0KdqbIhkKAj2v=QZ-hz5SDgAymFvHhHv4HguiPqrGUKl8WF3vrvdEMWKlRkBvGifKYZ8dvtRJn-vdRxVNv_VcRDapqVnYmgD3k4zlTq9ZdF94th-_A6JMENgok0AbC66yr50Gim8kv7ZsszWrKR28Ux8IZ7Sw3T=QAgJxLHi8qn6f0yXn0Fd7jZV4UHAbBSTVs-i-95VDCxBi4rB-oIqs7VmNAbJJuJV0cEI3lL3v3pC7lnoPOwg-x99uDfk=sWCBvGPg9yq1pvGrQoMibLDLmCI3LGVVJvTk2kunVjuNgE49xjtixc4WDv9uMThX4RcoRPVxw63Y5gpPl67_OWqEaHUR25Bg_dWDIxYqNYll6AzwtqHr_SdVk-Ph7=hniorDL0PE9fWKhBuyva2dZLCMKYRaQ7IUEFugtq7bBwF6HUxj1ko_LYPPj9HYYXkKvLSxCX6jJ0VP3h1l_YgV92HrRZ93Oh61YE=a5JJMSboZW8ddfPEyI5i1-mVqOFFKbEo_9A4aiDhdREB0DLmbw8gqUnVYDlEiAT7-zKWPIEsGgus6uxD4N_wZkXEi4c-=D0zQlD9gw41F6fg4VCNxoCsiTTDm9AuCbu=pOgl8ri7tvDgwk08hB4kmRZ33-bgHLkNX6fy4d0qUbI1Qqz1OJ4uW_m_dS4O43bquurIszThgjz1MTo4xpKH95DhtJjIyFb6sP=GWhcQcq8OG6yPO5C4mmsLzoLWtXKW=2yv8ojtkyzTcP6cuYIcDi8-OySSId4HGLzm8tn_iD8pVRmZnHCCjnoCTVCwDT0DZ59R8jO_fi0=H_c69oHH8=N2aW4Ty8PJEGb1XQTXn9XU=cXObvH0YSAwZd6vpY=bvp1qu1OMTD7lhZwtgdwp6aHfIjZ5Z_QERZU=oc3M8UI8ao0GBZfbSoWtOuYDUsU9Xfb07UQkwH8as9cw4cErKgHjzJbHn6gznB3gyWUgSgqwVaDKZkY_9Q1wV7Q0fZN-FRUnSTgaAm0HrEvlBBM6QZGBMtVpA7rD_ii3sgI0tOEMJQkUsyi4Apk1LKJWAWnpBL8Mc53XpPHhIDOrja7HUYu7IEmF5C0Ua35OiavfgYtclWvECUNuB6x15o_=RpU21fEjjzO8oiNcF-q7hb6uyd87CIDZEy7oT119PWbV9okjHPEFxEZNrhEMRFhjEn8K8lipsrJJV5I8sCyPcY6Bwno9Op==_2mVqNuKo9j4lRJ9VpIoGHM2zqLy8tPOzS2R8PzR=pBhZ6ufXrGjwlPwlS9vGXiydwDbwwLci9AZXWmz66DMg4m9Pv8M0w_IS6DrZvdtmxwUU0B=K2jlYVLkF=1pazo0UcCl1tw7M1sVxa=K_=WGtMb8MnOCHHHWfPmHoEZHFIFNb09=3JKju4GqFVrICSxcUbAKGKY9US6zDGPXK9iRNi0ffDE9AF1QzzyyD7tH-8bhpaqlslhDLi6Y_9CTigOGLdkkR3zET55X1G6csw3Kzu9RTy1TFOXFYy=P49u7Yz-DEnSRH1d--QLiQKtXWUTu9RDayI2nUSIDWxIHYgQUdwpuda2bfJJaib_5G8fmUq5s7ZLB8CLgQlHpYQrgZBaTXKQcln=xKiI1iqt63MYDw_AcCPgdg65tEQc=5MnWXd1LF1gLQScDdDEFrIjjUNqdBPVQ0MOsFvwi6WgQswsu5xtj4BnJZYHyopOVX-jUfhKHrOKLNE3XZ9=fKidin7IJ=LghoJtT4s-lIssK3bhyHKyiw=7n_IiPPuONbO5Nft8t6JzuXOFTTDIlHsvX4yCW6idvQE_nvXQc-k4lZLgoYLGoXzLA5v01FDPnY1LNBY1PvYS0XItbx=PRVB5_UwTJE3NJWVQawEapkIjw6iqIBiCUOB1H3lDYbr-zZkuyakQTyuu-BGO9rX_cT1gJVY85zSxRj_DUFu4rH8aCJ_p1H3DrPC03fWWxtS-w2SdS=PqRUyuQXRsjDZQaRk--_tNnqDlKb9oLSDuYMDapSiEE=LZFHcVK_illvmd16TKRlRJO4ZVAj4ivLo6tW6S5Ypt_Jmz_mxElY5J2FWOEMERKjcQjUf7juAu_sXddgCO=gG_pdWaED9l79gg5vLM7bjEjdAAELfDt5UHGHo=bmMtfdG=KH_4p2knaXasuXT-0YPE4k4wXxzE3cV6W2IqTQavnQWzZ4FCXRKzQJImcPKz61ypRCYBo0dzW1--fQMBlrwRtism6sn0=oQcF3nq-XDLOLtjL3u4Cu5Nv5uB4WJF1i_DGl=cIs24lZXRrOQW5s9knBymHzlIM=kg9NPnF7KWcq4j1magSNZ3uZfcsczKX21c-GaSPoms=8=yKc_PK_0fJ-bWuPEQ1InXR_XJIJg0Y4uN-uzVDqXi9uxCs6wHyNuFr6dn-bgrLgyt7kI3uF8YnO=Kh7p=vUDu6qiNsCqLInvQIM=qP0Zol=MkrTaFC930m9J0BB5oHH9iaZ-VD4KEQxQbF9AGWMtTa6ganquz=dsQqUMQcyxtJ1xwt2IMAqd2pQ4wvtv=qc5_v9kMk1OS1JqW3cOc9GfD-h3FEkUFkt3xHHjEsRax6QSsYpjARKzEXCzlpzlbXP2m4o' \
--header 'x-jfuguzwb-b: novv2r' \
--header 'x-jfuguzwb-c: AIAehsqHAQAAXeBr0sZP8e8062TpkNZhFN016TK3VZGucM0M2ZqaIR9FaOX5' \
--header 'x-jfuguzwb-d: ABaChIjBDKGNgUGAQZIQhISi0eIAtJmBDgCamiEfRWjl-f____-zYDxSAP84OwwraDmwK1FPpcvuYqo' \
--header 'x-jfuguzwb-f: AzuKisqHAQAAx_Ru3-AycK2ULWi72Jf9zSrNTrn5DnVmsk4OoZnASyvq1adYAWBA7-muctk0wH8AAOfvAAAAAA==' \
--header 'x-jfuguzwb-z: q' \
--header 'x-requested-with: XMLHttpRequest' \
--header 'Cookie: TLTSID=247de6898ae3162d9a0500e0ed96ae55; o59a9A4Gx=A_tkOcuHAQAAcwtJiifwqfjX5qsoLMNFrzxMHPZcoK8MC-Qxz5iacJ5Fh1_KAUOhEw2uctk0wH8AAOfvAAAAAA|1|1|5b95f2a8edf5d9a3fe393ca993ade67a2a977235; JSESSIONID=0000aTp65HSMT1QfX7wwWK8iufk:1eo0i0qso; NSC_tibqf-ofx=ffffffff3b22251e45525d5f4f58455e445a4a42378b; NSC_uppmt-usvf-ofx=ffffffff3b462a3f45525d5f4f58455e445a4a4212d3' \
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
Use the confirmation number from above API
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
