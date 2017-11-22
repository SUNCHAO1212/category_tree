挂类目树流程：
tree.py: 从文件中读入类目树，不同层以'\t'隔开，生成带有层级关系的 idpath，并存放在 MySQL 中（如果MySQL中有记录，需要先清理，然后生成）。
        其中类目树层级为第三级（关键字）及后续细化，文件格式见"a.txt"
write_dict.py: 从 MySQL 中读出上面的记录，并读取类目树前两级，将完整类目树进行合并。
        其中"level1", "level2", "idpath" 分别为：一级类目，二级类目，三级类目细化路径，"word"为当前关键字，可以是第三到五级的词，
        一个关键字的"idpath" 和 "id" 会有多个
event_test.py: 测试类目树挂载结果：读上面产生的完整类目树，存放到AC自动机内；选取标题，将标题中挂到类目树上，并产生多个 idpath ，
        记录在"log_files/result.json"中，未挂上的记录在"log_files/missed.txt"中。现有策略为选择每个不同关键字中最长的 idpath.
