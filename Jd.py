from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 导入鼠标操作
from selenium.webdriver.common.keys import Keys  # 导入键值操作
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# myusername = '13783465025'  # 京东账号
# mypassword = 'woainiawoainia2017'  # 京东密码
SIGN_PAGE = 'https://passport.jd.com/new/login.aspx'  # 登录页面


# 初始化工作
def init_browser():
    chrome360_options = Options()
    chrome360_options.binary_location = r"C:\\Users\\haijun.wang\\AppData\\Roaming\\360se6\\Application\\360se.exe"
    return webdriver.Chrome(chrome_options=chrome360_options)


# 登录并跳转到待评价页面
def jump_to_comment(driver):
    # 登录
    driver.get(SIGN_PAGE)
    try:
        # 登录操作
        # jumplogin = driver.find_element_by_link_text("账户登录")
        # loginname = driver.find_element_by_id("loginname")
        # password = driver.find_element_by_id("nloginpwd")
        # submit = driver.find_element_by_id("loginsubmit")
        # jumplogin.click()  # 点击切换账号登录
        # loginname.send_keys(myusername)
        # password.send_keys(mypassword)
        # submit.click()  # 点击登录按钮
        time.sleep(10)
        print("登录成功")

        # 跳转到我的订单
        current_window = browser.current_window_handle  # 定位当前页
        all_windows = driver.window_handles
        for window in all_windows:
            if window != current_window:
                driver.switch_to.window(window)
        current_window = driver.current_window_handle
        myorders = driver.find_element_by_link_text("我的订单")
        myorders.click()
        print("我的订单")
        time.sleep(1)

        # 跳转到待评价订单
        all_windows = driver.window_handles
        for window in all_windows:
            if window != current_window:
                driver.switch_to.window(window)
        current_window = driver.current_window_handle
        tocomments = driver.find_element_by_link_text("待评价")
        tocomments.click()
        print("待评价")
        time.sleep(1)
    except:
        print("获取待评价列表失败!")


# 执行评价，完成后关闭标签页
def comment_close_tab(driver, order):
    print("---->>去评论：" + order.get_attribute("href"))
    order.click()
    '''开始自动评价'''
    current_window = browser.current_window_handle  # 定位当前页
    all_windows = driver.window_handles
    for window in all_windows:
        if window != current_window:
            driver.switch_to.window(window)
    current_window = driver.current_window_handle

    # 打5星
    activity = driver.find_element_by_css_selector("#activityVoucher")
    stars = activity.find_elements_by_css_selector(".item > .commstar > .star.star5")
    for s in stars:
        ActionChains(driver).move_to_element_with_offset(s, 70, 0).click().perform()

    # 商品评分
    try:
        level = driver.find_element_by_css_selector(".fop-main > .commstar > .star.star5")
        if level:
            ActionChains(driver).move_to_element_with_offset(level, 70, 0).click().perform()
    except:
        print("---->>无商品评分")

    # 买家印象
    try:
        sign = driver.find_elements_by_css_selector(
            ".fop-item.J-mjyx > .fop-main > .m-tagbox.m-multi-tag > .tag-item")
        if sign and sign[0]:
            sign[0].click()
    except:
        print("---->>无买家印象")

    # 评价内容
    try:
        text = driver.find_element_by_css_selector(".fop-main > .f-textarea > textarea")
        if text:
            text.send_keys(u'我为什么喜欢在京东买东西，因为今天买明天就可以送到。我为什么每个商品的评价都一样，'\
                           u'因为在京东买的东西太多太多了，导致积累了很多未评价的订单，所以我统一用段话作为评价内容。京东购物这么久，有买到很好的产品！')
            time.sleep(1)
    except:
        print("---->>无评价内容")

    # 发表评价
    submit_btn = driver.find_element_by_link_text("发表")
    submit_btn.click()
    print("---->>评价完成")
    time.sleep(1)

    # 关闭标签页
    driver.close()
    '''结束自动评价'''


# 订单评价
def order_comment(browser):
    jump_to_comment(browser)
    current_window = browser.current_window_handle

    all_windows = browser.window_handles
    for window in all_windows:
        if window != current_window:
            browser.switch_to.window(window)
    current_window = browser.current_window_handle

    print("------------开始执行订单评价-------------")
    while True:
        comment_list = browser.find_elements_by_css_selector(".operate > a.btn-def")
        if len(comment_list) == 0:
            break

        print("-->>共：" + str(len(comment_list)) + "个待评价订单")
        for comm in comment_list:
            comment_close_tab(browser, comm)
            time.sleep(2)
            # 刷新待评价页面
            all_windows = browser.window_handles
            if len(all_windows) == 3:
                browser.switch_to.window(all_windows[2])
                browser.refresh()
                time.sleep(2)
            break
    print("------------结束执行订单评价-------------")

    browser.implicitly_wait(10)
    return browser


# 订单追评
def chase_order_comment(browser):
    print("------------开始执行订单追评价-------------")
    # 获取页面'待追评'标签,并点击
    chase_list = browser.find_element_by_link_text("待追评")
    chase_list.click()
    time.sleep(1)

    # 获取所有[追评]按钮
    while True:
        print('find all chase list')
        btn_list = browser.find_elements_by_css_selector(".operate > a.btn-def")
        if len(btn_list) == 0:
            break
        print("待追评:"+str(len(btn_list))+"个")
        for index, btn in enumerate(btn_list):
            btn.click()
            time.sleep(1)

            current_window = browser.current_window_handle
            all_windows = browser.window_handles
            for window in all_windows:
                if window != current_window:
                    browser.switch_to.window(window)

            try:
                text = browser.find_element_by_css_selector(".fop-item > .f-textarea > textarea")
                if text:
                    text.send_keys(u'当大家看到我的这一篇评价时，表示我对产品是认可的，尽管我此刻的评论是复制黏贴的。'\
                                   u'这一方面是为了肯定商家的服务，另一方面是为了节省自己的时间。')
            except:
                print("---->>无评价内容")

            # 发表追评并关闭标签页
            submit_btn = browser.find_element_by_link_text("发表")
            submit_btn.click()
            print("---->>追评完成("+str(index)+")")
            time.sleep(1)
            browser.close()

            # 切换到我的评价window
            all_windows = browser.window_handles
            if len(all_windows) == 3:
                browser.switch_to.window(all_windows[2])
        time.sleep(1)
        browser.refresh()
        time.sleep(1)


if __name__ == '__main__':
    browser = init_browser()
    browser = order_comment(browser)
    chase_order_comment(browser)
    # try:
    #
    # except:
    #     print("失败")
    # finally:
    #     # 退出驱动
    #     # browser.quit()
    #     print("xxxxx")
