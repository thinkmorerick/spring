# coding=utf8
"""
 不区分资金、资产端，按照一笔交易进行统计
 通常的统计中，按照道口贷是信息服务中介这个业务模式报数据
 中介的业务，就是撮合一笔交易成功，即需要钱的一方拿到钱开始，投钱的一方收回钱结束。
"""

import datetime
from utils import mysql_utils as mu
from constant import common_constants as cc


def get_loan_to_return_project_by_time(end_time):
    """真实的、未还清投资人的标的"""
    sql = '''select
                distinct p.project_no
            from sp_invest_project p, sp_investing_return ir, sp_investing i
            WHERE i.project_no = p.project_no and i.trans_id = ir.invest_trans_id
            AND p.project_no NOT IN (SELECT project_no FROM sp_project_tag where tag=0)
            AND p.project_type IN (0,4,5)
            AND p.status in (3,4)
            AND ir.created_on < '%s'
            AND (ir.real_return_time >= '%s' or ir.real_return_time is null) '''
    sql = sql % (end_time, end_time)
    result = mu.get_result_by_sql(sql)
    return result[0][0]


def get_loan_to_return_project_avg_period_by_weight_and_end_time(end_time, weight='amount'):
    """真实的、未还项目平均融资期限，单位：天"""
    if weight == 'arithmetic':
        avg_period = 'avg(datediff(p.repay_end_time,p.repay_start_time))'
    else:
        avg_period = 'sum(datediff(p.repay_end_time,p.repay_start_time)*p.total_amount)/sum(p.total_amount)'
    sql = '''select ''' + avg_period + '''
            from sp_invest_project p,
            (
                select
                    distinct p.project_no
                from sp_invest_project p, sp_investing_return ir, sp_investing i
                WHERE i.project_no = p.project_no and i.trans_id = ir.invest_trans_id
                AND p.project_no NOT IN (SELECT project_no FROM sp_project_tag where tag=0)
                AND p.project_type IN (0,4,5)
                AND p.status in (3,4)
                AND ir.created_on < '%s'
                AND (ir.real_return_time >= '%s' or ir.real_return_time is null))
            loan_to_return_project
            where loan_to_return_project.project_no = p.project_no '''
    sql = sql % (end_time, end_time)
    result = mu.get_result_by_sql(sql)
    return result[0][0]


def get_avg_loan_to_return_amt_by_user_type(end_time, user_type):
    """未还标的的、自然人/法人的平均在贷金额, 单位：万元"""
    sql = '''select sum(p.total_amount)/count(distinct i.creditor_enterprise_id)/10000
            from sp_invest_project p, sp_project_info i, sp_enterprise_info e, sp_user u,
            (
                select
                    distinct p.project_no
                from sp_invest_project p, sp_investing_return ir, sp_investing i
                WHERE i.project_no = p.project_no and i.trans_id = ir.invest_trans_id
                AND p.project_no NOT IN (SELECT project_no FROM sp_project_tag where tag=0)
                AND p.project_type IN (0,4,5)
                AND p.status in (3,4)
                AND ir.created_on < '%s'
                AND (ir.real_return_time >= '%s' or ir.real_return_time is null))
            loan_to_return_project
            where loan_to_return_project.project_no = p.project_no
                and i.project_no = p.project_no and e.id = i.creditor_enterprise_id
                and u.id = e.user_id '''
    sql = sql % (end_time, end_time)
    if cc.PERSONAL == user_type:
        sql += ' and u.type = 0'
    elif cc.MERCHANT == user_type:
        sql += ' and u.type = 1'
    result = mu.get_result_by_sql(sql)
    return result[0][0]


def get_loan_to_return_project_avg_interest_rate_based_on_loan_amt(end_time):
    """在投标的的平均借款利率, 没有还给投资人的标的的平均借款利率"""
    sql = '''select sum(r.interest_amt)/sum(r.capital_amt)*100
            from sp_loan_return r,(
                select
                    distinct p.project_no
                from sp_invest_project p, sp_investing_return ir, sp_investing i
                WHERE i.project_no = p.project_no and i.trans_id = ir.invest_trans_id
                AND p.project_no NOT IN (SELECT project_no FROM sp_project_tag where tag=0)
                AND p.project_type IN (0,4,5)
                AND p.status in (3,4)
                AND ir.created_on < '%s'
                AND (ir.real_return_time >= '%s' or ir.real_return_time is null)
                )
                a
            where a.project_no=r.project_no'''
    sql = sql % (end_time, end_time)
    result = mu.get_result_by_sql(sql)
    return result[0][0]


def get_loan_to_return_project_avg_total_rate_based_on_loan_amt(end_time):
    """在投标的的平均借款总利率, 包括了利息、管理费和登记费"""
    sql = '''select 100*sum(lp.interest_amt+lp.manage_fee_amt+lp.register_fee_amt)/sum(lp.amt+lp.interest_amt+lp.manage_fee_amt+lp.register_fee_amt)
            from
                (select
                    distinct p.project_no
                from sp_invest_project p, sp_investing_return ir, sp_investing i
                WHERE i.project_no = p.project_no and i.trans_id = ir.invest_trans_id
                AND p.project_no NOT IN (SELECT project_no FROM sp_project_tag where tag=0)
                AND p.project_type IN (0,4,5)
                AND p.status in (3,4)
                AND ir.created_on < '%s'
                AND (ir.real_return_time >= '%s' or ir.real_return_time is null)) p,
                sp_loan_pay lp
            where lp.project_no = p.project_no '''
    sql = sql % (end_time, end_time)
    result = mu.get_result_by_sql(sql)
    return result[0][0]


def get_loaning_user_num_by_user_type(end_time, user_type):
    sql = '''select
                count(distinct pi.creditor_enterprise_id) as num
            from  sp_project_info pi, sp_user u, sp_enterprise_info e,
                (select
                    distinct p.project_no
                from sp_invest_project p, sp_investing_return ir, sp_investing i
                WHERE i.project_no = p.project_no and i.trans_id = ir.invest_trans_id
                AND p.project_no NOT IN (SELECT project_no FROM sp_project_tag where tag=0)
                AND p.project_type IN (0,4,5)
                AND p.status in (3,4)
                AND ir.created_on < '%s'
                AND (ir.real_return_time >= '%s' or ir.real_return_time is null)) p
            where pi.project_no = p.project_no
            and u.id = e.user_id and e.id = pi.creditor_enterprise_id '''
    if cc.PERSONAL == user_type:
        sql += ' AND u.type = 0'
    elif cc.MERCHANT == user_type:
        sql += ' AND u.type = 1'
    sql = sql % (end_time, end_time)
    result = mu.get_result_by_sql(sql)
    return result[0][0]


def get_loan_to_return_user_list(end_time, size=1):
    sql = '''select
                pi.creditor_enterprise_id,
                sum(ip.total_amount) as loan_to_return_amt
            from  sp_project_info pi, sp_user u, sp_enterprise_info e, sp_invest_project ip,
                (select
                    distinct p.project_no
                from sp_invest_project p, sp_investing_return ir, sp_investing i
                WHERE i.project_no = p.project_no and i.trans_id = ir.invest_trans_id
                AND p.project_no NOT IN (SELECT project_no FROM sp_project_tag where tag=0)
                AND p.project_type IN (0,4,5)
                AND p.status in (3,4)
                AND ir.created_on < '%s'
                AND (ir.real_return_time >= '%s' or ir.real_return_time is null)) p
            where pi.project_no = p.project_no
            and u.id = e.user_id and e.id = pi.creditor_enterprise_id and ip.project_no = p.project_no
            group by pi.creditor_enterprise_id
            order by loan_to_return_amt desc
            limit %d '''
    sql %= (end_time, end_time, size)
    result = mu.get_result_by_sql(sql)
    return result


def get_loan_to_return_project_num(end_time):
    sql = '''select
                    count(distinct p.project_no)
                from sp_invest_project p, sp_investing_return ir, sp_investing i
                WHERE i.project_no = p.project_no and i.trans_id = ir.invest_trans_id
                AND p.project_no NOT IN (SELECT project_no FROM sp_project_tag where tag=0)
                AND p.project_type IN (0,4,5)
                AND p.status in (3,4)
                AND ir.created_on < '%s'
                AND (ir.real_return_time >= '%s' or ir.real_return_time is null)'''
    sql %= (end_time, end_time)
    result = mu.get_result_by_sql(sql)
    return result[0][0]


def get_loan_to_return_detail_with_association(end_time):
    """关联关系企业借款余额笔数、金额"""
    sql = '''select
                    count(distinct p.project_no), sum(ir.capital_amt)
                from sp_invest_project p, sp_investing_return ir, sp_investing i,
                    sp_project_info pi
                WHERE i.project_no = p.project_no and i.trans_id = ir.invest_trans_id
                AND pi.project_no = p.project_no
                AND pi.core_enterprise_id = 205
                AND p.project_no NOT IN (SELECT project_no FROM sp_project_tag where tag=0)
                AND p.project_type IN (0,4,5)
                AND p.status in (3,4)
                AND ir.created_on < '%s'
                AND (ir.real_return_time >= '%s' or ir.real_return_time is null)'''
    sql %= (end_time, end_time)
    results = mu.get_result_by_sql(sql)
    return results


if __name__ == '__main__':
    end_time = datetime.date.today()
    # get_loan_to_return_project_avg_period_by_weight_and_end_time(end_time, 'arithmetic')
    # get_loan_to_return_project_avg_total_rate_based_on_loan_amt(end_time)
    # print get_loaning_user_num_by_user_type(end_time, cc.PERSONAL), get_loaning_user_num_by_user_type(end_time, cc.MERCHANT)
    # results = get_loan_to_return_user_list(end_time, 10)
    # for result in results:
    #     print result
    # end_time = datetime.date.today()
    # result = get_loan_to_return_project_num(end_time)
    # print result
    result = get_loan_to_return_project_by_time(end_time)
    print(result)