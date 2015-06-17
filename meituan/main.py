#coding:utf-8
'''
http://www.meituan.com/index/changecity/initiative
1. get cities href 
2. get city href 
'''

import urllib
import urllib2
import os
import os.path
import time
from pyquery import PyQuery as pq

class mt_city():
    cities = {}
    def get_cities(self, city_url):
        p = pq(city_url)
        city = p('.isonline')
        city_dict = {}
        with open('cities.txt', 'w') as wf:
            wf.writelines('city, href '+ '\n')
            for ci in city:
                q = pq(ci)
                key = q.text().encode('utf-8')
                value = q.attr('href')
                if key and value:
                    wf.write(key + ','+ value + '\n')
                    city_dict[key] = value
        return city_dict
                
    def get_district(self, city_url):
        p = pq(city_url)
        districts = {}
        dis = pq(p('.filter-list--fold').html()).find('a')
        for ci in dis:
            q = pq(ci)
            key = q.text().encode('utf-8')
            if key == '全部' or key == '地铁附近':
                continue
            value = q.attr('href')
            if key and value:
                districts[key] = value
        return districts
                    
    def get_business(self, distric_url):
        p = pq(distric_url)
        business = pq(p('.J-area-block').html())('.item')
        dict_business = {}
        for bu in business:
            q = pq(bu)
            key = q.find('a').text().encode('utf-8')
            if key == '全部商圈':
                continue
            value = q.find('a').attr('href')
            if key and value:
                dict_business[key] = value
        return dict_business

    def save_data(self, city, city_url, district, dis_url, business):
        save_path = 'data.csv'
        if not os.path.exists(save_path):
            with open(save_path, 'w') as wf:
                wf.write('city,district,business,city_url,district_url,business_url\n')

        with open(save_path, 'a') as wf:
            list_data = []
            if len(business) == 0:
                data = city + ','+ district + ',' +  'None' + ',' + city_url + ',' + dis_url + ',' + 'None'
                wf.write(data + '\n')
            else:
                for key,value in business.items():
                    bus = key
                    bus_url = value.split('/')[-1]
                    data = city + ','+ district + ',' + bus + ',' + city_url + ',' + dis_url + ',' + bus_url
                    wf.write(data + '\n')


    def get_data(self,main_url):
        cities = self.get_cities(main_url)
        ci = {}
        for key,value in cities.items():
            districs = self.get_district(value + r'/category')
            for dis,url in districs.items():
                time.sleep(4)
                business = self.get_business(url)
                city_url = value.strip(r'http://').split('.')[0]
                dis_url = url.split('/')[-1]
                self.save_data(key, city_url, dis, dis_url, business)

    def get_data_constant(self, main_url):
        readed = {}
        alldata = {}
        with open('district', 'r') as rf:
            head = rf.readline()
            for line in rf:
                tmp = line.split(',')
                dis = tmp[0] + tmp[1]
                alldata[dis] = line
        if os.path.exists('data.csv'):
            with open('data.csv', 'r') as tf:
                head = tf.readline()
                for line in tf:
                    tmp = line.split(',')
                    ci = tmp[0]
                    di = tmp[1]
                    readed[ci+di] = 1

        while len(readed) != len(alldata):
            for key,value in alldata.items():
                if readed.has_key(key):
                    continue
                try:
                    time.sleep(2)
                    tmp = value.strip('\n').split(',')
                    city = tmp[0]
                    dis = tmp[1]
                    url = tmp[2]
                    business = self.get_business(url)
                    city_url = url.replace('http://', '').split('.')[0]
                    dis_url = url.split('/')[-1]
                    self.save_data(city, city_url, dis, dis_url, business)
                    readed[key] = 1
                    print '%s %s : %d' %(city,dis,len(business))
                except Exception,e:
                    print e
                    continue
    
    def test(self, main_url):
        cities = self.get_cities(main_url)
        with open('district', 'w') as wf:
            wf.write('city, district, href\n')
            for key,value in cities.items():
                time.sleep(3)
                districts = self.get_district(value + r'/category')
                print key, len(districts)
                for dis,href in districts.items():
                    wf.write(key + ',' + dis + ',' + href + '\n')



if __name__ == '__main__':
    cities = r'http://www.meituan.com/index/changecity/initiative'
    ci_url = 'MeituanCities.html'
    dis_url = u'http://bj.meituan.com/category/'
    business_url = 'http://bj.meituan.com/category/all/chaoyangqu'
    mt = mt_city()
    #import pdb
    #pdb.set_trace()
    #mt.get_district(dis_url)
    #mt.get_business(business_url)
    mt.get_data_constant(cities)
    print 'end'




