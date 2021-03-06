# '''
# author: ������
# create: 2020-07-16
# update: 2020-07-16
# '''

from models import Attend, Course, Category, Majors, User
from collections import Counter
import difflib
import operator

# 获得字符串匹配度
def get_equal_rate(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()



#分析相似课程
def calculate(id):
    user_list = []
    allcourses = Attend.query.filter(Attend.id == id).all()
    for attendcourse in allcourses:
        samecourses = Attend.query.filter(Attend.id != id, Attend.CID == attendcourse.CID).all()
        for samecourse in samecourses:
            user_list.append(samecourse.id)
    res = Counter(user_list)
    most_sameusers = res.most_common(3)
    cidset = []
    ratelist = []
    common_courses = []
    for user_id in most_sameusers:

        attends = Attend.query.filter(Attend.id == int(user_id[0])).all()
        for attend in attends:
            iattend = Attend.query.filter(Attend.id == id, Attend.CID == attend.CID).first()
            if iattend:
                pass
            else:
                for course in allcourses:
                    course1 = Course.query.filter(attend.CID == Course.CID).first()
                    course0 = Course.query.filter(course.CID == Course.CID).first()
                    rate = get_equal_rate(course0.Cname, course1.Cname)
                    if rate > 0.95:
                        pass
                    else:
                        if len(common_courses) < 6:
                            ratelist.append(rate)
                            if course1.CID not in cidset:
                                cidset.append(course1.CID)
                                major = Majors.query.filter(Majors.MID == course1.MID).first()
                                common_courses.append(
                                    {'cid': course1.CID, 'name': course1.Cname, 'major': major.Mname,
                                     'school': major.Sname, 'rate': rate, 'info': course1.Cinfo})
                            else:
                                pass
                        else:
                            min = ratelist[0]
                            mindex = 0
                            for i in range(1, 5):
                                if ratelist[i] < min:
                                    min = ratelist[i]
                                    mindex = i
                                else:
                                    pass
                            if ratelist[mindex] < rate:
                                ratelist[mindex] = rate
                                if course1.CID not in cidset:
                                    cidset.append(course1.CID)
                                    major = Majors.query.filter(Majors.MID == course1.MID).first()
                                    common_courses[mindex] = {'cid': course1.CID, 'name': course1.Cname,
                                                              'major': major.Mname,
                                                              'school': major.Sname, 'rate': rate,
                                                              'info': course1.Cinfo}
                                else:
                                    pass


                            else:
                                pass

                    # if course1.CID not in cidset:
                    #     cidset.append(course1.CID)
                    #     major = Majors.query.filter(Majors.MID == course1.MID).first()
                    #     common_courses.append({'cid': course1.CID, 'name': course1.Cname, 'major': major.Mname,
                    #                            'school': major.Sname, 'rate': rate, 'info': course1.Cinfo})
                    # else:
                    #     pass

        # len = len(common_courses)

        # for i in range(len):
        #     for j in range(len - i -1):
        #         if common_courses[j].rate < common_courses[j+1].rate
        # common = sorted(common_courses.items,key=lambda item:item.rate[1], reverse=True)
        # common = common_courses.sort(key=operator.itemgetter('rate'),reverse=True)
        # if len(common) < 5:
        #     return common
        # else:
        #     return common[0:5]
        return common_courses

        # same = Attend.query.filter(attend.CID == same.CID, same.id == id).first()
        # if same:
        #     pass
        # else:
        #     courses = Course.query.filter(attends.CID == Course.CID)
        #     commoncourse =
