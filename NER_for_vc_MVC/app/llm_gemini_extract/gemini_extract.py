import google.generativeai as genai
import pandas as pd
import json

rule_prompt = """Alright, below I will give you a text of vietnamese criminal data, 
            and I need you to output only json format, and what i required is
            [{name: (in vietnamese), 
             birthdate:(YYYY-MM-DD), 
             gender:(in english (Male/Female)), 
             province_name,
             district_name,
             village_name,
             full_address,
             crime:(in english),
             jail:(if yes yes, if not answer no),
             jail_duration: (if yes yes, if not answer no),
             fine:(if yes yes, if not answer no),
             fine_total:(if yes amount, if not answer no),
             other_punishment:(if yes detail, if not answer "no")}]
            and there might be several criminal in one text and
            don't complete the incomplete address just write what its originally there and
            skip those with null basic infomation"""

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

def extract_data(input_text):

    genai.configure(api_key='')
    model = genai.GenerativeModel("gemini-1.5-pro-latest", safety_settings=safety_settings)
    
    response = model.generate_content(rule_prompt + input_text)
    response_text = response.text

    if "json" in response_text:
        json_response_text = json.loads(response_text[7:-3])
    else:
        json_response_text = json.loads(response_text)

    df = pd.DataFrame(json_response_text)
    data_html = df.to_html(index=False)
    data_html = data_html[data_html.find('\n'):data_html.rfind('\n')]
    return data_html

input_text  = "'<Page:1>TÒA ÁN NHÂN DÂN CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM\nTHÀNH PHỐ LẠNG SƠN Độc lập – Tự do – Hạnh phúc\nTỈNH LẠNG SƠN\nBản án số: 19/2021/HS-ST\nNgày: 10 - 3 - 2021\nNHÂN DANH\nNƯỚC CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nTÒA ÁN NHÂN DÂN THÀNH PHỐ LẠNG SƠN, TỈNH LẠNG SƠN\n- Thành phần Hội đồng xét xử sơ thẩm gồm có:\nThẩm phán - Chủ tọa phiên tòa: Bà Nguyễn Minh Huyền\nCác Hội thẩm nhân dân:\n1. Ông Nguyễn Nhật Chiến;\n2. Bà Hà Hồng Thu.\n- Thư ký phiên tòa: Bà Hoàng Thị Lan - Thư ký Tòa án nhân dân thành\nphố Lạng Sơn, tỉnh Lạng Sơn.\n- Đại diện Viện Kiểm sát nhân dân thành phố Lạng Sơn, tỉnh Lạng Sơn\ntham gia phiên toà: Ông Chu Văn Tới - Kiểm sát viên.\nNgày 10 tháng 3 năm 2021 tại trụ sở Tòa án nhân dân thành phố Lạng\nSơn, tỉnh Lạng Sơn xét xử sơ thẩm công khai vụ án hình sự sơ thẩm thụ lý số\n06/2021/TLST- HS ngày 27 tháng 01 năm 2021 theo Quyết định đưa vụ án ra\nxét xử số 23/2021/QĐXXST- HS ngày 25 tháng 02 năm 2021 đối với bị cáo:\nVũ Thị Lan A, sinh ngày 22 tháng 9 năm 1998 tại huyện Ý Y, tỉnh Nam\nĐịnh; nơi đăng ký hộ khẩu thường trú: Số 92, khu D, thị trấn Đ, huyện C, tỉnh\nLạng Sơn; chỗ ở: Số 36, khu V, thị trấn Đ, huyện C, tỉnh Lạng Sơn; nghề\nnghiệp: Lao động tự do; trình độ văn hoá: 7/12; dân tộc: Kinh; giới tính: Nữ; tôn\ngiáo: Thiên Chúa giáo; quốc tịch: Việt Nam; con ông: Vũ Văn C và bà Vũ Thị\nL; chồng: Bùi Quang H; con: Có 01 con, sinh năm 2019; tiền án: Không; tiền sự:\nKhông. Bị cáo bị áp dụng biện pháp cấm đi khỏi nơi cư trú từ ngày 11/01/2021\nđến nay, có mặt.\nNgười chứng kiến: Anh Nguyễn Minh T, vắng mặt.\nNỘI DUNG VỤ ÁN:\nTheo các tài liệu có trong hồ sơ vụ án và diễn biến tại phiên tòa, nội dung\nvụ án được tóm tắt như sau:\nNgày 02/01/2021, Vũ Thị Lan A đi ra chợ Đ, thị trấn Đ, huyện C, tỉnh\nLạng Sơn mua 05 giàn pháo loại 36 quả/giàn với một người đàn ông khoảng 30<Page:2>tuổi, không biết tên địa chỉ với giá 60.000 đồng/giàn, tổng cộng là 300.000 đồng\nmang về nhà cất giấu. Đến 13 giờ ngày 05/01/2021 Vũ Thị Lan A cho 05 giàn\npháo vào trong vali cá nhân màu nâu rồi đón xe taxi xuống bến xe phía Bắc,\nhuyện C, tỉnh Lạng Sơn để lên xe khách đi về quê Nam Định. Khi đi đến bến xe\nphía Bắc, Vũ Thị Lan A cho vali đựng pháo lên xe ô tô Biển kiểm soát: 35B -\n010.74 do lái xe Nguyễn Viết H điều khiển, anh Nguyễn Minh T là phụ xe, vali\nđể ở hàng ghế cuối xe phía bên phải. Đến khoảng 13 giờ 50 phút cùng ngày khi\nxe rời bến đi đến Km17 + 500 đường quốc lộ 1A thuộc thôn T, xã M, thành phố\nL thì bị lực lượng Công an kiểm tra, phát hiện bắt quả tang.\nTại biên bản xác định trọng lượng, chủng loại vật nghi pháo ngày\n05/01/2021 của Công an thành phố Lạng Sơn, tỉnh Lạng Sơn đã xác định: Số\npháo thu giữ của Vũ Thị Lan A có tổng trọng lượng 7,5kg; gồm 05 khối hình\nhộp, mỗi khối chứa 36 vật hình trụ liên kết với nhau bởi dây nối, có kích thước\n14.5 cm x 14.5 cm x 15 cm, bên ngoài có dây nối.\nTại kết luận giám định số 12/KL-PC09 ngày 10/01/2021 của Phòng Kỹ\nthuật Hình sự - Công an tỉnh Lạng Sơn kết luận các mẫu vật pháo thu giữ đều\nchứa thuốc pháo, khi đốt đều gây ra tiếng nổ.\nTại bản Cáo trạng số 15/CT-VKSTP-MT ngày 25 tháng 01 năm 2021,\nViện kiểm sát nhân dân thành phố Lạng Sơn, tỉnh Lạng Sơn đã truy tố bị cáo Vũ\nThị Lan A về tội Tàng trữ, vận chuyển hàng cấm theo quy định tại điểm c khoản\n1 Điều 191 của Bộ luật Hình sự.\nTại phiên tòa, bị cáo Vũ Thị Lan A khai nhận: Ngày 02/01/2021 bị cáo ra\nchợ Đ, thị trấn Đ, huyện C, tỉnh Lạng Sơn mua 05 dàn pháo loại 36 quả/giàn với\ngiá 300.000 đồng để mang về quê đốt dịp tết nguyên đán. Sau khi mua được số\npháo trên, bị cáo mang số pháo trên về nhà cất giấu trong tủ quần áo từ ngày\n02/01/2021 đến ngày 05/01/2021 thì mang số pháo trên đi xe khách về quê, khi\nđang đi trên xe khách đến khu vực xã M, thành phố L thì bị Công an kiểm tra và\nthu giữ toàn bộ số pháo trên.\nNgười chứng kiến anh Nguyễn Minh T vắng mặt tại phiên tòa, các lời\nkhai trong hồ sơ thể hiện: Anh làm phụ xe của xe khách biển kiểm soát 35B -\n010.74 chạy tuyến Ninh Bình - Lạng Sơn. Ngày 05/01/2021 có một người phụ\nnữ bế một trẻ em khoảng 01 tuổi và cầm theo 01 vali màu nâu lên xe khách của\nanh, khi xe đi đến đoạn Km17 + 500 thuộc thôn T, xã M, thành phố L, tỉnh Lạng\nSơn thì bị lực lượng công an kiểm tra, phát hiện trong vali màu nâu của người\nphụ nữ đó có chứa pháo. Khi người phụ nữ có chiếc vali màu nâu lên xe, do là\nhành lý của khách nên anh không được kiểm tra, do đó không biết trong vali\nmàu nâu chứa pháo.\nTại phiên tòa, đại diện Viện Kiểm sát nhân dân thành phố Lạng Sơn, tỉnh\nLạng Sơn đề nghị Hội đồng xét xử: Tuyên bố bị cáo Vũ Thị Lan A phạm tội\nVận chuyển hàng cấm, do bị cáo thực hiện một chuỗi hành vi nên chỉ chịu một\ntội là Vận chuyển hàng cấm, không đề nghị xét xử về tội tàng trữ hàng cấm. Áp\ndụng điểm c khoản 1 Điều 191; điểm i, s khoản 1 Điều 51; Điều 65 Bộ luật Hình\nsự đề nghị xử phạt bị cáo Vũ Thị Lan A từ 06 đến 09 tháng tù cho hưởng án\n2<Page:3>treo, thời gian thử thách từ 12 đến 18 tháng tính từ ngày tuyên án sơ thẩm.\nKhông áp dụng hình phạt bổ sung là phạt tiền vì bị cáo không có tài sản riêng để\nđảm bảo thi hành án. Về xử lý vật chứng: Đối với toàn bộ số pháo đựng trong 01\nthùng bìa cát tông và 01 vali vải màu nâu thu giữ của bị cáo, Cơ quan điều tra đã\ntiêu hủy theo quy định.\nBị cáo không có ý kiến tranh luận với đại diện Viện kiểm sát. Trong lời\nnói sau cùng, bị cáo đề nghị Hội đồng xét xử xem xét giảm nhẹ hình phạt cho bị\ncáo.\nNHẬN ĐỊNH CỦA TÒA ÁN:\nTrên cơ sở nội dung vụ án, căn cứ vào các tài liệu trong hồ sơ vụ án đã\nđược tranh tụng tại phiên tòa, Hội đồng xét xử nhận định như sau:\n[1] Về hành vi, quyết định tố tụng, việc thu thập tài liệu chứng cứ của\nĐiều tra viên; Kiểm sát viên trong quá trình điều tra, truy tố đã thực hiện đúng\nthẩm quyền, trình tự, thủ tục theo quy định của Bộ luật Tố tụng hình sự. Quá\ntrình điều tra và tại phiên tòa, bị cáo không có ý kiến hoặc khiếu nại về hành vi,\nquyết định của Cơ quan tiến hành tố tụng, người tiến hành tố tụng. Do đó, các\nhành vi, quyết định tố tụng của Cơ quan tiến hành tố tụng, người tiến hành tố\ntụng đã thực hiện đều hợp pháp.\n[2] Lời khai của bị cáo tại phiên tòa phù hợp với các lời khai tại Cơ quan\nđiều tra, phù hợp với biên bản sự việc ngày 05/01/2021 và các tài liệu, chứng cứ\nkhác có trong hồ sơ vụ án đã được thẩm tra tại phiên tòa; có đủ căn cứ để xác\n[\nđịnh: Vào hồi 13 giờ 50 phút ngày 05/01/2021, bị cáo Vũ Thị Lan A đang có\nhành vi vận chuyển 7,5kg pháo nổ về quê sử dụng đốt nhân dịp Tết nguyên đán,\nkhi đi đến Km17, thuộc thôn T, xã M, thành phố L thì bị lực lượng công an bắt\ngiữ, do đó hành vi phạm tội của bị cáo đã phạm vào tội Vận chuyển hàng cấm\nnhư lời luận tội của đại diện Viện kiểm sát là có căn cứ.\n[3] Hành vi phạm tội của bị cáo là nguy hiểm cho xã hội, ảnh hưởng đến\ntrật tự trị an tại địa phương. Bản thân bị cáo có đủ năng lực trách nhiệm hình sự,\nnhận thức rõ Nhà nước nghiêm cấm hành vi vận chuyển và đốt pháo nổ; nhưng\ndo ý thức coi thường pháp luật nên bị cáo vẫn cố ý thực hiện. Hành vi của bị cáo\ncần phải được xử lý đúng quy định của pháp luật để giáo dục, răn đe và phòng\nngừa chung.\n[4] Để có căn cứ quyết định hình phạt, ngoài việc đánh giá tính chất, mức\nđộ nguy hiểm của hành vi phạm tội của bị cáo, cần xem xét đến đặc điểm về\nnhân thân, tình tiết tăng nặng, giảm nhẹ trách nhiệm hình sự đối với bị cáo.\n[5] Về tình tiết tăng nặng: Không có.\n[6] Về tình tiết giảm nhẹ trách nhiệm hình sự: Trong quá trình điều tra và\ntại phiên tòa bị cáo thành khẩn khai báo, ăn năn hối cải, lần phạm tội này là lần\nđầu và thuộc trường hợp ít nghiêm trọng. Do đó bị cáo được hưởng các tình tiết\ngiảm nhẹ trách nhiệm hình sự quy định tại điểm i, s khoản 1 Điều 51 Bộ luật\nHình sự.\n3<Page:4>[7] Về nhân thân: Bị cáo chưa có tiền án, tiền sự.\n[8] Từ những nhận định nêu trên, trên cơ sở xem xét đề nghị của Kiểm sát\nviên, Hội đồng xét xử xét thấy bị cáo có nhân thân tốt, có nhiều tình tiết giảm\nnhẹ quy định tại khoản 1 Điều 51 Bộ luật Hình sự, không có tình tiết tăng nặng,\nhiện đang nuôi con nhỏ 14 tháng tuổi, nhất thời phạm tội, có khả năng tự cải tạo.\nCăn cứ Điều 65 của Bộ luật Hình sự năm 2015; Điều 1, 2 Nghị quyết số\n02/2018/NQ-HĐTP ngày 15/5/2018 của Hội đồng Thẩm phán Tòa án nhân dân\ntối cao hướng dẫn áp dụng Điều 65 của Bộ luật Hình sự, xét thấy không cần\nthiết phải cách ly bị cáo ra khỏi đời sống xã hội mà cho bị cáo cải tạo tại địa\nphương cũng đủ sức răn đe, phòng ngừa, không gây nguy hiểm cho xã hội,\nkhông ảnh hưởng xấu đến an ninh, trật tự địa phương, đồng thời đảm bảo tính\nkhoan hồng của Nhà nước.\n[9] Về hình phạt bổ sung: Tại biên bản xác minh ngày 19/01/2021, thể\nhiện bị cáo không có nghề nghiệp, không có tài sản riêng để đảm bảo thi hành\nán, vì vậy không áp dụng hình phạt bổ sung là phạt tiền đối với bị cáo.\n[10] Về xử lý vật chứng: Áp dụng điểm c khoản 1 Điều 47 của Bộ luật\nHình sự; điểm a, c khoản 2 Điều 106 của Bộ luật Tố tụng hình sự: Xác nhận\ntoàn bộ số pháo nổ, 01 thùng bìa cát tông và 01 vali vải màu nâu thu giữ của bị\ncáo đã được tiêu hủy ngày 18/01/2021.\n[11] Bị cáo là người bị kết án nên phải chịu án phí hình sự sơ thẩm theo\nquy định tại khoản 2 Điều 136 của Bộ luật Tố tụng hình sự.\n[12] Bị cáo có quyền kháng cáo bản án theo quy định tại Điều 331, Điều\n333 Bộ luật Tố tụng hình sự.\nVì các lẽ trên,\nQUYẾT ĐỊNH:\nCăn cứ điểm c khoản 1 Điều 47; điểm i, s khoản 1 Điều 51; khoản 1, 2 ,5\nĐiều 65; điểm c khoản 1 Điều 191 Bộ luật Hình sự;\nCăn cứ điểm a, c khoản 2 Điều 106; khoản 2 Điều 136, Điều 331, Điều\n333 của Bộ luật Tố tụng hình sự; điểm a khoản 1 Điều 23 Nghị quyết số\n326/2016/UBTVQH14 ngày 30/12/2016 của Uỷ ban Thường vụ Quốc hội quy\nđịnh về mức thu, miễn, giảm, thu, nộp, quản lý và sử dụng án phí và lệ phí Tòa\nán.\n1. Về tội danh: Tuyên bố bị cáo Vũ Thị Lan A phạm tội Vận chuyển hàng\ncấm.\n2. Về hình phạt: Xử phạt bị cáo Vũ Thị Lan A 06 (sáu) tháng tù cho\nhưởng án treo. Thời gian thử thách 01 (một) năm tính từ ngày tuyên án sơ thẩm\n(10/3/2021).\nGiao bị cáo Vũ Thị Lan A cho Ủy ban nhân dân thị trấn Đ, huyện C, tỉnh\nLạng Sơn giám sát, giáo dục trong thời gian thử thách. Gia đình bị cáo có trách\nnhiệm phối hợp với Ủy ban nhân dân xã, phường nơi bị cáo cư trú trong việc\n4<Page:5>giám sát, giáo dục bị cáo. Trong trường hợp bị cáo thay đổi nơi cư trú thì thực\nhiện theo quy định tại Điều 92 của Luật Thi hành án hình sự.\nTrong thời gian thử thách, người được hưởng án treo cố ý vi phạm nghĩa\nvụ 02 lần trở lên thì Tòa án có thể quyết định buộc người được hưởng án treo\nphải chấp hành hình phạt tù của bản án đã cho hưởng án treo.\n3. Về xử lý vật chứng: Xác nhận Cơ quan điều tra đã tiêu hủy toàn bộ số\npháo còn lại sau giám định và 01 vali vải màu nâu theo biên bản kiểm tra tình\ntrạng tang vật và tiêu hủy vật chứng ngày 18/01/2021.\n4. Về án phí: Buộc bị cáo Vũ Thị Lan A phải nộp 200.000 đồng (hai trăm\nnghìn) tiền án phí hình sự sơ thẩm sung ngân sách Nhà nước.\n5. Quyền kháng cáo: Bị cáo có quyền kháng cáo trong thời gian 15 ngày\nkể từ ngày tuyên án.\nNơi nhận: TM. HỘI ĐỒNG XÉT XỬ SƠ THẨM\n- TAND tỉnh Lạng Sơn; THẨM PHÁN-CHỦ TỌA PHIÊN TÒA\n- VKSND tỉnh Lạng Sơn;\n- VKSND TP Lạng Sơn, tỉnh Lạng Sơn;\n- Sở Tư pháp tỉnh Lạng Sơn;\n- Công an TP Lạng Sơn, tỉnh Lạng Sơn;\n- Chi cục THADSTP. Lạng Sơn, tỉnh Lạng Sơn;\n- Bị cáo;\n- Lưu hồ sơ vụ án.\nNguyễn Minh Huyền\n5'"



