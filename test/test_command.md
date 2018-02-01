1. 运行 py.test  
执行测试时需要下面几步：  
* 从命令行进入测试文件所在目录，pytest会在该目录中寻找以test开头的文件  
* 找到测试文件，进入测试文件中寻找以test_开头的函数并执行  
* 测试函数以断言assert结尾  

2. 运行 py.test -q test_class.py  
下面的-q是 quiet的意思,就是忽略一些很细节的信息
使用测试类时，注意下面几点：
* 测试类所在的文件以test_开头
* 测试类以Test开头，并且不能带有__init__方法
* 类中测试函数以test_开头
* 测试函数以assert断言结尾

3. 运行 py.test -q test_params.py
说明：
* params是要进行测试的参数list，其中元素为tuple，每个tuple对应一套参数
* @pytest.mark.parametrize装饰器的第一个参数是一个字符串，不过这个字符串其实是以逗号分隔的一组参数，这个参数就是其所装饰的函数的参数。
* @pytest.mark.parametrize装饰器将params中的参数一套一套拿出来放入其所装饰的函数中执行

4. 运行 py.test -q fixture_params.py
说明：
* 把一个函数定用@pytest.fixture装饰，那这个函数就是fixture函数  
* 一个fixture函数可以被其他测试函数调用，将函数名当作参数即可，fixture的返回值会当作测试函数的参数  
* fixture函数中的params字段默认为None，如果有值，则每个值都会调用执行一次  
