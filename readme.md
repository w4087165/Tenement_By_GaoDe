# 基于高德地图API，解决租房问题
# 开发时间 开始-》9.04  结束：
# 技术
  前后端分离
        前端：flask 框架 返回静态页面
                1.通过高德地图API，创建地图
                2.添加搜索条件框，同步ajax请求
                3.拿到后端返回数据后，在高德地图中显示
                4.标记地图显示房屋信息后 点击标记点显示
                 显示具体内容：
                        4.1 房屋出租类型：（整租|合租）
                        4.2 价格
                        4.3 网站链接
                        4.4 可扩展× 一张改房屋照片
                5.后期补充
        后端：django 框架后端 负责返回前端需要数据
		1.负责爬取网页数据（具体：58同城 我爱我家 链家 **可再多）
		2.创建数据库 存贮数据 
		3.接受前段网页请求，返回需要数据。（逻辑处理 具体）
## 实现步骤     4.
