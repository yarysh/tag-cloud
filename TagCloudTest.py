# coding=utf-8

import unittest

from TagCloud import TagCloud


class TagCloudTest(unittest.TestCase):
    def testEmptyTagCloudRendersNull(self):
        """Tests invoke of class without any tags supplied"""
        tagCloud = TagCloud()
        self.assertEquals(None, tagCloud.render())

    def testAddingMultipleTagsIncreasesSizeKey(self):
        """Tests size increment of tag entity"""
        tagCloud = TagCloud()
        tagCloud.addTag('Foo')
        tagCloud.addTag('Foo')
        rendered = tagCloud.render('array')
        self.assertEquals(2, rendered['foo']['size'])

    def testTagCloudCreatedFromContructor(self):
        """
        Tests creation of cloud with tags
        provided directly to the contructor
        """
        tags = ['foo', 'bar', 'baz']
        tagCloud = TagCloud(tags)
        rendered = tagCloud.render('array')
        for item in tags:
            self.assertTrue(item in rendered)

    def testCustomTagEntity(self):
        tagCloud = TagCloud()
        self.assertEquals(0, tagCloud.calculateClassFromPercent(0))
        self.assertEquals(1, tagCloud.calculateClassFromPercent(5))
        self.assertEquals(2, tagCloud.calculateClassFromPercent(10))
        self.assertEquals(3, tagCloud.calculateClassFromPercent(20))
        self.assertEquals(4, tagCloud.calculateClassFromPercent(30))
        self.assertEquals(5, tagCloud.calculateClassFromPercent(40))
        self.assertEquals(6, tagCloud.calculateClassFromPercent(50))
        self.assertEquals(7, tagCloud.calculateClassFromPercent(60))
        self.assertEquals(8, tagCloud.calculateClassFromPercent(70))
        self.assertEquals(8, tagCloud.calculateClassFromPercent(80))
        self.assertEquals(8, tagCloud.calculateClassFromPercent(90))
        self.assertEquals(9, tagCloud.calculateClassFromPercent(100))

    def testRemovalOfTag(self):
        tagCloud = TagCloud()
        tagCloud.addTags(['test', 'removal', 'tags'])
        tagCloud.setRemoveTag('test')
        self.assertFalse('test' in tagCloud.render('array'))

    def testCustomAttributes(self):
        tagCloud = TagCloud()
        tags = [
            {
                'tag': 'Hello',
                'url': 'http://hello.com'
            },
            {
                'tag': 'World',
                'url': 'http://world.com'
            },
        ]
        for tag in tags:
            tagCloud.addTag(tag)
        rendered = tagCloud.render('array')
        self.assertEquals('http://hello.com', rendered['hello']['url'])
        self.assertEquals('http://world.com', rendered['world']['url'])

    def testOrderingBySize(self):
        tagCloud = TagCloud()
        tagCloud.addTag("hello")
        tagCloud.addTag("hello")
        tagCloud.addTag("hello")
        tagCloud.addTag("beautiful")
        tagCloud.addTag("beautiful")
        tagCloud.addTag("beautiful")
        tagCloud.addTag("world")
        tagCloud.setOrder('size', 'DESC')
        cloud = tagCloud.render('array')
        keys = cloud.keys()
        self.assertEquals("beautiful", keys[0])
        self.assertEquals("hello", keys[1])
        self.assertEquals("world", keys[2])

    def testHtmlizeFunction(self):
        tagCloud = TagCloud()
        tagCloud.addTag('Howdy')

        # default
        expected = "<span class='tag size9'> &nbsp; howdy &nbsp; </span>"
        self.assertEquals(expected, tagCloud.render())

        # custom htmlize function
        htmlizeCloud = TagCloud()
        htmlizeCloud.addTag("Howdy")
        htmlizeCloud.setHtmlizeTagFunction(lambda arrayInfo, sizeRange: '<p>{:s}</p>'.format(arrayInfo['tag']))
        self.assertEquals("<p>howdy</p>", htmlizeCloud.render('html'))

    def testEmptyAttributeCache(self):
        tagCloud = TagCloud()
        attributes = tagCloud.getAttributes()
        self.assertNotIn('tag', attributes)
        self.assertNotIn('size', attributes)

    def testAttributeCache(self):
        tagCloud = TagCloud()
        tagCloud.addTag("Howdy")
        attributes = tagCloud.getAttributes()
        self.assertIn('tag', attributes)
        self.assertIn('size', attributes)

    def testCustomAttributeCache(self):
        tagCloud = TagCloud()
        tagCloud.addTag({"tag": "Howdy", "description": "Greeting"})
        attributes = tagCloud.getAttributes()
        self.assertIn('tag', attributes)
        self.assertIn('size', attributes)
        self.assertIn('description', attributes)
        cloud = tagCloud.render("array")
        self.assertEquals("Greeting", cloud['howdy']['description'])

    def testNoTransliterate(self):
        tagCloud = TagCloud()
        tagCloud.setOption('transliterate', False)
        self.assertEquals(tagCloud.getOption("transliterate"), False)
        tagCloud.addTag('example')
        tagCloud.addTag(u'éxample')
        cloud = tagCloud.render("array")
        self.assertEquals(2, len(cloud))
        self.assertIn('example', cloud)
        self.assertIn(u'éxample', cloud)

    def testTransliterate(self):
        tagCloud = TagCloud()

        # transliterate should be default behaviour
        tagCloud.setOption('transliterate', True)
        self.assertEquals(tagCloud.getOption("transliterate"), True)

        tagCloud.addTag('myexample')
        tagCloud.addTag(u'myéxample')

        cloud = tagCloud.render("array")

        self.assertEquals(1, len(cloud))
        self.assertIn('myexample', cloud)
        self.assertNotIn(u'myéxample', cloud)

    def testAddString(self):
        tagCloud = TagCloud()
        tagCloud.addString('This is a tag-cloud script, written by Del Harvey. I wrote this tag-cloud class because I just love writing code')
        rendered = tagCloud.render('array')
        self.assertEquals(17, len(rendered))

    def testRemovalOfTags(self):
        tagCloud = TagCloud()
        tagCloud.addTags(['test', 'removal', 'tags'])
        tagCloud.setRemoveTags(['test', 'tags'])
        rendered = tagCloud.render('array')
        self.assertTrue('removal' in rendered)
        self.assertEquals(1, len(rendered))

    def testSetMinLength(self):
        tagCloud = TagCloud()
        tagCloud.addTags(['test', 'removal', 'tags'])
        tagCloud.setMinLength(5)
        self.assertEquals(1, len(tagCloud.render('array')))

    def testSetLimit(self):
        tagCloud = TagCloud()
        tagCloud.addTags(['test', 'removal', 'tags'])
        tagCloud.setLimit(1)
        self.assertEquals(1, len(tagCloud.render('array')))

    def testSize(self):
        tagCloud = TagCloud()
        tagCloud.addTags(['test', 'removal', 'tags', 'test', 'test'])
        cloud = tagCloud.render('array')
        self.assertEquals(4, cloud['tags']['range'])
        self.assertEquals(1, cloud['tags']['size'])
        self.assertEquals(4, cloud['removal']['range'])
        self.assertEquals(1, cloud['removal']['size'])
        self.assertEquals(9, cloud['test']['range'])
        self.assertEquals(3, cloud['test']['size'])


if __name__ == '__main__':
    unittest.main()
