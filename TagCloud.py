# coding=utf-8

from collections import OrderedDict
from math import floor
from random import shuffle
import re


class TagCloud(object):

    # Tag cloud version
    __version__ = '0.0.1'

    # Conversion map
    transliterationTable = {
        u'á': u'a', u'Á': u'A', u'à': u'a', u'À': u'A', u'ă': u'a', u'Ă': u'A', u'â': u'a', u'Â': u'A',
        u'å': u'a', u'Å': u'A', u'ã': u'a', u'Ã': u'A', u'ą': u'a', u'Ą': u'A', u'ā': u'a', u'Ā': u'A',
        u'ä': u'ae', u'Ä': u'AE', u'æ': u'ae', u'Æ': u'AE', u'ḃ': u'b', u'Ḃ': u'B', u'ć': u'c', u'Ć': u'C',
        u'ĉ': u'c', u'Ĉ': u'C', u'č': u'c', u'Č': u'C', u'ċ': u'c', u'Ċ': u'C', u'ç': u'c', u'Ç': u'C',
        u'ď': u'd', u'Ď': u'D', u'ḋ': u'd', u'Ḋ': u'D', u'đ': u'd', u'Đ': u'D', u'ð': u'dh', u'Ð': u'Dh',
        u'é': u'e', u'É': u'E', u'è': u'e', u'È': u'E', u'ĕ': u'e', u'Ĕ': u'E', u'ê': u'e', u'Ê': u'E',
        u'ě': u'e', u'Ě': u'E', u'ë': u'e', u'Ë': u'E', u'ė': u'e', u'Ė': u'E', u'ę': u'e', u'Ę': u'E',
        u'ē': u'e', u'Ē': u'E', u'ḟ': u'f', u'Ḟ': u'F', u'ƒ': u'f', u'Ƒ': u'F', u'ğ': u'g', u'Ğ': u'G',
        u'ĝ': u'g', u'Ĝ': u'G', u'ġ': u'g', u'Ġ': u'G', u'ģ': u'g', u'Ģ': u'G', u'ĥ': u'h', u'Ĥ': u'H',
        u'ħ': u'h', u'Ħ': u'H', u'í': u'i', u'Í': u'I', u'ì': u'i', u'Ì': u'I', u'î': u'i', u'Î': u'I',
        u'ï': u'i', u'Ï': u'I', u'ĩ': u'i', u'Ĩ': u'I', u'į': u'i', u'Į': u'I', u'ī': u'i', u'Ī': u'I',
        u'ĵ': u'j', u'Ĵ': u'J', u'ķ': u'k', u'Ķ': u'K', u'ĺ': u'l', u'Ĺ': u'L', u'ľ': u'l', u'Ľ': u'L',
        u'ļ': u'l', u'Ļ': u'L', u'ł': u'l', u'Ł': u'L', u'ṁ': u'm', u'Ṁ': u'M', u'ń': u'n', u'Ń': u'N',
        u'ň': u'n', u'Ň': u'N', u'ñ': u'n', u'Ñ': u'N', u'ņ': u'n', u'Ņ': u'N', u'ó': u'o', u'Ó': u'O',
        u'ò': u'o', u'Ò': u'O', u'ô': u'o', u'Ô': u'O', u'ő': u'o', u'Ő': u'O', u'õ': u'o', u'Õ': u'O',
        u'ø': u'oe', u'Ø': u'OE', u'ō': u'o', u'Ō': u'O', u'ơ': u'o', u'Ơ': u'O', u'ö': u'oe', u'Ö': u'OE',
        u'ṗ': u'p', u'Ṗ': u'P', u'ŕ': u'r', u'Ŕ': u'R', u'ř': u'r', u'Ř': u'R', u'ŗ': u'r', u'Ŗ': u'R',
        u'ś': u's', u'Ś': u'S', u'ŝ': u's', u'Ŝ': u'S', u'š': u's', u'Š': u'S', u'ṡ': u's', u'Ṡ': u'S',
        u'ş': u's', u'Ş': u'S', u'ș': u's', u'Ș': u'S', u'ß': u'SS', u'ť': u't', u'Ť': u'T', u'ṫ': u't',
        u'Ṫ': u'T', u'ţ': u't', u'Ţ': u'T', u'ț': u't', u'Ț': u'T', u'ŧ': u't', u'Ŧ': u'T', u'ú': u'u',
        u'Ú': u'U', u'ù': u'u', u'Ù': u'U', u'ŭ': u'u', u'Ŭ': u'U', u'û': u'u', u'Û': u'U', u'ů': u'u',
        u'Ů': u'U', u'ű': u'u', u'Ű': u'U', u'ũ': u'u', u'Ũ': u'U', u'ų': u'u', u'Ų': u'U', u'ū': u'u',
        u'Ū': u'U', u'ư': u'u', u'Ư': u'U', u'ü': u'ue', u'Ü': u'UE', u'ẃ': u'w', u'Ẃ': u'W', u'ẁ': u'w',
        u'Ẁ': u'W', u'ŵ': u'w', u'Ŵ': u'W', u'ẅ': u'w', u'Ẅ': u'W', u'ý': u'y', u'Ý': u'Y', u'ỳ': u'y',
        u'Ỳ': u'Y', u'ŷ': u'y', u'Ŷ': u'Y', u'ÿ': u'y', u'Ÿ': u'Y', u'ź': u'z', u'Ź': u'Z', u'ž': u'z',
        u'Ž': u'Z', u'ż': u'z', u'Ż': u'Z', u'þ': u'th', u'Þ': u'Th', u'µ': u'u', u'а': u'a', u'А': u'a',
        u'б': u'b', u'Б': u'b', u'в': u'v', u'В': u'v', u'г': u'g', u'Г': u'g', u'д': u'd', u'Д': u'd',
        u'е': u'e', u'Е': u'e', u'ё': u'e', u'Ё': u'e', u'ж': u'zh', u'Ж': u'zh', u'з': u'z', u'З': u'z',
        u'и': u'i', u'И': u'i', u'й': u'j', u'Й': u'j', u'к': u'k', u'К': u'k', u'л': u'l', u'Л': u'l',
        u'м': u'm', u'М': u'm', u'н': u'n', u'Н': u'n', u'о': u'o', u'О': u'o', u'п': u'p', u'П': u'p',
        u'р': u'r', u'Р': u'r', u'с': u's', u'С': u's', u'т': u't', u'Т': u't', u'у': u'u', u'У': u'u',
        u'ф': u'f', u'Ф': u'f', u'х': u'h', u'Х': u'h', u'ц': u'c', u'Ц': u'c', u'ч': u'ch', u'Ч': u'ch',
        u'ш': u'sh', u'Ш': u'sh', u'щ': u'sch', u'Щ': u'sch', u'ъ': u'', u'Ъ': u'', u'ы': u'y', u'Ы': u'y',
        u'ь': u'', u'Ь': u'', u'э': u'e', u'Э': u'e', u'ю': u'ju', u'Ю': u'ju', u'я': u'ja', u'Я': u'ja'
    }

    def __init__(self, tags=None):
        """
        Takes the tags and calls the correct
        setter based on the type of input

        :param tags: String or Collection of tags
        """

        # Tag array container
        self.tagsArray = {}

        # List of tags to remove from final output
        self.removeTags = []

        # Cached attributes for order comparison
        self.attributes = []

        # Amount to limit cloud by
        self._limit = None

        # Minimum length of string to filtered in string
        self._minLength = None

        # Custom format output of tags
        #
        # transformation: upper and lower for change of case
        # transliterate: True\False
        # trim: bool, applies trimming to tag
        self.options = {
            'transformation': 'lower',
            'transliterate': True,
            'trim': True
        }

        # Custom function to create the tag-output
        self._htmlizeTagFunction = None

        self.orderBy = None

        if tags:
            if isinstance(tags, basestring):
                self.addString(tags)
            elif tags:
                for tag in tags:
                    self.addTag(tag)

    def addString(self, string, separator=' '):
        """
        Convert a string into a array

        :param str string: The string to use
        :param str separator: The separator to extract the tags
        :rtype: TagCloud
        """
        inputArray = string.split(separator)
        tagArray = []
        for inputTag in inputArray:
            tagArray.append(self.formatTag(inputTag))
        self.addTags(tagArray)
        return self

    def setOption(self, option, value):
        """
        Set option value

        :param str option: Option property name
        :param value: New property value
        :rtype: TagCloud
        """
        self.options[option] = value
        return self

    def getOption(self, option):
        """
        Get option by name otherwise return all options

        :param str option: Option property name
        :rtype: list
        """
        if option:
            return self.options[option]
        else:
            return self.options

    def formatTag(self, string):
        """
        Parse tag into safe format

        :param str string: Tag to be formatted
        """
        if self.options['transliterate']:
            string = self.transliterate(string)

        if self.options['transformation']:
            if self.options['transformation'] == 'upper':
                string = string.upper()
            else:
                string = string.lower()

        if self.options['trim']:
            string = string.strip()
        return re.sub(r'[^\w ]', '', string, flags=re.UNICODE)

    def addTag(self, tagAttributes):
        """
        Assign tag to array

        :param dict | list | str | unicode tagAttributes: Tags or tag attributes array
        :rtype: bool
        """
        if tagAttributes is None:
            tagAttributes = {}
        if isinstance(tagAttributes, basestring):
            tagAttributes = {'tag': tagAttributes}
        tagAttributes['tag'] = self.formatTag(tagAttributes['tag'])
        if 'size' not in tagAttributes:
            tagAttributes['size'] = 1
        if 'tag' not in tagAttributes:
            return False
        tag = tagAttributes['tag']
        if not self.tagsArray.get(tag):
            self.tagsArray[tag] = {}

        if self.tagsArray[tag].get('size') and tagAttributes.get('size'):
            tagAttributes['size'] = self.tagsArray[tag]['size'] + tagAttributes['size']
        elif self.tagsArray[tag].get('size'):
            tagAttributes['size'] = self.tagsArray[tag]['size']
        self.tagsArray[tag] = tagAttributes
        self.addAttributes(tagAttributes)
        return self.tagsArray[tag]

    def addAttributes(self, attributes):
        """
        Add all attributes to cached array

        :param attributes:
        :rtype: TagCloud
        """
        self.attributes.extend(attributes)
        self.attributes = list(set(self.attributes))
        return self

    def getAttributes(self):
        """
        Get attributes from cache

        :rtype: list
        :return: A collection of multiple tabs
        """
        return self.attributes

    def addTags(self, tags=None):
        """
        Assign multiple tags to array

        :param list tags: A collection of multiple tabs
        :rtype: TagCloud
        """
        if tags is None:
            tags = []
        if not isinstance(tags, list):
            tags = [tags]
        for tagAttributes in tags:
            self.addTag(tagAttributes)
        return self

    def setMinLength(self, minLength):
        """
        Sets a minimum string length for the tags to display

        :param int minLength: The minimum string length of a tag
        :rtype: TagCloud
        """
        self._minLength = minLength
        return self

    def getMinLength(self):
        """
        Gets the minimum length value

        :rtype: int
        """
        return self._minLength

    def setLimit(self, limit):
        """
        Sets a limit for the amount of clouds

        :param int limit: The maximum number to display
        :rtype: TagCloud
        """
        self._limit = limit
        return self

    def getLimit(self):
        """
        Get the limit for the amount tags to display

        :rtype: int
        :return: The maximum number
        """
        return self._limit

    def setRemoveTag(self, tag):
        """
        Assign a tag to be removed from the array

        :param str tag: The tag value
        :rtype: TagCloud
        """
        self.removeTags.append(self.formatTag(tag))
        return self

    def setRemoveTags(self, tags):
        """
        Remove multiple tags from the array

        :param list tags: A collection of removable tags
        :rtype: TagCloud
        """
        for tag in tags:
            self.setRemoveTag(tag)
        return self

    def getRemoveTags(self):
        """
        Get the list of remove tags

        :rtype: list
        :return: A collection of tags to remove
        """
        return self.removeTags

    def setOrder(self, field, direction='ASC'):
        """
        Assign the order field and order direction of the array

        Order by tag or size / defaults to random

        :param str field: The name of the field to sort by
        :param str direction: The sort direction ASC|DESC
        :rtype: TagCloud
        """
        self.orderBy = {
            'field': field,
            'direction': direction
        }
        return self

    def setHtmlizeTagFunction(self, htmlizeTagFunction):
        """
        Inject a custom function/closure for generating the rendered HTML

        :param htmlizeTagFunction: The function/closure
        :rtype: TagCloud
        """
        self._htmlizeTagFunction = htmlizeTagFunction
        return self

    def render(self, returnType='html'):
        """
        Generate the output for each tag.

        :param str returnType: The type of data to return [html|array]
        :rtype: dict | None | str
        """
        self.remove()
        self.minLength()
        if not self.orderBy:
            self.shuffle()
        else:
            orderDirection = 'SORT_DESC' if self.orderBy['direction'].lower() == 'desc' else 'SORT_ASC'
            self.tagsArray = self.order(self.tagsArray, self.orderBy['field'], orderDirection)
        self.limit()
        maximum = self.getMax()
        if self.tagsArray:
            result = '' if returnType == 'html' else (OrderedDict() if returnType == 'array' else '')
            for tag, arrayInfo in self.tagsArray.items():
                sizeRange = int(self.getClassFromPercent((float(arrayInfo['size']) / maximum) * 100))
                arrayInfo['range'] = sizeRange
                if returnType == 'array':
                    result[tag] = arrayInfo
                elif returnType == 'html':
                    result += self.htmlizeTag(arrayInfo, str(sizeRange))
            return result
        return None

    def htmlizeTag(self, arrayInfo, sizeRange):
        """
        Convert a tag into an html-snippet

        This function is mainly an anchor to decide if a user-supplied
        custom function should be used or the normal output method.

        :param dict arrayInfo: The data to pass into the closure
        :param str sizeRange: The size to pass into the closure
        :rtype: str
        """
        htmlizeTagFunction = self._htmlizeTagFunction
        if htmlizeTagFunction and callable(htmlizeTagFunction):
            # this cannot be written in one line or the PHP interpreter will puke
            # apparently, it's okay to have a function in a variable,
            # but it's not okay to have it in an instance-variable.
            return htmlizeTagFunction(arrayInfo, sizeRange)
        else:
            return "<span class='tag size{:s}'> &nbsp; {:s} &nbsp; </span>".format(sizeRange, arrayInfo['tag'])

    def remove(self):
        """
        Removes tags from the whole array
        :rtype: dict
        :return: The tag array excluding the removed tags
        """
        _tagsArray = {}
        for key, value in self.tagsArray.items():
            if not value['tag'] in self.getRemoveTags():
                _tagsArray[value['tag']] = value
        self.tagsArray = {}
        self.tagsArray = _tagsArray
        return self.tagsArray

    def order(self, unsortedArray, sortField, sortWay='SORT_ASC'):
        """
        Orders the cloud by a specific field

        :param dict unsortedArray: Collection of unsorted data
        :param str sortField: The field that should be sorted
        :param str sortWay: The direction to sort the data [SORT_ASC|SORT_DESC]
        """
        sortedArray = {}
        for uniqid, row in unsortedArray.items():
            for attr in self.getAttributes():
                sortedArray.setdefault(attr, {})
                if row.get(attr):
                    sortedArray[attr][uniqid] = unsortedArray[uniqid][attr]
                else:
                    sortedArray[attr][uniqid] = None

        if sortWay:
            sortFields = sortedArray[sortField].items()
            sortedArray = OrderedDict()
            for key in OrderedDict(sorted(sortFields, key=lambda t: t[0], reverse=(sortWay == 'SORT_ASC'))).keys():
                sortedArray[key] = unsortedArray[key]
            return sortedArray
        return unsortedArray

    def limit(self):
        """
        Parses the array and returns limited amount of items

        :rtype: dict
        :return: The collection limited to the amount defined
        """
        limit = self.getLimit()
        if limit:
            i = 0
            _tagsArray = {}
            for key, value in self.tagsArray.items():
                if i < limit:
                    _tagsArray[value['tag']] = value
                i += 1
            self.tagsArray = {}
            self.tagsArray = _tagsArray
        return self.tagsArray

    def minLength(self):
        """
        Reduces the array by removing strings with a
        length shorter than the minLength

        :rtype: dict
        :return: The collection of items within
        the string length boundaries
        """
        limit = self.getMinLength()
        if limit:
            i = 0
            _tagsArray = {}
            for key, value in self.tagsArray.items():
                if len(value['tag']) >= limit:
                    _tagsArray[value['tag']] = value
                i += 1
            self.tagsArray = {}
            self.tagsArray = _tagsArray
        return self.tagsArray

    def getMax(self):
        """
        Finds the maximum 'size' value of an array

        :rtype: int
        :return: The maximum size value in the entire collection
        """
        maximum = 0
        if self.tagsArray:
            p_size = 0
            for cKey, cVal in self.tagsArray.items():
                c_size = cVal['size']
                if c_size > p_size:
                    maximum = c_size
                    p_size = c_size
        return maximum

    def shuffle(self):
        """
        Shuffle associated names in array

        :rtype: dict
        :return: The shuffled collection
        """
        keys = self.tagsArray.keys()
        shuffle(keys)
        if keys and isinstance(keys, list):
            tmpArray = self.tagsArray
            self.tagsArray = {}
            for value in keys:
                self.tagsArray[value] = tmpArray[value]
        return self.tagsArray

    def getClassFromPercent(self, percent):
        """
        Get the class range using a percentage

        :param int | float percent:
        :rtype: int | float
        :return: The respective class name based on the percentage value
        """
        cls = floor(percent / 10)
        if percent >= 5:
            cls += 1

        if 80 <= percent < 100:
            cls = 8
        elif percent == 100:
            cls = 9
        return cls

    def calculateClassFromPercent(self, percent):
        """
        Calculate the class given to a tag from the
        weight percentage of the given tag.

        :param int percent: The percentage value
        :rtype: float | int
        """
        return self.getClassFromPercent(percent)

    def transliterate(self, string):
        """
        Convert accented chars into basic latin chars
        @see http://stackoverflow.com/questions/6837148/change-foreign-characters-to-normal-equivalent

        :param str string: Non transliterated string
        :return: Transliterated string
        """
        for search, replace in TagCloud.transliterationTable.items():
            string = string.replace(search, replace)
        return string
