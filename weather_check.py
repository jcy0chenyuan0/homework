# -*- coding: utf-8 -*-
"""
weather_check.py
查询昆明市呈贡区的实时天气。

数据来源：Open-Meteo（https://open-meteo.com），免费、无需 API Key。

用法：
    python weather_check.py
"""

import sys

import requests

# ---- 目标地点：昆明市呈贡区 ----
LOCATION_NAME = "昆明市呈贡区"
LATITUDE = 24.879      # 纬度
LONGITUDE = 102.802    # 经度

API_URL = "https://api.open-meteo.com/v1/forecast"

# WMO 天气代码 -> 中文描述
WEATHER_CODES = {
    0: "晴",
    1: "晴间多云",
    2: "多云",
    3: "阴",
    45: "雾",
    48: "雾凇",
    51: "小毛毛雨",
    53: "毛毛雨",
    55: "大毛毛雨",
    56: "冻毛毛雨",
    57: "强冻毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "冻雨",
    67: "强冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "小阵雨",
    81: "阵雨",
    82: "强阵雨",
    85: "小阵雪",
    86: "强阵雪",
    95: "雷阵雨",
    96: "雷阵雨伴小冰雹",
    99: "雷阵雨伴大冰雹",
}


def describe(code):
    """把 WMO 天气代码翻译成中文描述。"""
    return WEATHER_CODES.get(code, f"未知天气({code})")


def fetch_weather():
    """请求 Open-Meteo，返回当前天气与未来 3 天预报。"""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
            "wind_speed_10m",
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
        ],
        "timezone": "Asia/Shanghai",
        "forecast_days": 3,
    }

    resp = requests.get(API_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def print_weather(data):
    """格式化输出天气信息。"""
    current = data["current"]
    print("=" * 40)
    print(f"  地点：{LOCATION_NAME}")
    print(f"  时间：{current['time']}")
    print("=" * 40)
    print(f"  天气：{describe(current['weather_code'])}")
    print(f"  气温：{current['temperature_2m']} °C")
    print(f"  体感：{current['apparent_temperature']} °C")
    print(f"  湿度：{current['relative_humidity_2m']} %")
    print(f"  风速：{current['wind_speed_10m']} km/h")
    print("-" * 40)

    daily = data["daily"]
    print("  未来 3 天预报：")
    for i, day in enumerate(daily["time"]):
        print(
            f"    {day}   "
            f"{describe(daily['weather_code'][i]):<8}"
            f"{daily['temperature_2m_min'][i]} ~ "
            f"{daily['temperature_2m_max'][i]} °C"
        )
    print("=" * 40)


def keep_window_open():
    """打包为 exe 双击运行时，保留独立的控制台窗口，避免结果一闪而过。

    仅在「PyInstaller 打包后的 exe」中生效（sys.frozen 为真）；
    用 python 直接运行时不会暂停，便于脚本 / 管道调用。
    """
    if not getattr(sys, "frozen", False):
        return
    try:
        input("\n按回车键关闭窗口...")
    except (EOFError, KeyboardInterrupt):
        pass


def main():
    exit_code = 0
    try:
        data = fetch_weather()
    except requests.RequestException as exc:
        print(f"获取天气失败：{exc}", file=sys.stderr)
        exit_code = 1
    else:
        print_weather(data)
    finally:
        # 作为 main 独立运行时，保留窗口以便查看输出。
        keep_window_open()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
