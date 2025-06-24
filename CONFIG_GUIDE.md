# 京东茅台秒杀系统配置指南

## 📋 配置文件说明

### 文件位置
- **主配置文件**: `config.ini`
- **配置模板**: `config.template.ini`

### 配置优先级
1. **环境变量** (最高优先级)
2. **加密配置文件**
3. **运行时输入** (最低优先级)

## 🔧 详细配置说明

### [config] 基础配置

#### 设备指纹参数
```ini
# 设备标识符 - 自动更新
eid = ""

# 设备指纹 - 自动更新  
fp = ""
```
- **作用**: 用于京东风控验证
- **配置**: 登录后自动更新，无需手动修改
- **注意**: 不要随意修改，可能导致风控

#### 商品配置
```ini
# 商品SKU ID
sku_id = 100012043978

# 抢购数量
seckill_num = 1
```
- **sku_id**: 茅台固定为 `100012043978`
- **seckill_num**: 建议设置为 `1`，避免因数量过多失败

#### 时间配置
```ini
# 抢购开始时间
buy_time = 11:59:59.200

# 抢购结束时间
last_purchase_time = 12:30:00.000
```
- **格式**: `HH:MM:SS.mmm` (时:分:秒.毫秒)
- **茅台时间**: 工作日 12:00-12:30
- **建议**: 提前200毫秒开始抢购

#### 风控配置
```ini
# 风险等级
risk_level = BALANCED

# 并发进程数
max_processes = 8

# 重试次数
max_retries = 100
```

**风险等级说明**:
- `CONSERVATIVE`: 保守模式，安全但速度慢
- `BALANCED`: 平衡模式，推荐使用
- `AGGRESSIVE`: 激进模式，速度快但风险高

#### 浏览器配置
```ini
# 用户代理
default_user_agent = "Mozilla/5.0..."

# 随机用户代理
random_useragent = false
```
- **建议**: 使用最新Chrome的User-Agent
- **random_useragent**: 建议设置为 `false`

### [account] 账户配置

#### 支付密码
```ini
payment_pwd = ""
```

**配置方式**:

1. **环境变量 (推荐)**:
   ```bash
   # Windows
   set JD_PAYMENT_PWD=123456
   
   # Linux/Mac
   export JD_PAYMENT_PWD=123456
   
   # PowerShell
   $env:JD_PAYMENT_PWD="123456"
   ```

2. **运行时输入**:
   - 程序会提示输入
   - 自动加密保存

3. **直接填写**:
   ```ini
   payment_pwd = "123456"
   ```

**何时需要**:
- 账户有京券
- 使用了京豆支付
- 京东要求输入支付密码

### [messenger] 消息通知

#### 启用通知
```ini
enable = true
```
- `true`: 启用微信通知
- `false`: 禁用通知

#### Server酱密钥
```ini
sckey = ""
```

**配置方式**:

1. **环境变量 (推荐)**:
   ```bash
   # Windows
   set JD_SCKEY=SCT123456ABCDEF
   
   # Linux/Mac
   export JD_SCKEY=SCT123456ABCDEF
   ```

2. **运行时输入**:
   - 登录后程序询问是否配置
   - 选择 `yes` 后输入SCKEY

3. **直接填写**:
   ```ini
   sckey = "SCT123456ABCDEF"
   ```

**获取SCKEY**:
1. 访问 https://sct.ftqq.com/
2. 微信扫码登录
3. 创建应用获取SCKEY

## 🚀 快速配置步骤

### 新手配置
1. **复制模板**:
   ```bash
   cp config.template.ini config.ini
   ```

2. **设置环境变量**:
   ```bash
   set JD_PAYMENT_PWD=您的支付密码
   set JD_SCKEY=您的SCKEY
   ```

3. **运行程序**:
   ```bash
   python main.py
   ```

### 高级配置
1. **修改时间参数** (根据网络延迟调整)
2. **调整风控等级** (根据成功率调整)
3. **优化并发数** (根据电脑性能调整)

## ⚠️ 注意事项

### 安全建议
- ✅ 优先使用环境变量配置敏感信息
- ✅ 不要将包含密码的config.ini上传到公共仓库
- ✅ 定期更换支付密码和SCKEY

### 常见错误
- ❌ 时间格式错误 (必须包含毫秒)
- ❌ SKU ID错误 (茅台固定为100012043978)
- ❌ 支付密码格式错误 (必须是6位数字)

### 性能优化
- 🔧 根据网络情况调整 `buy_time`
- 🔧 根据电脑性能调整 `max_processes`
- 🔧 根据成功率调整 `risk_level`

## 🛠️ 故障排除

### 配置不生效
1. 检查配置文件格式
2. 确认环境变量设置
3. 重启程序重新加载配置

### 抢购失败
1. 调整 `buy_time` 提前时间
2. 增加 `max_retries` 重试次数
3. 尝试不同的 `risk_level`

### 通知不工作
1. 确认 `enable = true`
2. 检查SCKEY格式
3. 测试Server酱服务

## 📞 技术支持

- **详细文档**: `README.md`
- **安全指南**: `SECURITY_FEATURES_GUIDE.md`
- **问题反馈**: 提交Issue或联系开发者
