from loguru import logger

from WechatAPI import WechatAPIClient
from utils.decorators import *
from utils.plugin_base import PluginBase
import requests
import tomllib
import json
import ast

class PluginsSwitch(PluginBase):
    description = "PluginsSwitch"
    author = "xuangeer"
    version = "0.0.1"
    mymap = {}
    mymapstr = {}


    # 同步初始化
    def __init__(self):
        super().__init__()
        
        with open("main_config.toml", "rb") as f:
            config = tomllib.load(f)

        self.admins = config["XYBot"]["admins"]
        return

    # 异步初始化
    async def async_init(self):
        await self.queryall(self.mymap)
        return

    @on_text_message(priority=90)
    async def handle_text(self, bot: WechatAPIClient, message: dict):
#    	   if message["SenderWxid"] in self.admins:  #如果是管理员放行
#            return
        msg = message["Content"]
        command = str(msg).strip().split(" ")[0]
        if (command not in self.mymap):  # 不是指令
            print("不是命令 放行")
            return True
        if message["FromWxid"] in self.mymap[command]:
            return False

            
    async def queryall(self, mymap):
        with open('plugins/PluginsSwitch/db.json', 'r') as f:
            content = f.read().strip()
            if content:
                data_str = content
            if not data_str.strip():
                self.mymap = {}
            else:
                try:
                    self.mymap = ast.literal_eval(data_str)
                except Exception as e:
                    self.mymap = {}
    async def mymapSetall(self):
        try:
            with open('plugins/PluginsSwitch/db.json', 'w') as f:
                f.write(str(self.mymap).replace("'", '"'))
        except Exception as e:
            print(f"写入文件时发生错误: {e}")
        print("写入文件成功")
            
    async def mymapset(self, name, fromWxid):
        if name not in self.mymap:
            self.mymap[name] = set()
        self.mymap[name].add(fromWxid)

    async def mymapdel(self, name , fromWxid):
        self.mymap[name].discard(fromWxid)
        if len(self.mymap[name]) == 0 :
            del self.mymap[name]
        
    @on_text_message(priority=20)
    async def handle_text1(self, bot: WechatAPIClient, message: dict):
        if message["SenderWxid"] not in self.admins:
            if "开启命令" in message["Content"] or "关闭命令" in message["Content"]:
                await bot.send_text_message(message["FromWxid"], "无管理员权限")
            return
        command = str(message["Content"]).strip().split(" ")
        if len(command) == 1 and (command[0] == "关闭命令" or command[0] == "开启命令"):  # 只是指令，但没请求内容
            await bot.send_text_message(message["FromWxid"], "请正确输入关闭指令\n实例: 关闭命令 点歌")
            return
            
        mingling = command[0]
        name = command[1]
        if mingling == "关闭命令":
            if name == "星座":
                await self.mymapset("天蝎座" , message["FromWxid"])
                await self.mymapset("巨蟹座" , message["FromWxid"])
                await self.mymapset("白羊座" , message["FromWxid"])
                await self.mymapset("金牛座" , message["FromWxid"])
                await self.mymapset("双子座" , message["FromWxid"])
                await self.mymapset("狮子座" , message["FromWxid"])
                await self.mymapset("处女座" , message["FromWxid"])
                await self.mymapset("天秤座" , message["FromWxid"])
                await self.mymapset("射手座" , message["FromWxid"])
                await self.mymapset("摩羯座" , message["FromWxid"])
                await self.mymapset("水瓶座" , message["FromWxid"])
                await self.mymapset("双鱼座" , message["FromWxid"])
            else:
                await self.mymapset(name , message["FromWxid"])
            await bot.send_text_message(message["FromWxid"], "命令[" + name + "]关闭成功")
            await self.mymapSetall()
            return
            
        if mingling == "开启命令":
            if name == "星座":
                await self.mymapdel("天蝎座" , message["FromWxid"])
                await self.mymapdel("巨蟹座" , message["FromWxid"])
                await self.mymapdel("白羊座" , message["FromWxid"])
                await self.mymapdel("金牛座" , message["FromWxid"])
                await self.mymapdel("双子座" , message["FromWxid"])
                await self.mymapdel("狮子座" , message["FromWxid"])
                await self.mymapdel("处女座" , message["FromWxid"])
                await self.mymapdel("天秤座" , message["FromWxid"])
                await self.mymapdel("射手座" , message["FromWxid"])
                await self.mymapdel("摩羯座" , message["FromWxid"])
                await self.mymapdel("水瓶座" , message["FromWxid"])
                await self.mymapdel("双鱼座" , message["FromWxid"])
            else:
                if name not in self.mymap or message["FromWxid"] not in self.mymap[name]:
                    await bot.send_text_message(message["FromWxid"], "命令[" + name + "]并未关闭")
                    return
                await self.mymapdel(name , message["FromWxid"])
            await self.mymapSetall()
            await bot.send_text_message(message["FromWxid"], "命令[" + name + "]开启成功")
            return
        
            
        
      