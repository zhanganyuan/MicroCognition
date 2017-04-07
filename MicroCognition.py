import urllib.error
import urllib.parse
import urllib.request

content_type = {'json': 'application/json',
                'stream': 'application/octet-stream',
                'from-data': 'multipart/form-data',
                'form-urlencoded': 'application/x-www-form-urlencoded'}


def get_body_json(key, data):
    """{"url":"http://example.com/images/test.jpg"}
    :param data: 
    :param key: 
    """
    return str({key: data}).encode('utf-8')


def generate_body(data, type_list, json_key):
    """
        生成请求的body
    :param data: 
    :param type_list: 
    :param json_key: 
    :return: 
    """
    if isinstance(data, str):
        c_type = content_type[type_list[0]]
        body = get_body_json(json_key, data)
    elif isinstance(data, bytes):
        c_type = content_type[type_list[1]]
        body = data
    else:
        # 不支持的data类型
        return None
    return body, c_type


class MicroCognition:
    """
    这是一个微软认知API的轮子。
    如果你需要扩展这个轮子，你所需要做的只是补充api_***，
    api_***的格式如下：
    {
     'API Name': ['Request url',
                [supported Content-type key in content_type like: 'json', 'stream' ],
                {
                Default Request params like:  
                    'language': 'unk',
                    'detectOrientation': 'true'
                },
                supported Content-type of application/json key like:
                'url'],
    }
    """
    api_computer_vision = {
        'OCR': ['https://westus.api.cognitive.microsoft.com/vision/v1.0/ocr?{}',
                ['json', 'stream'],
                {
                    'language': 'unk',
                    'detectOrientation': 'true'
                },
                'url'],
        'Analyze': ['https://westus.api.cognitive.microsoft.com/vision/v1.0/analyze?{}',
                    ['json', 'stream'],
                    {
                        'visualFeatures': 'Categories,Description,Tags,Faces,ImageType,Color,Adult',
                        'details': 'Celebrities',
                        'language': 'en'
                    },
                    'url'],
    }
    api_face = {
        'Detect': ['https://westus.api.cognitive.microsoft.com/face/v1.0/detect?{}',
                   ['json', 'stream'],
                   {
                       'returnFaceId': 'true',
                       'returnFaceLandmarks': 'false',
                       'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion'
                   },
                   'url'],
    }

    def __init__(self):
        pass

    @staticmethod
    def generate_url_body(mode, data, params):
        """
        根据url生成完整的url,如果params为None则使用默认参数
        :param data: 
        :param params: 用户可指定的url参数
        :return: 
        """
        url, type_list, json_key = mode[0], mode[1], mode[3]
        if params is None:
            params = urllib.parse.urlencode(mode[2])
        body, c_type = generate_body(data, type_list, json_key)
        return url.format(params), body, c_type

    @staticmethod
    def call_api(mode, key, data, params=None):
        full_url, body, c_type = MicroCognition.generate_url_body(mode, data, params)
        headers = {
            'Content-Type': c_type,
            'Ocp-Apim-Subscription-Key': key,
        }
        try:
            print(full_url)
            print(body)
            print(headers)
            req = urllib.request.Request(full_url, data=body,
                                         headers=headers)
            resp = urllib.request.urlopen(req)
            return resp.read()
        except Exception as e:
            print("[error {0}] {1}".format(e.__cause__, e.__context__))


if __name__ == '__main__':
    link = 'http://i4.buimg.com/567571/06b5fe7021dc8be7.jpg'
    ret_data = MicroCognition.call_api(MicroCognition.api_computer_vision['OCR'], '9929dc10dc534c3084e7b65e800167a3',
                                       link)
    print(ret_data)
