import pandas as pd
import socket
from ping3 import ping
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 域名列表（已去重整理）
domains = [
    "adfdv.occupationedu.com",
    "tsnewjn.occupationedu.com",
    "hengppxjn.occupationedu.com",
    "kmljn.occupationedu.com",
    "kskt2023.occupationedu.com",
    "hdnxy2023jn.occupationedu.com",
    "kjhba.occupationedu.com",
    "2023hbnh2.occupationedu.com",
    "uytdf.occupationedu.com",
    "jrjyzxnxy.dianyueyun.com",
    "hdsffkqnxy.dianyuesoft.com",
    "2024alkeqjn.dianyueyun.com",
    "dqnshjn.dianyueyun.com",
    "hh.jn.dianyueyun.com",
    "wd240619jn.dianyueyun.com",
    "hbjn.dianyueyun.com",
    "wd24080101jn.dianyueyun.com",
    "wd240809jn.dianyueyun.com",
    "wd240812jn.dianyueyun.com",
    "wd24100902jn.dianyueyun.com",
    "wd241018jn.dianyueyun.com",
    "192.168.5.251",  # 内网IP（移除端口）
    "wd24110401jn.dianyueyun.com",
    "wd241119jn.dianyueyun.com",
    "wd24111904jn.dianyueyun.com",
    "wd241120jn.dianyueyun.com",
    "wd24112001jn.dianyueyun.com",
    "wd241206jn.dianyueyun.com",
    "wd24120603jn.dianyueyun.com",
    "wd241209jn.dianyueyun.com",
    "wd241218jn.dianyueyun.com",
    "wd250113jn.dianyueyun.com",
    "wd250114jn.dianyueyun.com",
    "wd250115jn.dianyueyun.com",
    "wd250305jn.dianyueyun.com",
    "wd250218jn.dianyueyun.com",
    "wd250227jn.dianyueyun.com",
    "wd250228jn.dianyueyun.com",
    "wd250306jn.dianyueyun.com",
    "wd250312jn.dianyueyun.com",
    "wd25031201jn.dianyueyun.com",
    "wd250313jn.dianyueyun.com",
    "wd250327jn.dianyueyun.com",
    "wd25042201jn.dianyueyun.com",
    "wd25042202jn.dianyueyun.com",
    "wd25042302jn.dianyueyun.com",
    "wd250424jn.dianyueyun.com",
    "wd250516jn.dianyueyun.com",
    "wd25052101jn.dianyueyun.com",
    "wd25052102jn.dianyueyun.com",
    "wd241008jn.dianyueyun.com",
    "wd250528jn.dianyueyun.com",
    "wd250529jn.dianyueyun.com",
    "wd25052902jn.dianyueyun.com",
    "wd25052903jn.dianyueyun.com",
    "wd25060503jn.dianyueyun.com",
    "wd25060501jn.dianyueyun.com",
    "wd25060502jn.dianyueyun.com",
    "wd25060504jn.dianyueyun.com",
    "wd250618jn.dianyueyun.com",
    "wd250620jn.dianyueyun.com",
    "wd250710jn.dianyueyun.com",
    "wd250806jn.dianyueyun.com",
    "hbjz2025jn.dianyueyun.com",
    "192.168.20.222",  # 内网IP（移除端口）
    "wd251216jn.dianyueyun.com"
]

def get_ip(domain):
    """获取域名IP，内网IP直接返回"""
    try:
        if domain.replace('.', '').isdigit() or domain.startswith('192.168.'):
            return domain
        return socket.gethostbyname(domain)
    except:
        return "无法解析"

def test_ping(domain):
    """执行ping测试"""
    try:
        # 内网IP特殊处理
        target = domain.split(':')[0] if ':' in domain else domain
        delay = ping(target, timeout=2, unit='ms')
        if delay is None:
            return "超时", "❌ 超时"
        return f"{delay:.2f} ms", "✅ 正常"
    except:
        return "错误", "❌ 错误"

# 执行测试
results = []
print(f"开始测试 {len(domains)} 个域名... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")

for idx, domain in enumerate(domains, 1):
    ip = get_ip(domain)
    delay, status = test_ping(domain)
    results.append({
        "序号": idx,
        "域名": domain,
        "IP地址": ip,
        "延迟": delay,
        "状态": status,
        "备注": "内网" if domain.startswith(('192.168.', '10.', '172.16.')) else ""
    })
    print(f"[{idx}/{len(domains)}] {domain:40s} → {status:8s} {delay}")

# 生成DataFrame
df = pd.DataFrame(results)

# 统计信息
success = df[df["状态"].str.contains("正常")].shape[0]
total = len(df)
avg_delay = df[df["延迟"].str.contains("ms")]["延迟"].str.extract(r'([\d.]+)').astype(float).mean().values[0] if not df[df["延迟"].str.contains("ms")].empty else 0

print(f"\n✅ 测试完成！成功率: {success}/{total} ({success/total*100:.1f}%) | 平均延迟: {avg_delay:.2f} ms")

# 保存Excel
filename = f"域名Ping测试结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Ping结果', index=False)
    
    # 写入统计摘要
    summary = pd.DataFrame([{
        "测试时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "总域名数": total,
        "成功数": success,
        "失败数": total - success,
        "成功率": f"{success/total*100:.1f}%",
        "平均延迟": f"{avg_delay:.2f} ms"
    }])
    summary.to_excel(writer, sheet_name='统计摘要', index=False)

print(f"\n📁 结果已保存至: {filename}")
print("💡 提示: Excel中绿色=正常，红色=异常（可用条件格式进一步美化）")