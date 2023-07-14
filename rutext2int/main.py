from .worker import T2IWorker, TextElem
from .my_data import MY_CONST


class Text2IntSpecial:

    def __init__(self):
        self.data = []
        data = MY_CONST["special"]

        print(data)
        for elem in data:
            self.data.append(Text2IntUnit(**elem))

    def get_value(self, src_title):
        result = None
        for elem in self.data:
            result = elem.get_value(src_title=src_title)
            if result != None:
                break
        return result


class Text2IntNum:
    def __init__(self, **kwargs):
        self._value = kwargs.get("value", None)
        self._degree = T2IWorker.degree(self._value)

    def __str__(self):
        return str(self.value)

    @property
    def degree(self):
        return self._degree

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, num):
        self._value = num
        self._degree = T2IWorker.degree(self._value)

    @property
    def exist(self) -> bool:
        if self._value == None:
            result = False
        else:
            result = True
        return result


class Text2IntRU:
    def __init__(self, **kwargs):
        self.text2intdict = kwargs.get("dict", Text2IntDict())
        # self.text = T2IWorker.split_text(**kwargs)
        # self.text.append("###")

    def parse_pure(self, text):
        src_text = T2IWorker.split_text(text=text)
        src_text.append(TextElem(pure="###", morph="###"))
        ua_num = Text2IntNum(value=None)
        ua_res = []
        for elem in src_text:
            elem: TextElem = elem
            temp_num = Text2IntNum(value=self.text2intdict.get_value(elem.morph))
            # print(f"temp_num = {temp_num}")
            if not temp_num.exist:
                if not ua_num.exist:
                    ua_res.append(elem.pure)
                    continue
                else:
                    ua_res.append(f"{ua_num}")
                    ua_num = Text2IntNum(value=None)
                    ua_res.append(elem.pure)
                continue
            if not ua_num.exist:
                ua_num = temp_num
                continue
            if ua_num.degree > temp_num.degree:
                ua_num.value = ua_num.value + temp_num.value
            elif temp_num.value == 1000 and ua_num.value < 3:
                ua_num.value = ua_num.value*1000
            else:
                ua_res.append(f"{ua_num}")
                ua_num = temp_num
        ua_res = ua_res[:-1]
        return ua_res

    def parse(self, text):
        res_list = self.parse_pure(text=text)
        result = " ".join(res_list)
        return result


class Text2IntDict:
    def __init__(self):
        self.data = []
        data = MY_CONST["text2int"]
        for elem in data:
            self.data.append(Text2IntUnit(**elem))

    def get_value(self, src_title):
        result = None
        for elem in self.data:
            result = elem.get_value(src_title=src_title)
            if result != None:
                break
        return result


class Text2IntUnit:
    def __init__(self, **kwargs):
        self.title = kwargs["title"]
        self.value = kwargs["value"]

    def get_value(self, src_title):
        result = None
        if src_title in self.title:
            result = self.value
        return result


if __name__ == "__main__":
    new = Text2IntRU()
    print(new.parse("родился он в  двух тысячном триста двенадцатом году от сотворения мира в семь сорок восемь утра"))
