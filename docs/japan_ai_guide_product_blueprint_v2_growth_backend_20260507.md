# Japan AI Guide（日本 AI 导览平台）产品蓝图 V2

> 更新日期：2026-05-07  
> 本版重点：把“前台 AI 内容体验”升级为“前台增长平台 + 后台运营/统计/归因系统”的完整蓝图。

---

# 一、项目定位

Japan AI Guide 是一个：

> 像 ChatGPT 一样使用的日本 AI 导览平台。

它不是传统旅游网站，而是：

# AI 日本旅游内容入口 + AI 推荐流量平台

用户进入网站后，不需要学习复杂页面结构，只需要直接提问：

```text
用户提问
↓
AI 返回旅游内容卡片
↓
继续推荐相关景点 / 美食 / 酒店 / 路线 / 文化内容
↓
形成路线 / 内容流
↓
未来转向包车 / 接送 / 酒店 / 餐厅 / 景区预订
```

---

# 二、当前核心战略

## 1. 前 6-12 个月核心目标

前期不急于商业化，不急于做重交易闭环。

核心目标是：

# 疯狂做内容，疯狂做用户，疯狂做平台推广

重点是：

- 让用户觉得平台好用
- 让用户觉得平台好玩
- 让用户形成“去日本之前先问 Japan AI Guide”的习惯
- 让平台成为日本旅游前置决策入口

前期产品可以免费，后台功能可以提前做出来，但不急着收费。

---

## 2. 免费不是没有商业价值

前期免费阶段真正积累的是：

- 用户 query 数据
- 用户兴趣路径
- 推荐点击数据
- 来源渠道数据
- 内容热度数据
- 分享传播数据
- 未来商业转化基础

也就是说：

# 前台免费，后台记录增长资产。

---

# 三、前台产品结构

## 1. 主页面

主页面保持极简 ChatGPT 风格：

```text
左侧：
历史记录 / 收藏 / 已生成路线

中间：
Logo
AI 输入框
快捷问题按钮
AI 回答内容流

右上：
语言选择
```

主页面不是传统导航站。

所有内容都通过 AI 回答卡片呈现。

---

## 2. AI 回答卡片

AI 回答卡片是前台核心。

例如用户输入：

```text
清水寺
```

系统返回：

- 景点介绍
- 历史背景
- 文化故事
- 附近景点
- 附近美食
- 推荐路线
- 推荐酒店
- 继续提问按钮

未来可扩展：

- 播放 AI 讲解
- 查看地图
- 加入路线
- 收藏
- 分享
- 包车询价
- 酒店/餐厅/门票跳转

---

## 3. Multi-card 内容流

当前系统已经从：

```text
1 query -> 1 card
```

升级为：

```text
1 query
↓
main_card
↓
related_cards
↓
recommendation sections
↓
suggested prompts
```

这是 Japan AI Guide 的核心产品形态。

---

# 四、AI 内容编排核心

当前核心链路：

```text
query
↓
intent router
↓
token gate
↓
content index
↓
top-k ranking
↓
cache
↓
repository
↓
recommendation orchestrator
↓
multi-card response
```

当前已经完成：

- AnswerCard Schema
- Intent Router
- Token Gate
- Content Library
- Cache + Ranking
- Top-K Ranking
- Multi-Card Response
- Recommendation Orchestrator

---

# 五、Recommendation Orchestrator

Recommendation Orchestrator 是系统的大脑。

它负责决定：

- 用户问城市时，先推荐什么
- 用户问路线时，先推荐什么
- 用户问景点时，先推荐什么
- 用户随便问时，如何给出 suggested prompts
- 如何避免 main card / related card / section 重复
- 如何让推荐内容像 AI 导游，而不是硬广告

示例：

| Intent | 推荐顺序 |
|---|---|
| city_query | 景点 → 路线 → 美食 → 文化 → 酒店 |
| route_query | 景点 → 美食 → 酒店 → 文化 |
| spot_query | 附近景点 → 美食 → 路线 → 文化 |
| food_query | 美食 → 附近景点 → 路线 |
| culture_query | 文化 → 相关景点 → 路线 |
| hotel_query | 酒店 → 附近景点 → 路线 |
| generic_query | suggested prompts |

---

# 六、后台系统总体定位

未来必须建设一个后台系统：

# Japan AI Guide Admin / Growth Console

它不是普通 CMS，而是：

# 内容管理 + 推荐控制 + 数据统计 + 流量归因 + 合作方管理 + 增长分析后台

后台的核心作用：

```text
管理内容
↓
控制推荐策略
↓
统计用户行为
↓
分析推广渠道
↓
记录合作方归因
↓
支撑未来商业化
```

---

# 七、后台模块设计

## 1. 内容管理后台 CMS

用于管理：

- 景点
- 城市
- 美食
- 路线
- 文化内容
- 酒店
- 购物中心
- 景区
- 餐厅
- 多语言内容
- 图片 / 音频 / 标签

核心能力：

- 新增内容
- 修改内容
- 上下架
- 多语言编辑
- 内容标签管理
- 推荐理由编辑
- 内容质量评分
- SEO 标题与描述
- 封面图管理

---

## 2. 推荐编排后台

用于控制 Recommendation Orchestrator。

后台可以调整：

- 不同 intent 的 section 顺序
- 每个 section 展示数量
- 推荐阈值
- 去重规则
- suggested prompts
- 城市/季节/节日策略
- 内容优先级
- 合作方加权
- A/B test 策略

注意：

# 合作方加权只能微调，不能破坏用户体验。

---

## 3. 合作方推荐控制

未来可以管理：

- 合作酒店
- 合作餐厅
- 合作景区
- 合作购物中心
- 合作包车/接送服务
- 合作活动
- 合作 campaign

每个合作方可以配置：

- partner_id
- partner_type
- 城市
- 区域
- 标签
- 适合人群
- 预算区间
- 推荐权重
- 合作开始/结束时间
- 跳转链接
- 追踪参数
- 推荐理由
- 是否可展示“合作推荐”标记

---

# 八、推荐与营销的平衡原则

## 核心原则

# 不做硬广告，做可信推荐。

推荐逻辑必须遵守：

```text
用户适合
+
路线合理
+
内容质量合格
+
合作方轻度加权
```

不能变成：

```text
谁给钱，谁排第一。
```

---

## 推荐权重分层

| 权重层级 | 优先级 | 含义 |
|---|---:|---|
| 用户体验权重 | 最高 | 是否适合用户需求 |
| 内容相关性 | 高 | 是否与 query / intent / route 匹配 |
| 质量权重 | 高 | 评分、距离、便利性、口碑 |
| 商业权重 | 低 | 合作方加权、活动加权 |
| 风险过滤 | 强制 | 不适合则禁止推荐 |

---

## 禁止推荐规则

即使是合作方，也不能推荐：

- 明显离路线很远
- 明显超出用户预算
- 低评分或体验差
- 与用户需求无关
- 破坏路线节奏
- 对老人/儿童/家庭不友好但仍强推
- 只因为合作就强行置顶

---

# 九、增长统计系统

从 Day 1 开始必须记录数据。

前期即使免费，也要把所有增长轨迹记录下来。

## 1. 核心增长指标

| 指标 | 含义 |
|---|---|
| DAU | 每日活跃用户 |
| WAU / MAU | 周/月活跃 |
| Query Volume | 每日 AI 提问量 |
| Sessions | 会话数 |
| Avg Queries Per Session | 每个会话平均提问数 |
| Retention | 次日/7日/30日留存 |
| Share Rate | 分享率 |
| Favorite Rate | 收藏率 |
| Route Generation Rate | 路线生成率 |
| Prompt Continuation Rate | suggested prompts 点击率 |
| Card CTR | 卡片点击率 |
| Section CTR | 推荐区点击率 |
| External Link CTR | 外部跳转点击率 |

---

## 2. 内容表现统计

后台要能看到：

- 热门 query
- 热门城市
- 热门景点
- 热门路线
- 热门美食
- 热门文化问题
- 热门酒店/区域
- 搜索无结果问题
- AI fallback 问题
- 用户最常继续追问的问题

这会帮助平台反向建设内容库。

---

## 3. 推荐表现统计

每个推荐都要能追踪：

- 是否展示
- 展示位置
- 是否点击
- 是否收藏
- 是否加入路线
- 是否分享
- 是否跳转
- 是否带来后续转化

推荐数据字段建议：

```json
{
  "recommendation_id": "...",
  "session_id": "...",
  "query_id": "...",
  "intent": "city_query",
  "section_type": "recommended_hotels",
  "card_slug": "kyoto_station_hotel_x",
  "position": 2,
  "shown_at": "...",
  "clicked": true
}
```

---

# 十、流量来源与跳转归因

这是增长后台最重要模块之一。

## 1. 来源追踪

必须记录用户从哪里来：

- 小红书
- 抖音
- Google
- YouTube
- Instagram
- TikTok
- 微信群
- 朋友圈
- 合作酒店
- 合作旅行社
- SEO 页面
- 直接访问

记录字段：

```text
utm_source
utm_medium
utm_campaign
utm_content
referrer
landing_page
first_query
device
language
country
city
```

---

## 2. 外部跳转追踪

必须记录用户从 Japan AI Guide 跳去了哪里：

- 酒店官网
- 餐厅预约
- 景区门票
- DaDa 包车
- Google Maps
- OTA 平台
- 合作方页面

记录字段：

```text
outbound_click_id
session_id
user_id
source_card
partner_id
destination_url
utm_params
clicked_at
```

---

## 3. 推荐归因

未来每一次合作推荐都应该生成：

```text
recommendation_id
partner_id
campaign_id
session_id
query_id
intent
card_slug
section_type
position
click_event
conversion_event
```

这样酒店/餐厅/景区才能知道：

# 这个客人是否由 Japan AI Guide 推荐而来。

---

# 十一、Event Tracking System

统一事件系统是后台统计的基础。

## 事件类型

| Event | 含义 |
|---|---|
| page_view | 页面访问 |
| session_start | 会话开始 |
| query_submit | 用户提问 |
| answer_rendered | AI 回答展示 |
| card_impression | 卡片曝光 |
| card_click | 卡片点击 |
| section_impression | 推荐区曝光 |
| suggested_prompt_click | 继续提问点击 |
| favorite_add | 收藏 |
| route_generate | 生成路线 |
| share_click | 分享 |
| outbound_click | 外部跳转 |
| partner_click | 合作方点击 |
| conversion_reported | 转化回传 |

---

## 事件 Schema 示例

```json
{
  "event_id": "evt_...",
  "event_type": "card_click",
  "timestamp": "2026-05-07T10:00:00+09:00",
  "user_id": "anonymous_or_login_user",
  "session_id": "sess_...",
  "query_id": "query_...",
  "intent": "city_query",
  "source": {
    "utm_source": "xiaohongshu",
    "utm_campaign": "kyoto_spring"
  },
  "target": {
    "card_slug": "kiyomizu",
    "section_type": "recommended_spots",
    "position": 1
  }
}
```

---

# 十二、后台数据表方向

除原有内容表外，新增以下方向。

## 1. 增长与事件表

```text
analytics_events
sessions
traffic_sources
queries
query_results
card_impressions
card_clicks
section_impressions
outbound_clicks
```

---

## 2. 推荐与编排表

```text
recommendation_rules
orchestration_configs
recommendation_logs
recommendation_experiments
suggested_prompts
```

---

## 3. 合作方与归因表

```text
partners
partner_campaigns
partner_links
partner_recommendation_rules
partner_clicks
partner_conversions
```

---

## 4. 内容运营表

```text
content_items
content_tags
content_quality_scores
content_translations
content_media
content_publish_status
```

---

# 十三、后台权限设计

未来后台需要不同角色。

| 角色 | 权限 |
|---|---|
| Admin | 全部权限 |
| Content Editor | 内容编辑、上下架 |
| Growth Operator | 查看增长数据、配置推广活动 |
| Recommendation Manager | 调整推荐策略 |
| Partner Manager | 管理合作方、链接、归因 |
| Analyst | 只看数据报表 |
| Viewer | 只读 |

---

# 十四、后台 Dashboard

后台首页建议分为 6 块。

## 1. 增长总览

- 今日访问
- 今日 query
- 今日新用户
- 今日分享
- 今日外部跳转
- 今日热门来源

## 2. 内容表现

- 热门城市
- 热门景点
- 热门路线
- 热门美食
- 热门问题
- 无结果 query

## 3. 推荐表现

- 推荐曝光
- 推荐点击
- section CTR
- suggested prompts CTR
- dedupe 情况
- orchestration strategy 表现

## 4. 渠道来源

- 小红书来源
- 抖音来源
- Google 来源
- SEO 来源
- 合作方来源
- 直接访问

## 5. 合作方表现

- 合作酒店曝光
- 合作酒店点击
- 合作餐厅点击
- 景区跳转
- DaDa 包车导流
- partner conversion

## 6. 系统健康

- API 成功率
- cache hit rate
- fallback rate
- token usage
- response time
- error log

---

# 十五、阶段路线图

## Phase 1：AI 内容平台内核

目标：

- ChatGPT 式首页
- AnswerCard
- Intent Router
- Content Library
- Ranking
- Multi-card
- Recommendation Orchestrator

状态：

# 已基本完成。

---

## Phase 2：增长统计与后台基础

目标：

- Event Tracking
- UTM / Referrer Tracking
- Query Tracking
- Card CTR Tracking
- Outbound Link Tracking
- Basic Admin Dashboard
- Content CMS 基础

这是当前蓝图新增重点。

---

## Phase 3：内容飞轮与用户习惯

目标：

- 疯狂做内容
- 疯狂做 SEO
- 疯狂做社媒推广
- 提升分享
- 提升收藏
- 提升路线生成
- 让用户形成使用习惯

商业化保持轻，不破坏体验。

---

## Phase 4：合作方推荐与归因

目标：

- 合作酒店推荐
- 合作餐厅推荐
- 合作景区推荐
- 合作购物中心推荐
- partner link tracking
- campaign tracking
- partner dashboard

---

## Phase 5：交易接口接入

后期接入：

- 酒店预订接口
- 餐厅预约接口
- 景区门票接口
- 包车 / 接送接口
- DaDa 调度系统
- 支付与订单系统

---

# 十六、商业化节奏

## 前期：免费增长期

目标：

- 做内容
- 做用户
- 做习惯
- 做流量
- 做数据

不急：

- 强广告
- 强交易
- 强付费
- 复杂订单

---

## 中期：轻商业化

方式：

- 合作方轻推荐
- 合作链接跳转
- 内容页自然推荐
- 路线中自然推荐
- DaDa 包车入口
- 酒店/餐厅/门票跳转

---

## 后期：交易闭环

方式：

- 酒店预订
- 餐厅预约
- 门票预订
- 包车下单
- 接送下单
- AI 旅行 Agent
- Partner ROI Dashboard

---

# 十七、最终目标

Japan AI Guide 最终不是单纯的旅游网站。

而是：

# AI 日本旅游流量入口

最终形成：

```text
内容
↓
用户
↓
数据
↓
推荐
↓
信任
↓
交易
↓
合作方网络
```

也就是：

# AI 内容流量 → 用户习惯 → 推荐归因 → 旅游交易

的完整闭环。
