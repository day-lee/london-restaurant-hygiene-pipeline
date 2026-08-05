from lxml import etree
from datetime import datetime 

def parse_xml(file_path:str): 
    tree = etree.parse(file_path)
    root = tree.getroot() 
    item_count = int(root.findtext("./Header/ItemCount"))
    records = root.xpath(".//EstablishmentDetail")

    target_tags = ["FHRSID", "BusinessName", "RatingDate", "PostCode", "RatingValue", "LocalAuthorityCode", "LocalAuthorityName"] 

    result_list = []

    for record in records:
        record_dict = {} 
        for tag in target_tags:
            node = record.find(tag)

            # 노드가 없거나 텍스트가 비어있으면 None 처리 
            if node is None or node.text is None:
                record_dict[tag] = None 
                continue 
            text_value = node.text.strip() 
            if not text_value: #" " 빈 문자열
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


    
