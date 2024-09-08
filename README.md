适用于Windows系统
该工具是作者在学习网络爬虫时做的小工具，主要功能为批量爬取百度帖子中的所有图片的原图片（不是缩略图）。
为了规避百度贴吧对爬虫的工具，所以使用了谷歌浏览器自动化工具。
使用方法：
--第一次使用先配置config.json，将chromedriver.exe完整路径设置为"driver_path"的key值
--打开文件夹下的setup.bat
--按格式要求输入贴吧网址
--此时会自动让弹出的谷歌浏览器进入帖子画面，他可能会要求登录百度账号。您可以选择登录，也可以选择关闭登陆弹窗，点击左上角的刷新按钮刷新一次浏览器页面。
--等待获取网页源代码
--按要求选择工作参数
--输出结果将保存到output文件夹

--------------------------------------------------
This tool is a small utility created by the author while learning web scraping. Its main function is to batch scrape all original images (not thumbnails) from Baidu Tieba posts.
To avoid detection by Baidu Tieba's anti-scraping measures, it uses Google Chrome's automation tool.
Usage Instructions:
--For the first use, configure config.json by setting the complete path of chromedriver.exe as the value for the key "driver_path".
--Open setup.bat in the folder.
--Enter the Tieba URL as required by the format.
-At this point, the Google Chrome browser will automatically open and navigate to the post page. It may prompt you to log in to your Baidu account. You can choose to log in or close the login popup and click the refresh button in the top left corner to refresh the browser page.
--Wait for the webpage source code to be retrieved.
--Select the working parameters as required.
--The output results will be saved in the output folder.
