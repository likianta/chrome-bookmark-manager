# Chrome 书签美化工具

本工具用于净化书签标题格式, 以及加速导入过程.

**净化书签标题:**

- 中文符号变为英文符号
- 删除多余的空格
- 放松紧凑的标点
- 统一标题中的分隔符
- 字母全小写 (可选)

**加速导入:**

经本工具生成的净化后的 html 文件, 打开和导入速度均有提升.

测试 4000 条书签的打开速度, 比原始的书签文件快上数倍, 导入速度也有小幅提升.

**使用方法:**

1. Chrome 导出书签到本地
2. 在 Chrome 中打开此书签文件, 按 f12 查看源码, 并复制源码到 data/bookmark.html
3. 运行 src/app.py
4. 生成文件: data/bookmark.json, output/bookmark_prettified.html
5. 将 output/bookmark_prettified.html 导入到浏览器即可
