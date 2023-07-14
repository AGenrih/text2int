import logging
import os
import sys
import razdel
import yaml
import pymorphy2


class TextElem:
    def __init__(self, **kwargs):
        self._morph: str = kwargs["morph"]
        self._pure: str = kwargs["pure"]

    @property
    def morph(self) -> str:
        return self._morph

    @property
    def pure(self) -> str:
        return self._pure


class T2IWorker:

    @staticmethod
    def prepare_title(**kwargs):
        tmp_result = T2IWorker.split_text(**kwargs)
        result = []
        for tmp_elem in tmp_result:
            # elem = Porter.stem(tmp_elem)
            result.append(tmp_elem)
        return result

    @staticmethod
    def degree(src_num):
        result = None
        if src_num == 0:
            return 0
        try:
            tmp_res = None
            i = 0
            while not tmp_res and i < 10:
                i += 1
                tmp_res = src_num % 10**i
            # for i in range(3):
            #     if src_num % 10**i > 0:
            #         result = i
            #         break
            result = tmp_res - 1
        except:
            result = None
        return result

    @staticmethod
    def split_text(**kwargs) -> list:
        text = kwargs['text'].lower()
        pure_res = []
        tokens = razdel.tokenize(text=text)
        last = 0
        tokens = list(tokens)
        for i in range(len(tokens)):
            if (
                last
                and tokens[i].start == last
                and str(tokens[i].text).lower() not in (':', ',', '.')
            ):
                pure_res[-1] += str(tokens[i].text).lower()
            elif (
                    last
                    and tokens[i].start == last
                    and str(tokens[i].text).lower() in (':', ',', '.')
                    and T2IWorker._str_number(tokens[i - 1].text)
                    and i + 1 < len(tokens)
                    and T2IWorker._str_number(tokens[i + 1].text)
            ):
                pure_res[-1] += str(tokens[i].text).lower()
            else:
                pure_res.append(str(tokens[i].text).lower())
            last = tokens[i].stop
        morph_res = [pymorphy2.MorphAnalyzer().parse(word=word)[0].normal_form for word in pure_res]
        result = []
        for i in range(len(pure_res)):
            result.append(TextElem(pure=pure_res[i], morph=morph_res[i]))
        return result

    @staticmethod
    def _str_number(src_str: str):
        try:
            float(src_str)
            return 1
        except:
            return 0





