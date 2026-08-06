from lxml import etree
from datetime import datetime 

def parse_xml(file_path:str): 
    tree = etree.parse(file_path) #파일 읽기
    root = tree.getroot()         #최상위 태그 찾기
    item_count = int(root.findtext("./Header/ItemCount"))
    records = root.xpath(".//EstablishmentDetail")

    target_tags = ["FHRSID", "BusinessName", "RatingDate", "PostCode", "RatingValue", "LocalAuthorityCode", "LocalAuthorityName"] 

    result_list = []

    for record in records:
        record_dict = {} 
        for tag in target_tags:
            node = record.find(tag)
            # node가 존재하고 text가 있을 때만 strip(), 없으면 None 반환
            text_value = node.text.strip() if (node is not None and node.text) else None
            # text_value가 None이거나 빈 문자열("")이면 None 저장 후 넘어감
            if not text_value:
                record_dict[tag] = None 
                continue 
            try: 
                if tag == "RatingDate":
                    record_dict[tag] = datetime.strptime(text_value, '%Y-%m-%d').date() # date() 연월일까지만 남기려고 
                else:
                    record_dict[tag] = str(text_value)
            except ValueError:
                record_dict[tag] = None
        result_list.append(record_dict)
    print("item count: ",item_count, "Count match" if item_count == len(result_list) else "Count not match")
    return result_list


    
