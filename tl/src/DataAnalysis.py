from sys import path
path.append('../../')
from tl.src.user_loan_feature import get_user_loan_feature
from tl.src.order_loan_feature import get_order_loan
from tl.src.click_feature import get_click_feature
from tl.src.loan_feature import get_loan_feature
from tl.src.order_feature import get_order_feature
from tl.src.user_feature import get_user_feature
from tl.src.util import *

root_dir, train_url, feature_url = get_url()
loan, user, order, click = read_data()

# 转换金额
loan['loan_amount'] = change_loan(loan['loan_amount'])
order['price'] = change_loan(order['price'])
order['discount'] = change_loan(order['discount'])

uid = pd.DataFrame(user["uid"])

for start_month in [8]:
    MONTH = start_month + 2
    NUM = 3

    feature_loan = get_loan_feature(start_month, MONTH, NUM, uid, loan)
    user_m = get_user_feature(start_month, MONTH, user, feature_url, save=0)
    # feature = get_order_feature(start_month, MONTH, NUM, order, uid)
    feature = pd.DataFrame(
        pd.read_csv(feature_url + 'order_feature_start_' + str(start_month) + '_end_' + str(MONTH) + '.csv'))

    order_loan = get_order_loan(order, loan, uid, start_month, MONTH, NUM)
    user_loan = get_user_loan_feature(user, loan, start_month, MONTH)
    # feature_click = get_click_feature(start_month, MONTH, click)
    feature_click = pd.DataFrame(
        pd.read_csv(feature_url + 'click_feature_start_' + str(start_month) + '_end_' + str(MONTH) + '.csv'))

    feature = pd.merge(feature, feature_loan, on=["uid"], how="left")
    feature = pd.merge(feature, user_m, on=["uid"], how="left")
    feature = pd.merge(feature, feature_click, on=["uid"], how="left")
    feature = pd.merge(feature, order_loan, on=["uid"], how="left")
    feature = pd.merge(feature, user_loan, on=["uid"], how="left")

    # 处理异常值
    feature = handle_na(feature)

    # 保存特征数据
    feature.to_csv(feature_url + "train_x_offline_start_" + str(start_month) + "_end_" + str(MONTH) + ".csv",
                   index=False)
