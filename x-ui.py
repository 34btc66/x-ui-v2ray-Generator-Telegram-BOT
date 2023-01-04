#!/usr/bin/python3
import os
from configparser import ConfigParser
import pytz
import time
import requests
from persiantools.jdatetime import JalaliDateTime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import base64
import telebot
import json
import re
from telebot import types
from telebot.types import ReplyKeyboardRemove
import pathlib
import qrcode
import datetime
global files_path
files_path = str(pathlib.Path(__file__).resolve().parent) + "/"
def load_config():
    global API, TimeLocation, \
        Bot_Admin_Passwd, XUI_User, XUI_Pass, SSLcertname, SSLkeyname, \
        trojan_domain, trojan_xui_port, server_json, user_ban, bot_commands_list, users_id
    config_path = str(pathlib.Path(__file__).resolve().parent) + "/config.ini"
    config = ConfigParser()
    config.read(config_path)
    API = config.get("XUI_BOT", 'api')
    TimeLocation = config.get("XUI_BOT", 'timelocation')
    Bot_Admin_Passwd = config.get("XUI_BOT", 'bot_admin_passwd')
    XUI_User = config.get("XUI_BOT", 'xui_user')
    XUI_Pass = config.get("XUI_BOT", 'xui_pass')
    SSLcertname = config.get("XUI_BOT", 'sslcertname')
    SSLkeyname = config.get("XUI_BOT", 'sslkeyname')
    trojan_domain = config.get("XUI_BOT", 'trojan_domain')
    trojan_xui_port = config.get("XUI_BOT", 'trojan_xui_port')
    server_json = json.loads(config.get("XUI_BOT", 'server_json'))
    user_ban = config.get("XUI_BOT", 'user_ban')
    users_id = config.get("XUI_BOT", 'users_id')
    bot_commands_list = config.get("XUI_BOT", 'bot_commands_list')
def update_config(system, value):
    config_path = str(pathlib.Path(__file__).resolve().parent) + "/config.ini"
    config = ConfigParser()
    config.read(config_path)
    cfgfile = open(config_path, 'w')
    config.set("XUI_BOT", system, value)
    config.write(cfgfile)
    cfgfile.close()
    load_config()
load_config()

API_TOKEN = API
bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')
print("Bot running ...")
server = {key.lower():value.lower() for key, value in server_json.items()}
adminpass = Bot_Admin_Passwd
current_time = JalaliDateTime.now(pytz.timezone(TimeLocation)).strftime("%Y/%m/%d  -  %H:%M:%S")
vmesscmdd = []
vlesscmdd = []
for key in server_json.keys():
    vmesskey = str(key).lower() + '_vmess'
    vlesskey = str(key).lower() + '_vless'
    vmesscmdd.append(vmesskey)
    vlesscmdd.append(vlesskey)

# def restartApp():
# python = sys.executable
# os.execl(python, python, *sys.argv)

def Get_Ban_list():
    text = user_ban.replace('[','').replace(']','').replace("', '",' ').replace("'",'')
    #print(text)
    li = list(text.split(" "))
    return li

def restartAPP():
    os.system(f'sh {files_path}reset.sh')

def append_new_user(logwrite):
    file_name = f'{files_path}userslog.txt'
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(logwrite)

def bancheck(user):
    get_new_Ban = user_ban.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '')
    checklist = list(get_new_Ban.split(" "))
    x = []
    x.append(user)
    matches = str(set(checklist).intersection(set(x))).replace("', '", '').replace("{", "").replace("}", "").replace(
        "'", "")
    if matches == "set()":
        return False
    else:
        return True
        #print("Found")

def get_command_list():
    commands = bot.get_my_commands()
    cmd_list = []
    for command in commands:
        cmd_list.append(str(command))
    update_config('bot_commands_list', str(cmd_list))
    new_cmd_list = bot_commands_list.replace('"', '').replace("'", '"')
    update_config('bot_commands_list', new_cmd_list)

def SET_command_list():
    #Generate Commands Base server_json elements :
    location_name = """[
                            {"name": "Australia", "code": "AU"},
                            {"name": "Austria", "code": "AT"},
                            {"name": "Belarus", "code": "BY"},
                            {"name": "Belgium", "code": "BE"},
                            {"name": "Brazil", "code": "BR"},
                            {"name": "Canada", "code": "CA"},
                            {"name": "China", "code": "CN"},
                            {"name": "Cyprus", "code": "CY"},
                            {"name": "Czech Republic", "code": "CZ"},
                            {"name": "Denmark", "code": "DK"},
                            {"name": "Estonia", "code": "EE"},
                            {"name": "Finland", "code": "FI"},
                            {"name": "France", "code": "FR"},
                            {"name": "Georgia", "code": "GE"},
                            {"name": "Germany", "code": "DE"},
                            {"name": "Greece", "code": "GR"},
                            {"name": "Hong Kong", "code": "HK"},
                            {"name": "Hungary", "code": "HU"},
                            {"name": "Iceland", "code": "IS"},
                            {"name": "India", "code": "IN"},
                            {"name": "Indonesia", "code": "ID"},
                            {"name": "Iran, Islamic Republic Of", "code": "IR"},
                            {"name": "Ireland", "code": "IE"},
                            {"name": "Israel", "code": "IL"},
                            {"name": "Italy", "code": "IT"},
                            {"name": "Japan", "code": "JP"},
                            {"name": "Korea, Republic of", "code": "KR"},
                            {"name": "Kuwait", "code": "KW"},
                            {"name": "Lithuania", "code": "LT"},
                            {"name": "Luxembourg", "code": "LU"},
                            {"name": "Malaysia", "code": "MY"},
                            {"name": "Maldives", "code": "MV"},
                            {"name": "Mexico", "code": "MX"},
                            {"name": "Monaco", "code": "MC"},
                            {"name": "Netherlands", "code": "NL"},
                            {"name": "New Zealand", "code": "NZ"},
                            {"name": "Norway", "code": "NO"},
                            {"name": "Poland", "code": "PL"},
                            {"name": "Portugal", "code": "PT"},
                            {"name": "Romania", "code": "RO"},
                            {"name": "Russian Federation", "code": "RU"},
                            {"name": "Singapore", "code": "SG"},
                            {"name": "Slovakia", "code": "SK"},
                            {"name": "Slovenia", "code": "SI"},
                            {"name": "Spain", "code": "ES"},
                            {"name": "Sweden", "code": "SE"},
                            {"name": "Switzerland", "code": "CH"},
                            {"name": "Taiwan", "code": "TW"},
                            {"name": "Turkey", "code": "TR"},
                            {"name": "Turkmenistan", "code": "TM"},
                            {"name": "Ukraine", "code": "UA"},
                            {"name": "United Arab Emirates", "code": "AE"},
                            {"name": "United Kingdom", "code": "GB"},
                            {"name": "United States", "code": "US"}
                        ]"""
    location_json = json.loads(location_name)
    deslist_vmess = []
    deslist_vless = []
    for cname in server_json.keys():
        cname_2word = str(cname[1:3]).lower()
        for item in location_json:
            if cname_2word == str(item['code']).lower():
                ds_vmess = '''{"command": "''' + str(
                    cname[1:]).lower() + "_vmess" + '''", "description": "Location : ''' + item[
                               'name'] + ''' (VMESS)"}'''
                ds_vless = '''{"command": "''' + str(
                    cname[1:]).lower() + "_vless" + '''", "description": "Location : ''' + item[
                               'name'] + ''' (VLESS)"}'''
                deslist_vmess.append(ds_vmess)
                deslist_vless.append(ds_vless)
    finall = [x for y in zip(deslist_vmess, deslist_vless) for x in y]
    finall.append('{"command":"trojan", "description":"Location : United Kingdom (Trojan)"}')
    finall.append('{"command":"don", "description":"Donations"}')
    finall.append('{"command":"app", "description":"Download Apps"}')
    finall.append('{"command":"set", "description":"Bot Setup"}')
    finalsetcommand = str(finall).replace("'", "")
    update_config('bot_commands_list', finalsetcommand)
    # Set Telegram Commands Base bot_commands_list elements :
    new_cmd_list = bot_commands_list
    update_config('bot_commands_list', str(new_cmd_list))
    json_object = json.loads(bot_commands_list)
    l = []
    for item in json_object:
        l.extend([telebot.types.BotCommand(f"{item['command']}", f"{item['description']}")])
    bot.set_my_commands(l)

@bot.message_handler(commands=['install'])
def install_bot(message):
    global msginstall
    msginstall = bot.send_message(message.chat.id, "Please Enter Admin Password : ")
    bot.register_next_step_handler(msginstall, checkpassinstall)
def checkpassinstall(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        if message.text == adminpass:
            bot.send_message(message.chat.id,
                             f"Current ADMIN PASS IS : {Bot_Admin_Passwd}\n\nDo You Want To Change it ?\nEnter y for change pass and n for no change :")
            bot.register_next_step_handler(msginstall, step0_changepass)
        else:
            bot.send_message(message.chat.id,
                             "❌ The Password is incorrect\n\nPlease Enter correct password again :\n\n<b>(for exit enter ex)</b>")
            if message.text in ("ex", "EX", "Ex"):
                bot.send_message(message.chat.id, f"✅ Exit Success.")
            else:
                bot.register_next_step_handler(msginstall, checkpassinstall)

def step0_changepass(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        if message.text in ["y", "Y", "Yes", "yes", "YES"]:
            bot.send_message(message.chat.id, f"Please enter the new password : ")
            bot.register_next_step_handler(msginstall, step1_changepass)
        else:
            bot.send_message(message.chat.id, f"[STEP 1] >> Please enter new server settings : ")
            r = json.dumps(server_json, indent=2)
            bot.send_message(message.chat.id,
                             f"The Currect Server Settings is : \n\n<code>{r}</code>\n\n🆕 Please Enter The new Servers or <b>(for cancel this proccess type : ex)</b>",
                             parse_mode='HTML')
            bot.register_next_step_handler(msginstall, step1)

def step1_changepass(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        update_config('bot_admin_passwd', str(message.text))
        bot.send_message(message.chat.id, f"✅ ADMIN Panel password {message.text} Saved .")
        r = json.dumps(server_json, indent=2)
        bot.send_message(message.chat.id,
                         f"The Currect Server.json Settings is : \n\n<code>{r}</code>\n\n🆕 Please Enter The new Servers or <b>(for cancel this proccess type : ex)</b>",
                         parse_mode='HTML')
        bot.send_message(message.chat.id, f"[STEP 1] >> Please enter new server settings : ")
        bot.register_next_step_handler(msginstall, step1)

def step1(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        srvjson = f'''{str(message.text)}'''
        update_config("server_json", srvjson.replace("'", '"'))
        SET_command_list()
        bot.send_message(message.chat.id, "<b>✅ the new Server config saved successfully.\n\n✅ the Telegram Commands update successfully.</b>", parse_mode='HTML')
        bot.send_message(message.chat.id, f"[STEP 2] >> Please enter xui username panel : ")
        bot.register_next_step_handler(msginstall, step2)
def step2(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        update_config('xui_user', str(message.text))
        bot.send_message(message.chat.id, f"✅ XUI Username {message.text} Saved .")
        bot.send_message(message.chat.id, f"[STEP 3] >> Please enter xui password panel : ")
        bot.register_next_step_handler(msginstall, step3)

def step3(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        update_config('xui_pass', str(message.text))
        bot.send_message(message.chat.id, f"✅ XUI Password {message.text} Saved .")
        bot.send_message(message.chat.id, f"[STEP 4] >> Please enter trojan domain url : \nsample : example.com")
        bot.register_next_step_handler(msginstall, step4)

def step4(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        update_config('trojan_domain', str(message.text))
        bot.send_message(message.chat.id, f"✅ Trojan Domain Url {message.text} Saved .")
        bot.send_message(message.chat.id, f"[STEP 5] >> Please enter trojan port xui panel : \nsample : 54321")
        bot.register_next_step_handler(msginstall, step5)

def step5(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        update_config('trojan_xui_port', str(message.text))
        bot.send_message(message.chat.id, f"✅ Trojan Port XUI Panel {message.text} Saved .")
        bot.send_message(message.chat.id, f"[STEP 6] >> Please enter ssl cert name address : \nsample : /root/cert.crt")
        bot.register_next_step_handler(msginstall, step6)

def step6(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        update_config('sslcertname', str(message.text))
        bot.send_message(message.chat.id, f"✅ SSL Cert Name Address {message.text} Saved .")
        bot.send_message(message.chat.id,
                         f"[STEP 7] >> Please enter ssl key name address : \nsample : /root/private.key")
        bot.register_next_step_handler(msginstall, step7)

def step7(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        update_config('sslkeyname', str(message.text))
        bot.send_message(message.chat.id, f"✅ SSL Cert Key Address {message.text} Saved .")
        bot.send_message(message.chat.id,
                         f"[STEP 8] >> Please enter time location : \nsample : Asia/Tehran , Europe/Istanbul")
        bot.register_next_step_handler(msginstall, step8)

def step8(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        update_config('timelocation', str(message.text))
        bot.send_message(message.chat.id, f"✅ Time Location {message.text} Saved .")
        bot.send_message(message.chat.id, f"✅✅✅ Congradulation! , You Almost Done. Bot Restart Now ...")
        bot.send_message(message.chat.id, "<b>✅ Restart Done Successfully.</b>", parse_mode='HTML')
        restartAPP()

@bot.message_handler(commands=['restart'])
def reset_bot(message):
    bot.send_message(message.chat.id, "<b>✅ Restart Done Successfully.</b>", parse_mode='HTML')
    restartAPP()

@bot.message_handler(commands=['loguser'])
def log_user(message):
    # file = open(f'{files_path}userslog.txt', 'rb')
    # listfile = file.read()
    # listtext = f"{listfile}"
    usr_doc = open(f'{files_path}userslog.txt', 'rb')
    bot.send_document(message.chat.id, usr_doc)
    # bot.send_message(message.chat.id,f"{(listtext)}",parse_mode='HTML')
    # file.close()
    usr_doc.close()

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
    usrs_ids_list = list(usrs_ids.split(" "))
    while ("" in usrs_ids_list):
        usrs_ids_list.remove("")
    if message.from_user.id not in usrs_ids_list:
        usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
        usrs_ids_list = list(usrs_ids.split(" "))
        while ("" in usrs_ids_list):
            usrs_ids_list.remove("")
        usrs_ids_list.append(str(message.from_user.id))
        final_new_id = list(dict.fromkeys(usrs_ids_list))
        update_config('users_id', str(final_new_id))

    ch = bancheck(message.from_user.username)
    if ch == False:
        bot.send_message(message.chat.id, """\
برای ساخت v2ray مورد نظر از بخش Menu لوکیشن و نوع اتصال را انتخاب کنید

اگر میخواهید برای گسترش اینترنت ازاد کمکی بکنید برای اطلاعات بیشتر از بخش Menu گزینه Donation /don را انتخاب کنید 

📥 برای دانلود اپ و راهنمای اتصال ازین گزینه استفاده کنید ( /app )
\
""")
    else:
        bot.reply_to(message, 'دسترسی شما به علت اسپم و استفاده بیش از حد مجاز در این ربات مسدود شده است')

@bot.message_handler(commands=['msgall'])
def send_message_users(message):
    load_config()
    msg_text = str(message.text)[8:]
    usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
    usrs_ids_list = list(usrs_ids.split(" "))
    for chat in usrs_ids_list:
        bot.send_message(chat_id=chat, text=str(msg_text))

@bot.message_handler(commands=['msgid'])
def get_user_id(message):
    msgbotid = bot.send_message(chat_id=message.chat.id, text="یوزر ای دی را وارد کنید")

    bot.register_next_step_handler(msgbotid, send_message_users)
def send_message_users(message):
    global usid
    usid = message.text
    msgbotid2 = bot.send_message(chat_id=message.chat.id, text="پیام را وارد کنید")
    bot.register_next_step_handler(msgbotid2, success_message_users)
def success_message_users(message):
    global usidTEXT
    usidTEXT = message.text
    try:
        bot.send_message(chat_id=usid, text=str(usidTEXT))
        bot.send_message(chat_id=message.chat.id, text="✅ پیام با موفقیت ارسال شد")
    except:
        bot.send_message(chat_id=message.chat.id, text="❌ یوزر نادرست است")



@bot.message_handler(commands=['showusersid'])
def show_users_id(message):
    load_config()
    usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
    usrs_ids_list = list(usrs_ids.split(" "))
    bot.send_message(chat_id=message.chat.id, text=str(len(usrs_ids_list)))
    bot.send_message(chat_id=message.chat.id, text=str(users_id))

@bot.message_handler(func=lambda message: message.text in vmesscmdd)
def create_vmess(message):
    usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
    usrs_ids_list = list(usrs_ids.split(" "))
    while ("" in usrs_ids_list):
        usrs_ids_list.remove("")
    if message.from_user.id not in usrs_ids_list:
        usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
        usrs_ids_list = list(usrs_ids.split(" "))
        while ("" in usrs_ids_list):
            usrs_ids_list.remove("")
        usrs_ids_list.append(str(message.from_user.id))
        final_new_id = list(dict.fromkeys(usrs_ids_list))
        update_config('users_id', str(final_new_id))

    ch = bancheck(message.from_user.username)
    if ch == False:
        bot.send_message(message.chat.id, "لطفا 10 ثانیه منتظر بمانید , در حال اماده سازی لینک vmess شما هستیم")
        sss = str(message.text)
        sname = str(sss.replace('_vmess', '')).lower()
        srv = server[sname]
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        browser.get(srv)
        print("Webdriver ready to work...")

        time.sleep(2)
        sent = bot.send_message(message.chat.id, "10 ثانیه ...")

        user = browser.find_element(By.XPATH,
                                    value="//*[@id='app']/main/div[2]/div/form/div[1]/div/div/span/span/input")
        user.clear()
        user.send_keys(XUI_User)

        passs = browser.find_element(By.XPATH,
                                     value="//*[@id='app']/main/div[2]/div/form/div[2]/div/div/span/span/input")
        passs.clear()
        passs.send_keys(XUI_Pass)

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='app']/main/div[2]/div/form/div[3]/div/div/span/button")
        button.click()
        browser.get(f'{srv}xui/inbounds')
        button = browser.find_element(By.XPATH, value="//*[@id='sider']/div/ul/li[2]")
        button.click()

        time.sleep(2)
        bot.edit_message_text("8 ثانیه ...", message.chat.id, sent.message_id)

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='content-layout']/main/div/div/div[2]/div[1]/div/div/div/button")
        button.click()
        time.sleep(2)
        # vmess name
        remark = browser.find_element(By.XPATH,
                                      value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[1]/div[1]/div[2]/div/span/input")
        remark.clear()
        # fname = message.from_user.first_name
        # lname = message.from_user.last_name
        if message.from_user.username == "":
            vmessname = message.from_user.id + "#" + sname.replace('/', '')
        else:
            vmessname = message.from_user.username + "#" + sname.replace('/', '')

        remark.send_keys(vmessname)
        time.sleep(2)
        bot.edit_message_text("6 ثانیه ...", message.chat.id, sent.message_id)
        # ipserver

        if srv == 'http://fc.nevergiveup.lol:2345/':
            ip = 'fc.nevergiveup.lol'
        else:
            ipg = re.findall(r'[0-9]+(?:\.[0-9]+){3}', srv)
            ip = str(ipg).replace('[', '').replace(']', '').replace('\'', '').replace('\"', '')

        # port
        portg = browser.find_element(By.XPATH,
                                     value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[1]/div[5]/div[2]/div/span/input")
        port = portg.get_attribute('value')
        # uid
        uidg = browser.find_element(By.XPATH,
                                    value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[2]/div[1]/div[2]/div/span/input")
        uid = uidg.get_attribute('value')

        # selectWS
        buttonws = browser.find_element(By.XPATH,
                                        value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[3]/div/div[2]/div/span/div")
        buttonws.click()

        buttonws.send_keys(Keys.ARROW_DOWN)
        buttonws.send_keys(Keys.ARROW_DOWN)
        buttonws.send_keys(Keys.ENTER)

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[3]/div/button[2]")
        button.click()
        time.sleep(2)
        bot.edit_message_text("4 ثانیه ...", message.chat.id, sent.message_id)
        vmess_json = {
            "v": "2",
            "ps": f'{vmessname}',
            "add": ip,
            "port": port,
            "id": uid,
            "aid": 0,
            "net": "ws",
            "type": "none",
            "host": "",
            "path": "/",
            "tls": "none"
        }
        #Create and send qr code :
        now = str(datetime.datetime.now()).replace("-", '').replace(" ", "").replace(".", "").replace(":", "")[4:]
        VmesURL = "vmess://" + base64.b64encode(json.dumps(vmess_json, sort_keys=True).encode('utf-8')).decode()
        image = qrcode.make(VmesURL)
        image.save(f"{files_path}{vmessname + now}vmess.png")
        print(VmesURL)
        time.sleep(2)
        bot.edit_message_text("2 ثانیه ...", message.chat.id, sent.message_id)
        browser.switch_to.window(browser.window_handles[0])

        browser.delete_all_cookies()
        browser.close()
        browser.quit()

        time.sleep(2)
        vmesCopy = f"<code>{VmesURL}</code>"
        #bot.edit_message_text(vmesCopy, message.chat.id, sent.message_id, parse_mode='HTML')
        bot.delete_message(message.chat.id, sent.message_id)
        bot.send_photo(message.chat.id, photo=open(f"{files_path}{vmessname + now}vmess.png", 'rb'), caption=vmesCopy)
        os.remove(f"{files_path}{vmessname + now}vmess.png")
        append_new_user(
            f"User : @{vmessname} \nID : {message.from_user.id}\nTime : {current_time}\nURL : <code>{VmesURL}</code>\n++++++++++++++++++++++")

    else:
        bot.reply_to(message, 'دسترسی شما به علت اسپم و استفاده بیش از حد مجاز در این ربات مسدود شده است')

@bot.message_handler(func=lambda message: message.text in vlesscmdd)
def create_vless(message):
    usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
    usrs_ids_list = list(usrs_ids.split(" "))
    while ("" in usrs_ids_list):
        usrs_ids_list.remove("")
    if message.from_user.id not in usrs_ids_list:
        usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
        usrs_ids_list = list(usrs_ids.split(" "))
        while ("" in usrs_ids_list):
            usrs_ids_list.remove("")
        usrs_ids_list.append(str(message.from_user.id))
        final_new_id = list(dict.fromkeys(usrs_ids_list))
        update_config('users_id', str(final_new_id))

    ch = bancheck(message.from_user.username)
    if ch == False:
        bot.send_message(message.chat.id, "لطفا 10 ثانیه منتظر بمانید , در حال اماده سازی لینک vless شما هستیم")
        sss = str(message.text)
        sname = sss.replace('_vless', '')
        srv = server[sname]
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        browser.get(srv)
        print("Webdriver ready to work...")

        time.sleep(2)
        sent = bot.send_message(message.chat.id, "10 ثانیه ...")

        user = browser.find_element(By.XPATH,
                                    value="//*[@id='app']/main/div[2]/div/form/div[1]/div/div/span/span/input")
        user.clear()
        user.send_keys(XUI_User)

        passs = browser.find_element(By.XPATH,
                                     value="//*[@id='app']/main/div[2]/div/form/div[2]/div/div/span/span/input")
        passs.clear()
        passs.send_keys(XUI_Pass)

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='app']/main/div[2]/div/form/div[3]/div/div/span/button")
        button.click()
        browser.get(f'{srv}xui/inbounds')
        button = browser.find_element(By.XPATH, value="//*[@id='sider']/div/ul/li[2]")
        button.click()

        time.sleep(2)
        bot.edit_message_text("8 ثانیه ...", message.chat.id, sent.message_id)

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='content-layout']/main/div/div/div[2]/div[1]/div/div/div/button")
        button.click()
        time.sleep(1)
        # vmess name
        remark = browser.find_element(By.XPATH,
                                      value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[1]/div[1]/div[2]/div/span/input")
        remark.clear()
        # fname = message.from_user.first_name
        # lname = message.from_user.last_name
        if message.from_user.username == "":
            vlessname = message.from_user.id + "%23" + sname.replace('/', '')
        else:
            vlessname = message.from_user.username + "%23" + sname.replace('/', '')

        remark.send_keys(vlessname)
        time.sleep(2)
        bot.edit_message_text("6 ثانیه ...", message.chat.id, sent.message_id)
        # Select Vless
        tg = browser.find_element(By.XPATH,
                                  value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[1]/div[3]/div[2]/div/span/div")
        tg.click()
        tg.send_keys(Keys.ARROW_DOWN)
        tg.send_keys(Keys.ENTER)
        # ipserver
        if srv == 'http://fc.nevergiveup.lol:2345/':
            ip = 'fc.nevergiveup.lol'
        else:
            ipg = re.findall(r'[0-9]+(?:\.[0-9]+){3}', srv)
            ip = str(ipg).replace('[', '').replace(']', '').replace('\'', '').replace('\"', '')
        # port
        portg = browser.find_element(By.XPATH,
                                     value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[1]/div[5]/div[2]/div/span/input")
        port = portg.get_attribute('value')
        # uid
        uidg = browser.find_element(By.XPATH,
                                    value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[2]/div[1]/div[2]/div/span/input")
        uid = uidg.get_attribute('value')

        # selectWS
        buttonws = browser.find_element(By.XPATH,
                                        value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[4]/div/div[2]/div/span/div")
        buttonws.click()
        buttonws.send_keys(Keys.ARROW_DOWN)
        buttonws.send_keys(Keys.ARROW_DOWN)
        buttonws.send_keys(Keys.ENTER)
        button = browser.find_element(By.XPATH,
                                      value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[3]/div/button[2]")
        button.click()
        time.sleep(2)
        bot.edit_message_text("4 ثانیه ...", message.chat.id, sent.message_id)
        vlessConfig = "vless://" + str(uid) + "@" + str(ip) + ":" + str(
            port) + "?type=ws&security=none&path=%2F#" + str(
            vlessname)
        now = str(datetime.datetime.now()).replace("-", '').replace(" ", "").replace(".", "").replace(":", "")[4:]
        image = qrcode.make(vlessConfig)
        image.save(f"{files_path}{vlessname + now}vless.png")
        time.sleep(2)
        bot.edit_message_text("2 ثانیه ...", message.chat.id, sent.message_id)
        browser.switch_to.window(browser.window_handles[0])
        browser.delete_all_cookies()
        browser.close()
        browser.quit()
        time.sleep(2)
        vlesCopy = f"<code>{vlessConfig}</code>"
        #bot.edit_message_text(vlesCopy, message.chat.id, sent.message_id, parse_mode='HTML')
        bot.delete_message(message.chat.id, sent.message_id)
        bot.send_photo(message.chat.id, photo=open(f"{files_path}{vlessname + now}vless.png", 'rb'), caption=vlesCopy)
        os.remove(f"{files_path}{vlessname + now}vless.png")
        append_new_user(
            f"User : @{vlessname} \nTime : {current_time}\nURL : <code>{vlessConfig}</code>\n++++++++++++++++++++++")

    else:
        bot.reply_to(message, 'دسترسی شما به علت اسپم و استفاده بیش از حد مجاز در این ربات مسدود شده است')

@bot.message_handler(commands=['don'])
def donation_alert(message):
    ch = bancheck(message.from_user.username)
    if ch == False:
        bot.send_message(message.chat.id, """
درصورت تمایل میتوانید مبلغی تتر جهت ارتقاع سرور ها اهدا کنید

USDT(TRC20) Wallet Address :

<code>TJDAmLNdzYmZAPrCURPPuC9z2RxD3v6jSB</code>
""", parse_mode='HTML')

    else:
        bot.reply_to(message, 'دسترسی شما به علت اسپم و استفاده بیش از حد مجاز در این ربات مسدود شده است')

@bot.message_handler(commands=['app'])
def download_app(message):
    ch = bancheck(message.from_user.username)
    if ch == False:
        bot.send_message(message.chat.id, """
<a href='https://play.google.com/store/apps/details?id=com.v2ray.ang&hl=en&gl=US'>Download Android App</a>

<a href='https://apps.apple.com/us/app/shadowlink-shadowsocks-tool/id1439686518'>Download IOS App</a>

<a href='https://github.com/v2fly/v2ray-core/releases/tag/v4.31.0'>Download WINDOWS App</a>

<b>مراحل استفاده و اضافه کردن سرور به فیلترشکن در گوشی‌های اندروید :</b>

1. ابتدا یکی از متن‌های درهم انگلیسی‌ای که قرار میدیم رو لمس کنید که کپی بشه
2. وارد برنامه‌ی V2rayNG بشید و روی علامت  +  کلیک کنین
3. گزینه import config from clipboard رو پیدا کنید و روش کلیک کنین
4. در انتهای سرورها یک سرور دیگه اضافه میشه بعد از انجام مرحله سوم.
5. روی سرور اضافه شده کلیک کرده و به فیلترشکن متصل بشید.

<b>مراحل استفاده و اضافه کردن سرور به فیلترشکن در گوشی‌های آیفون :</b>

1. ابتدا روی حروف انگلیسی درهم بزنید و لمس کنید
2. نرم افزار ShadowLink یا Fair VPN رو باز کنید
3. پایین سمت راست روی VPN بزنید
4. گزینه Add VPN by link رو لمس کنید
5. داخل کادر paste کنید
6. اوکی Ok رو بزنید و به سرور جدید متصل بشید
""", parse_mode='HTML')
    else:
        bot.reply_to(message, 'دسترسی شما به علت اسپم و استفاده بیش از حد مجاز در این ربات مسدود شده است')

@bot.message_handler(commands=['contact'])
def contact_us1(message):
    msgg = bot.send_message(message.chat.id, "☎️ برای تماس با ما لطفا پیام خود را وارد کنید :")
    bot.register_next_step_handler(msgg, contact_us2)
def contact_us2(message):
    bot.send_message(message.chat.id, "✅ پیام شما دریافت شد. با تشکر")
    file_name = f'{files_path}contact.txt'
    contact_message = f"User_Name : {message.from_user.username}\nUser_ID : {message.from_user.id}\nDate : {current_time}\nMessage : {message.text}\n+++++++++++++++++++++++++++++++++++++++"
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(contact_message)
@bot.message_handler(commands=['showcontact'])
def log_user(message):
    file = open(f'{files_path}contact.txt', 'rb')
    listfile = file.read()
    usr_doc = open(f'{files_path}contact.txt', 'rb')
    bot.send_document(message.chat.id, usr_doc)
    bot.send_message(message.chat.id, listfile, parse_mode='HTML')
    file.close()
    usr_doc.close()

@bot.message_handler(commands=['trojan'])
def create_trojan(message):
    usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
    usrs_ids_list = list(usrs_ids.split(" "))
    while ("" in usrs_ids_list):
        usrs_ids_list.remove("")
    if message.from_user.id not in usrs_ids_list:
        usrs_ids = users_id.replace('[', '').replace(']', '').replace("', '", ' ').replace("'", '').replace(",", '')
        usrs_ids_list = list(usrs_ids.split(" "))
        while ("" in usrs_ids_list):
            usrs_ids_list.remove("")
        usrs_ids_list.append(str(message.from_user.id))
        final_new_id = list(dict.fromkeys(usrs_ids_list))
        update_config('users_id', str(final_new_id))

    ch = bancheck(message.from_user.username)
    if ch == False:
        bot.send_message(message.chat.id, "لطفا 10 ثانیه منتظر بمانید , در حال اماده سازی لینک trojan شما هستیم")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        time.sleep(2)
        sent = bot.send_message(message.chat.id, "10 ثانیه ...")
        # sname = "/ca"
        # srv = server[sname]
        srv = f"http://{trojan_domain}:{trojan_xui_port}/"
        browser.get(srv)
        print("Webdriver ready to work...")

        user = browser.find_element(By.XPATH,
                                    value="//*[@id='app']/main/div[2]/div/form/div[1]/div/div/span/span/input")
        user.clear()
        user.send_keys(XUI_User)

        passs = browser.find_element(By.XPATH,
                                     value="//*[@id='app']/main/div[2]/div/form/div[2]/div/div/span/span/input")
        passs.clear()
        passs.send_keys(XUI_Pass)

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='app']/main/div[2]/div/form/div[3]/div/div/span/button")
        button.click()

        time.sleep(2)
        bot.edit_message_text("8 ثانیه ...", message.chat.id, sent.message_id)
        time.sleep(2)
        browser.get(f'{srv}xui/inbounds')
        button = browser.find_element(By.XPATH, value="//*[@id='sider']/div/ul/li[2]")
        button.click()

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='content-layout']/main/div/div/div[2]/div[1]/div/div/div/button")
        button.click()
        time.sleep(2)
        bot.edit_message_text("6 ثانیه ...", message.chat.id, sent.message_id)
        remark = browser.find_element(By.XPATH,
                                      value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[1]/div[1]/div[2]/div/span/input")
        remark.clear()
        if message.from_user.username == "":
            trjname = message.from_user.id + "Trojan"
        else:
            trjname = message.from_user.username + "Trojan"
        time.sleep(2)
        bot.edit_message_text("4 ثانیه ...", message.chat.id, sent.message_id)
        remark.send_keys(trjname)

        tg = browser.find_element(By.XPATH,
                                  value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[1]/div[3]/div[2]/div/span/div")
        tg.click()
        tg.send_keys(Keys.ARROW_DOWN)
        tg.send_keys(Keys.ARROW_DOWN)
        tg.send_keys(Keys.ENTER)

        xtls = browser.find_element(By.XPATH,
                                    value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[4]/div[2]/div[2]/div/span/button")
        xtls.click()

        dom = browser.find_element(By.XPATH,
                                   value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[5]/div[1]/div[2]/div/span/input")
        dom.clear()
        domname = trojan_domain
        dom.send_keys(domname)
        time.sleep(2)
        bot.edit_message_text("2 ثانیه ...", message.chat.id, sent.message_id)
        cert = browser.find_element(By.XPATH,
                                    value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[5]/div[3]/div[2]/div/span/input")
        cert.clear()
        certname = SSLcertname
        cert.send_keys(certname)

        key = browser.find_element(By.XPATH,
                                   value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[5]/div[4]/div[2]/div/span/input")
        key.clear()
        keyname = SSLkeyname
        key.send_keys(keyname)

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[3]/div/button[2]")
        button.click()

        # port
        portg = browser.find_element(By.XPATH,
                                     value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[1]/div[5]/div[2]/div/span/input")
        port = portg.get_attribute('value')
        # trans
        transq = browser.find_element(By.XPATH,
                                      value="//*[@id='inbound-modal']/div[2]/div/div[2]/div[2]/form[2]/div/div[2]/div/span/input")
        trans = transq.get_attribute('value')

        trojanURL = f"trojan://{trans}@{trojan_domain}:{port}#{trjname}"
        now = str(datetime.datetime.now()).replace("-", '').replace(" ", "").replace(".", "").replace(":", "")[4:]
        image = qrcode.make(trojanURL)
        image.save(f"{files_path}{trjname + now}Trojan.png")
        #bot.edit_message_text(f"<code>{trojanURL}</code>", message.chat.id, sent.message_id, parse_mode='HTML')
        bot.delete_message(message.chat.id, sent.message_id)
        bot.send_photo(message.chat.id, photo=open(f"{files_path}{trjname + now}Trojan.png", 'rb'), caption=f"<code>{trojanURL}</code>")
        os.remove(f"{files_path}{trjname + now}Trojan.png")
        append_new_user(f"User : @{trjname} \nTime : {current_time}\nURL : {trojanURL}\n++++++++++++++++++++++")
        print(trojanURL)
        browser.switch_to.window(browser.window_handles[0])
        # stop webdriver
        browser.delete_all_cookies()
        browser.close()
        browser.quit()
    else:
        bot.reply_to(message, 'دسترسی شما به علت اسپم و استفاده بیش از حد مجاز در این ربات مسدود شده است')

# def readJson():
# serverJson = server_json
# return serverJson

# def writeToserver(value):
# with open(f'{files_path}SetConfig.py', 'r') as fp:
# lines = fp.readlines()
# for row in lines:
# word = 'server_json'
# if row.find(word) != -1:
# with open(f"{files_path}SetConfig.py", "r+") as f:
# lines = f.readlines()
# del lines[lines.index(row)]
# f.seek(0)
# f.truncate()
# f.writelines(lines)
# with open(f"{files_path}SetConfig.py") as f:
# person = value
# with open(f"{files_path}SetConfig.py", "a") as f2:
# f2.write("server_json = {}\n".format(person))

@bot.message_handler(commands=['srv'])
def send_srv(message):
    global msgsrv
    msgsrv = bot.send_message(message.chat.id, "Please Enter Admin Password : ")
    bot.register_next_step_handler(msgsrv, checkpasssrv)
def checkpasssrv(message):
    r = json.dumps(server_json, indent=2)

    if message.text == adminpass:
        msg = bot.send_message(message.chat.id,
                               f"The Currect Server.json Settings is : \n\n<code>{r}</code>\n\n🆕 Please Enter The new Servers or <b>(for cancel this proccess type : ex)</b>",
                               parse_mode='HTML')
        bot.register_next_step_handler(msg, ServerWrite_srv)
    else:
        bot.send_message(message.chat.id, "❌ The Password is incorrect\n\nPlease Enter correct password again :\n\n<b>(for exit enter ex)</b>")
        if message.text in ("ex", "EX", "Ex"):
            bot.send_message(message.chat.id, f"✅ Exit Success.")
        else:
            bot.register_next_step_handler(msgsrv, checkpasssrv)
def ServerWrite_srv(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"Exit")
    else:
        srvjson = f'''{str(message.text)}'''
        update_config("server_json", srvjson.replace("'", '"'))
        SET_command_list()
        bot.send_message(message.chat.id, "<b>✅ the new Server config saved successfully.\n\n✅ the Telegram Commands update successfully.</b>", parse_mode='HTML')

@bot.message_handler(commands=['generate_commands'])
def send_generate_commands(message):
    #bot.send_message(message.chat.id, f"<code>{bot_commands_list}</code>")
    #print(bot_commands_list)
    global msg_generate_commands
    msg_generate_commands = bot.send_message(message.chat.id, "Please Enter Admin Password : ")
    bot.register_next_step_handler(msg_generate_commands, checkpass_generate_commands)
def checkpass_generate_commands(message):
    if message.text == adminpass:
        bot.send_message(message.chat.id,
                               f"Current Command list : \n\n<code>{bot_commands_list}</code>\n\n<b>Please Enter y(yes) for Generate new commands automaticlly \n\nor\n\nPlease enter n(no) for cancel this proccess</b>",
                               parse_mode='HTML')
        bot.register_next_step_handler(msg_generate_commands, CommandWrite_generate_commands)
    else:
        bot.send_message(message.chat.id,
                         "❌ The Password is incorrect\n\nPlease Enter correct password again :\n\n<b>(for exit enter ex)</b>")
        if message.text in ("ex", "EX", "Ex"):
            bot.send_message(message.chat.id, f"✅ Exit Success.")
        else:
            bot.register_next_step_handler(msg_generate_commands, checkpass_generate_commands)
def CommandWrite_generate_commands(message):
    if message.text in ("n", "No", "no", "N", "NO"):
        bot.send_message(message.chat.id, f"Exit")
    else:
        if message.text in ("y", "Y", "YES", "yes", "Yes"):
            bot.send_message(message.chat.id, f"<b>✅ the new settings saved successfully.</b>\n\n",
                             parse_mode='HTML')
            SET_command_list()
        else:
            msg = bot.send_message(message.chat.id, f"<b>You must enter y/Yes or n/No only, please try again.</b>\n\n",
                             parse_mode='HTML')
            bot.register_next_step_handler(msg, CommandWrite_generate_commands)

@bot.message_handler(commands=['edit_commands'])
def send_Command_edit_commands(message):
    global msg_edit_commands
    msg_edit_commands = bot.send_message(message.chat.id, "Please Enter Admin Password : ")
    bot.register_next_step_handler(msg_edit_commands, checkpasslist_edit_commands)
def checkpasslist_edit_commands(message):
    if message.text == Bot_Admin_Passwd:
        msg = bot.send_message(message.chat.id,
                               f"The Current Telegram Commands Are : \n\n<code>{bot_commands_list}</code>\n\n🆕 Please Enter The new Telegram Commands : \n\nSend me a list of commands for bot. Please use this format:\ncommand1 - Description\ncommand2 - Another description\n\n<b>(for cancel this proccess type : ex)</b>",
                               parse_mode='HTML')
        bot.register_next_step_handler(msg, ListWrite_edit_commands)
    else:
        bot.send_message(message.chat.id,
                         "❌ The Password is incorrect\n\nPlease Enter correct password again :\n\n<b>(for exit enter ex)</b>")
        if message.text in ("ex", "EX", "Ex"):
            bot.send_message(message.chat.id, f"✅ Exit Success.")
        else:
            bot.register_next_step_handler(msg_edit_commands, checkpasslist_edit_commands)
def ListWrite_edit_commands(message):
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"Exit")
    else:
        new_cmd_list = message.text
        update_config('bot_commands_list', str(new_cmd_list))
        json_object = json.loads(bot_commands_list)
        l = []
        for item in json_object:
            #print(item['command'], item['description'])
            l.extend([telebot.types.BotCommand(f"{item['command']}", f"{item['description']}")])
        #print(l)
        bot.set_my_commands(l)
        bot.send_message(message.chat.id,
                         f"<b>✅ Telegram Commands are Updated successfully.</b>",
                         parse_mode='HTML')

@bot.message_handler(commands=['set'])
def send_Command_set(message):
    ch = bancheck(message.from_user.username)
    global msg_setting
    if ch == False:
        msg_setting = bot.send_message(message.chat.id, "Please Enter Admin Password : ")
        bot.register_next_step_handler(msg_setting, checkpassset)
    else:
        bot.reply_to(message, 'دسترسی شما به علت اسپم و استفاده بیش از حد مجاز در این ربات مسدود شده است')
def checkpassset(message):
    if message.text == Bot_Admin_Passwd:
        msg = bot.send_message(message.chat.id,
                               f"1️⃣ Edit Server List : /srv\n\n2️⃣ Edit Telegram Bot Commands : \n/edit_commands\n\n3️⃣ Generate Commands Automatic : \n/generate_commands\n\n4️⃣ Ban Users : /ban\n\n5️⃣ Initialize The Bot : /install\n\n6️⃣ Restart Bot : /restart\n\n7️⃣ Servers Info : /serversinfo\n\n8️⃣ Show User Log : /loguser\n\n9️⃣ Send Msg ALL : /msgall\n\n🔟 Send Msg ID : /msgid\n\n1️⃣1️⃣ Read Messages : /showcontact\n\n1️⃣2️⃣User ID List : /showusersid",
                               parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,
                         "❌ The Password is incorrect\n\nPlease Enter correct password again :\n\n<b>(for exit enter ex)</b>")
        if message.text in ("ex", "EX", "Ex"):
            bot.send_message(message.chat.id, f"✅ Exit Success.")
        else:
            bot.register_next_step_handler(msg_setting, checkpassset)

def generate_buttons(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup
def set_unban(user):
    ban = bancheck(user)
    if ban == True:
        ban_list = Get_Ban_list()
        for i in ban_list:
            ban_list = Get_Ban_list()
            if i == user:
                ban_list.remove(i)
                update_config('user_ban', str(ban_list))
@bot.message_handler(commands=['ban'])
def send_helloban(message):
    global msg_ban
    msg_ban = bot.send_message(message.chat.id, "Please Enter Admin Password : ")
    bot.register_next_step_handler(msg_ban, checkpassban)
def checkpassban(message):
    if message.text == Bot_Admin_Passwd:
        listtext = str(user_ban)
        bot.send_message(message.chat.id,
                         f"The Current User Banned : \n\n<code>{listtext}</code>\n",
                         parse_mode='HTML')
        msg = bot.send_message(message.chat.id, "Please Enter telegram id for add or remove from list : \n\nfor exit enter ex")
        bot.register_next_step_handler(msg, btnGenerateban)
    else:
        bot.send_message(message.chat.id,
                         "❌ The Password is incorrect\n\nPlease Enter correct password again :\n\n<b>(for exit enter ex)</b>")
        if message.text in ("ex", "EX", "Ex"):
            bot.send_message(message.chat.id, f"✅ Exit Success.")
        else:
            bot.register_next_step_handler(msg_ban, checkpassban)
def btnGenerateban(message):
    global setuserbanTEXT
    setuserbanTEXT = message.text
    if message.text in ("ex", "EX", "Ex"):
        bot.send_message(message.chat.id, f"✅ Exit Success.")
    else:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup = generate_buttons(['ban', 'unban', 'exit'], markup)
        message = bot.reply_to(message, """What you want to do ?""", reply_markup=markup)
        bot.register_next_step_handler(message, BanUserOptban)

def BanUserOptban(message):
    opt = bancheck(setuserbanTEXT)
    if message.text == "ban":
        if opt == True:
            bot.reply_to(message, f"the user : {setuserbanTEXT} already in ban list", reply_markup=ReplyKeyboardRemove())
        else:
            ban_list = Get_Ban_list()
            ban_list.append(str(setuserbanTEXT))
            update_config('user_ban', str(ban_list))
            bot.reply_to(message, f"the user : {setuserbanTEXT} added to ban list", reply_markup=ReplyKeyboardRemove())
    elif message.text == 'unban':
        if opt == True:
            set_unban(setuserbanTEXT)
            bot.reply_to(message, f"the user : {setuserbanTEXT} UnBanned", reply_markup=ReplyKeyboardRemove())
        else:
            bot.reply_to(message, f"The User {setuserbanTEXT} Already Not Ban", reply_markup=ReplyKeyboardRemove())
    elif message.text == 'exit':
        bot.send_message(message.chat.id, f"✅ Exit Success.", reply_markup=ReplyKeyboardRemove())
    else:
        bot.reply_to(message, f"Choose Ban or Unban , Try Again", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(commands=['serversinfo'])
def server_info(message):
    TUsage = []
    TUser = []
    for sname in server_json:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        url = server_json[sname]
        browser.get(url)
        inf = f"Webdriver ready to work for getting data from {url}"
        bot.send_message(message.chat.id, inf, parse_mode='HTML')
        user = browser.find_element(By.XPATH,
                                    value="//*[@id='app']/main/div[2]/div/form/div[1]/div/div/span/span/input")
        user.clear()
        user.send_keys(XUI_User)

        passs = browser.find_element(By.XPATH,
                                     value="//*[@id='app']/main/div[2]/div/form/div[2]/div/div/span/span/input")
        passs.clear()
        passs.send_keys(XUI_Pass)

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='app']/main/div[2]/div/form/div[3]/div/div/span/button")
        button.click()

        time.sleep(2)
        browser.get(f'{url}xui/inbounds')
        button = browser.find_element(By.XPATH, value="//*[@id='sider']/div/ul/li[2]")
        button.click()

        button = browser.find_element(By.XPATH,
                                      value="//*[@id='content-layout']/main/div/div/div[2]/div[1]/div/div/div/button")
        button.click()
        time.sleep(2)
        server_title = sname + f" {url} "
        total_usage = browser.find_element(By.XPATH,
                                           value="""//*[@id="content-layout"]/main/div/div/div[1]/div/div/div[2]/span""").text
        total_user = browser.find_element(By.XPATH,
                                          value="""//*[@id="content-layout"]/main/div/div/div[1]/div/div/div[3]/span""").text
        information = f"Server Name : <code>{server_title}</code> \nTotal Users : <code>{total_user}</code> \nTotal Usage : <code>{total_usage}</code>"
        bot.send_message(message.chat.id, information, parse_mode='HTML')
        browser.switch_to.window(browser.window_handles[0])
        browser.delete_all_cookies()
        browser.close()
        browser.quit()
        TUsage.append(total_usage)
        TUser.append(total_user)

    l = TUsage
    MB = []
    KB = []
    GB = []

    def converttoint(list):
        list = [w.replace(' KB', '') for w in list]
        list = [w.replace(' MB', '') for w in list]
        list = [w.replace(' GB', '') for w in list]
        global resol
        resol = [eval(i) for i in list]
        resol = sum(resol)
        return resol

    for d in l:
        if ' MB' in d:
            MB.append(d)
        if ' KB' in d:
            KB.append(d)
        if ' GB' in d:
            GB.append(d)

    KB = (converttoint(KB) / 1024) / 1024
    MB = converttoint(MB) / 1024
    GB = converttoint(GB)
    sumi = KB + MB + GB
    sumdec = f"Total Usage is : {sumi:.2f} GB"
    bot.send_message(message.chat.id, sumdec, parse_mode='HTML')
    #print(f"Total Usage is : <code>{sumi:.2f}</code> GB")
    global usersums
    usersums = [eval(i) for i in TUser]
    usersums = sum(usersums)
    #print(f"Total Connecions : {usersums}")
    bot.send_message(message.chat.id, f"Total Connecions : <code>{usersums}</code>", parse_mode='HTML')

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    ch = bancheck(message.from_user.username)
    if ch == False:
        bot.reply_to(message, 'برای ساخت v2ray مورد نظر از بخش Menu لوکیشن و نوع اتصال را انتخاب کنید')
    else:
        bot.reply_to(message, 'دسترسی شما به علت اسپم و استفاده بیش از حد مجاز در این ربات مسدود شده است')

if __name__ == '__main__':
    # bot.infinity_polling()
    # bot.polling(none_stop=True)
    bot.infinity_polling(timeout=10, long_polling_timeout=5)