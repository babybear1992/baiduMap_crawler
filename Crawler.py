import urllib.request as urllibRe
import json
import os
import sys
import time
class Crawler(object):
    """docstring for Dimension"""
    def __init__(self,lng1,lat1,lng2,lat2,item,tag,ak,file_path):
        self.lng1 = lng1
        self.lat1 = lat1
        self.lng2 = lng2
        self.lat2 = lat2
        self.item = item
        self.tag = tag
        self.ak = ak
        self.file_path = file_path

    def get_lng(self):
        lng_sw, lng_ne = float(self.lng1), float(self.lng2)
        lng_list = []
        for i in range(0,int((lng_ne - lng_sw + 0.01)/0.01)):
            lng_list.append(round(lng_sw + 0.01 * i,3))
        lng_list.append(lng_ne)
        return lng_list

    def get_lat(self):
        lat_sw, lat_ne = float(self.lat1), float(self.lat2)
        lat_list = []
        for i in range(0,int((lat_ne - lat_sw + 0.01)/0.01)):
            lat_list.append(round(lat_sw + 0.01*i,3))
        lat_list.append(lat_ne)
        return lat_list
    
    def get_block(self):
        lat_list, lng_list = self.get_lat(), self.get_lng()
        block_list= []
        tmp = ''            
        for i in range(0,len(lat_list)-1):
            for j in range(0,len(lng_list)-1):
                tmp = str(lat_list[i]) +','+str(lng_list[j]) + ',' + str(lat_list[i+1]) + ',' + str(lng_list[j+1])
                block_list.append(tmp)
                tmp = ''
        return block_list
    
     def check_block(self):
        url_list = []
        for blk in self.get_block():
            first_page = 'http://api.map.baidu.com/place/v2/search?query='+self.item + '&tag='+ \
            self.tag+'&scope=2&bounds=' + str(blk) + '&page_size=20&page_num=0'+'&output=json&ak=' + self.ak
            sample_obj = urlRe.urlopen(first_page)
            sample_data = json.load(sample_obj)
       
            if 0 < sample_data['total'] <400:
                if 20 % 10 ==0:
                    page_num_max = int(sample_data['total']/20)
                else: 
                    page_num_max = int(sample_data['total']/20) + 1
                
                for page_num in range(0,page_num_max):
                    tmp = 'http://api.map.baidu.com/place/v2/search?query='+ self.item + '&tag='+ self.tag \
                +'&scope=2&bounds=' + str(blk)+ '&page_size=20&page_num='+str(page_num)+'&output=json&ak=' + self.ak
                
                url_list.append(tmp)
                
            else:
                if sample_data['total'] != 0:
                    doc1 = open('error_blk.csv','a')
                    doc1.write(str(blk) + ',' + first_page)
                    doc1.write('\n')
                else: 
                    doc2 = open('zero_blk.csv','a')
                    doc2.write(str(blk) + ',' + first_page)
        doc1.close
        doc2.close
        
        return url_list
    
    def get_data(self):
        res = []
        for url in self.check_block():
            obj = urllibRe.urlopen(url)
            data = json.load(obj)
            for item in data['results']:
                jname = item['name']
                jlat = item['location']['lat']
                jlng = item['location']['lng']
                j_address = item['address']
                juid = item['uid']
                temp = juid + ',' + jname +','+ str(jlat) + ',' + str(jlng) + ','+j_address
                res.append(temp)
        return res
    
    def get_result(self):
        
        start_time = time.time()
        print ('Starting at '+start_time)
        doc = open(self.file_path,'a')
        column = ['SID','Name','Lat','Lng','Address']
        doc.write(column)
        for row in self.get_data():
            doc.write(row)
            doc.write('\n')
        doc.close
        
        end_time = time.time()
        print ('Ending at '+ end_time)
        print ('Completed, which took about ' + (end_time - start_time))


if __name__ == '__main__':
    
#     lng1,lat1 = 121.15,30.86 # 整体sw
#     lng2,lat2 = 121.90,31.36 # 整体ne
## 选取核心区做测试
    lng1, lat1 = 121.42,31.18
    lng2, lat2 = 121.56,31.25
    
    item = '%e8%b4%ad%e7%89%a9' #购物
    tag = '%e4%be%bf%e5%88%a9%e5%ba%97' # 便利店
    ak = ' ' # APIkey 
    file_path = 'bianlidian.csv'
    Crawler(lng1,lat1,lng2,lat2,item,tag,ak,file_path).get_result()