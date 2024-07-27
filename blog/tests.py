from django.test import TestCase
import json
from pprint import pprint

# Create your tests here.
body = '''{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Wow, this editor instance exports its content as JSON."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "asdglasdg"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "asdlgasj"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "dgaslkdgjlasdjg"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "asdg"
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {
        "level": 1
      },
      "content": [
        {
          "type": "text",
          "text": "dalsdkgjasldg"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "ㅇㅁㄴㅇㄻㄴㅇㄹ"
        }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "dasldjg"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "# # # -asdg"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "paragraph"
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph"
            }
          ]
        }
      ]
    },
    {
      "type": "orderedList",
      "attrs": {
        "start": 1
      },
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "asdlkjgasdg"
                }
              ]
            },
            {
              "type": "orderedList",
              "attrs": {
                "start": 1
              },
              "content": [
                {
                  "type": "listItem",
                  "content": [
                    {
                      "type": "paragraph",
                      "content": [
                        {
                          "type": "text",
                          "text": "dkaljsdg"
                        }
                      ]
                    },
                    {
                      "type": "orderedList",
                      "attrs": {
                        "start": 1
                      },
                      "content": [
                        {
                          "type": "listItem",
                          "content": [
                            {
                              "type": "paragraph",
                              "content": [
                                {
                                  "type": "text",
                                  "text": "lkgjsd"
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "type": "listItem",
                          "content": [
                            {
                              "type": "paragraph",
                              "content": [
                                {
                                  "type": "text",
                                  "text": "ㅇㅁㄴㅇㄻㄴㅇㄹ"
                                }
                              ]
                            },
                            {
                              "type": "orderedList",
                              "attrs": {
                                "start": 1
                              },
                              "content": [
                                {
                                  "type": "listItem",
                                  "content": [
                                    {
                                      "type": "paragraph",
                                      "content": [
                                        {
                                          "type": "text",
                                          "text": "ㅇㅁㄴ읾ㄴㅇㄹ"
                                        }
                                      ]
                                    },
                                    {
                                      "type": "bulletList",
                                      "content": [
                                        {
                                          "type": "listItem",
                                          "content": [
                                            {
                                              "type": "paragraph",
                                              "content": [
                                                {
                                                  "type": "text",
                                                  "text": "dasdf"
                                                }
                                              ]
                                            },
                                            {
                                              "type": "bulletList",
                                              "content": [
                                                {
                                                  "type": "listItem",
                                                  "content": [
                                                    {
                                                      "type": "paragraph",
                                                      "content": [
                                                        {
                                                          "type": "text",
                                                          "text": "dasd"
                                                        }
                                                      ]
                                                    }
                                                  ]
                                                },
                                                {
                                                  "type": "listItem",
                                                  "content": [
                                                    {
                                                      "type": "paragraph"
                                                    }
                                                  ]
                                                }
                                              ]
                                            }
                                          ]
                                        }
                                      ]
                                    },
                                    {
                                      "type": "orderedList",
                                      "attrs": {
                                        "start": 1
                                      },
                                      "content": [
                                        {
                                          "type": "listItem",
                                          "content": [
                                            {
                                              "type": "paragraph",
                                              "content": [
                                                {
                                                  "type": "text",
                                                  "text": "aalksd"
                                                }
                                              ]
                                            },
                                            {
                                              "type": "bulletList",
                                              "content": [
                                                {
                                                  "type": "listItem",
                                                  "content": [
                                                    {
                                                      "type": "paragraph",
                                                      "content": [
                                                        {
                                                          "type": "text",
                                                          "text": "dasdf"
                                                        }
                                                      ]
                                                    }
                                                  ]
                                                }
                                              ]
                                            }
                                          ]
                                        }
                                      ]
                                    }
                                  ]
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "type": "listItem",
                          "content": [
                            {
                              "type": "paragraph",
                              "content": [
                                {
                                  "type": "text",
                                  "text": "sdg"
                                }
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "orderedList",
      "attrs": {
        "start": 3
      },
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "dasdf"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "asdf"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph"
            }
          ]
        }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "asdgjasdg"
                }
              ]
            },
            {
              "type": "bulletList",
              "content": [
                {
                  "type": "listItem",
                  "content": [
                    {
                      "type": "paragraph",
                      "content": [
                        {
                          "type": "text",
                          "text": "dalksjdg"
                        }
                      ]
                    },
                    {
                      "type": "bulletList",
                      "content": [
                        {
                          "type": "listItem",
                          "content": [
                            {
                              "type": "paragraph",
                              "content": [
                                {
                                  "type": "text",
                                  "text": "asdl"
                                },
                                {
                                  "type": "text",
                                  "marks": [
                                    {
                                      "type": "bold"
                                    }
                                  ],
                                  "text": "kgjalskdg"
                                }
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}'''

body2 = '''{'content': [{'attrs': {'level': 2},
              'content': [{'text': 'How to monthy?', 'type': 'text'}],
              'type': 'heading'},
             {'content': [{'text': '클릭해서 바로 수정할 수 있어요. ', 'type': 'text'}],
              'type': 'paragraph'},
             {'content': [{'text': 'monthy의 핵심은 ', 'type': 'text'},
                          {'marks': [{'type': 'bold'}],
                           'text': '별표',
                           'type': 'text'},
                          {'text': ' 버튼! ⭐️ (수정할 때만 보여요)', 'type': 'text'}],
              'type': 'paragraph'},
             {'content': [{'text': '이렇게 ', 'type': 'text'},
                          {'marks': [{'type': 'thumb'}],
                           'text': '마음에 드는 문장',
                           'type': 'text'},
                          {'text': '을 ', 'type': 'text'},
                          {'marks': [{'type': 'bold'}],
                           'text': '드래그',
                           'type': 'text'},
                          {'text': '해서 ', 'type': 'text'},
                          {'marks': [{'type': 'underline'}],
                           'text': '제목',
                           'type': 'text'},
                          {'text': '을 지정할 수도 있구요, 오늘의 ', 'type': 'text'},
                          {'marks': [{'type': 'underline'}],
                           'text': '대표 사진',
                           'type': 'text'},
                          {'text': '을 설정할 수도 있어요!', 'type': 'text'}],
              'type': 'paragraph'},
             {'type': 'paragraph'},
             {'type': 'paragraph'},
             {'type': 'paragraph'},
             {'content': [{'text': '     추신. 달력 위 배너 사진을 넣을 수 있어요.',
                           'type': 'text'}],
              'type': 'paragraph'}],
 'type': 'doc'}'''
EMPTY_DICT = {'type': 'text', 'text': '\n'}

def type_paragraph(paragraph, new_body : list, prefix = ''):
    content = paragraph.get('content')
    if content is None:
        new_body.append({'type': 'text', 'text': prefix +'\n'})
        return new_body
    temp_text = ""
    for text in content:
        if text['type'] == 'text':
            temp_text += str(text['text'])
    if prefix == '':
        new_dict = {'type': 'text', 'text': temp_text}
    else:
        new_dict = {'type': 'text', 'text': prefix + ' ' + temp_text}
    new_body.append(new_dict)
    return new_body

def type_heading(heading, new_body : list):
    content = heading.get('content')
    if content is None:
        new_body.append(EMPTY_DICT)
        return new_body
    temp_text = ""
    for text in content:
        if text['type'] == 'text':
            temp_text += str(text['text'])
    new_dict = {'type': 'text', 'text': temp_text}
    new_body.append(new_dict)
    return new_body

def type_bullet_list(bullet_list, new_body : list, prefix = ''):
    content = bullet_list.get('content')
    if content is None:
        new_body.append(EMPTY_DICT)
        return new_body
    for item in content:
        if item['type'] == 'listItem':
            _content = item.get('content')
            if _content is None:
                new_body.append(EMPTY_DICT)
                continue
            for page in _content:
                if page['type'] == 'paragraph':
                    new_body = type_paragraph(page, new_body, prefix + '- ')
                elif page['type'] == 'bulletList':
                    new_body = type_bullet_list(page, new_body, prefix + '  ')
                elif page['type'] == 'orderedList':
                    new_body = type_ordered_list(page, new_body, prefix + '  ')
    return new_body

def type_ordered_list(ordered_list, new_body : list, prefix = ''):
    content = ordered_list.get('content')
    attr = ordered_list.get('attrs')
    start = int(attr['start'])
    if content is None:
        new_body.append(EMPTY_DICT)
        return new_body
    for item in content:
        if item['type'] == 'listItem':
            _content = item.get('content')
            if _content is None:
                new_body.append(EMPTY_DICT)
                continue
            for page in _content:
                if page['type'] == 'paragraph':
                    new_body = type_paragraph(page, new_body, prefix + str(start) + '. ')
                elif page['type'] == 'orderedList':
                    new_body = type_ordered_list(page, new_body, prefix + '   ')
                elif page['type'] == 'bulletList':
                    new_body = type_bullet_list(page, new_body, prefix + '   ')
            start += 1
    return new_body


def change_body_str(body_str) -> str:
    body_dict = json.loads(body_str)
    new_body = []
    for page in body_dict['content']: 
        try:
            if page['type'] == 'heading':
                new_body = type_heading(page, new_body)
            elif page['type'] == 'paragraph':
                new_body = type_paragraph(page, new_body)
            elif page['type'] == 'image':
                src = page['attrs']['src']
                new_dict = {'type': 'image', 'src': src}
                new_body.append(new_dict)
            elif page['type'] == 'bulletList':
                new_body = type_bullet_list(page, new_body)
            elif page['type'] == 'orderedList':
                new_body = type_ordered_list(page, new_body)
        except:
            pass
    new_body_json = json.dumps(new_body, ensure_ascii=False)
    return new_body_json
str = change_body_str(body.replace("'", '"'))
json = json.loads(str)
pprint(json)