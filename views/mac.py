from netaddr import EUI, mac_bare
from macaddress import format_mac
from macaddress import default_dialect
import re

#将MAC地址转换成想要的新MAC
class ClassFormatMac():
    def formatMac(mac, macDifference):
        mac = EUI(mac)
        #将MAC地址中的符号去掉
        macBare = format_mac(mac, mac_bare)
        #format_mac(mac, 'netaddr.mac_cisco')
        macBareInt = int(macBare,16)
        #将16进制转成10进制
        formatMacInt = macBareInt +  macDifference
        #对10进制进行计算
        formatMacHex = hex(formatMacInt)
        #将10进制转成16进制
        formatMacBare = formatMacHex.strip("0x")               
        #去掉十六进制前缀     
        formatMacZfill = formatMacBare.zfill(12)    
        #如果出现前面是0开头，进制转换中会出现缺位，重新填充0
        pattern = re.compile('.{2}')
        # 写出正则表达式 任意2个字符
        formatMac = ':'.join(pattern.findall(formatMacZfill))
        # findall是找到所有的字符,再在字符中添加":"，当然你想添加其他东西当然也可以
        #最后发现EUI方法直接就可以从字符串生成MAC,但是生成格式为AA-BB-CC-DD-EE-FF
        #formatMac = EUI(formatMac)        
        return formatMac

#原方法使用下列方式计算，取MAC地址最后一位然后计算，但是考虑如果最后是FF很容易产生进位问题
            #ipmiMAC = "aa:bb:cc:dd:ee:ff"
            # print("the pxe mac is :", ipmiMAC)
            # prefix = ipmiMAC[:-2]
            # print("the prefix mac is :", prefix)
            # last_two = ipmiMAC[-2:]
            # print("the last_two is:", last_two)
            # last_two_int = int(last_two, 16)
            # print("the last_two_int is :", last_two_int)
            # new_last_two_int = last_two_int + 3
            # print("the new_last_two_int is :", new_last_two_int)
            # new_last_two = hex(new_last_two_int)
            # print("the new_last_two is :", new_last_two)
            # if len(new_last_two) == 3:
            #     new_last_two = new_last_two[-1:]
            #     print("len == 3", new_last_two)
            # else:
            #     new_last_two = new_last_two[-2:]
            # pxeMAC = prefix + new_last_two
            # print(pxeMAC.upper())