"""
영화 100개 샘플 데이터 생성 스크립트
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SyncSessionLocal
from app.models.movie import Movie


# 영화 샘플 데이터 (일부만 작성, 실제로는 100개 필요)
SAMPLE_MOVIES = [
  {
    "name": "마더!",
    "director": "대런 아로노프스키",
    "summary": "외딴 집에서 남편과 함께 살아가던 여인은 자신의 공간이 점점 낯선 타인들로 채워지는 경험을 한다. 예고 없이 찾아온 손님들은 무례하게 집을 점유하고, 그들의 행동은 점점 통제를 벗어난다. 여인은 집을 지키기 위해 애쓰지만 남편은 이를 묵인하며 상황을 악화시킨다. 혼란이 극에 달할수록 그녀의 정체성과 감정은 무너져 간다. 사랑과 헌신은 폭력과 착취로 변질되고, 창조와 파괴의 순환이 노골적으로 드러난다. 개인의 불안은 결국 인간 사회 전체에 대한 잔혹한 은유로 확장된다.",
    "cast": "제니퍼 로렌스, 하비에르 바르뎀",
    "keywords": ["혼돈", "침식", "불안", "은유", "종말"],
    "url":"https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/0d9f5e4f-31ab-41ec-33b2-bfc24f454900/public"
  },
  {
    "name": "반지의 제왕",
    "director": "피터 잭슨",
    "summary": "강대한 힘을 지닌 반지가 다시 세상에 모습을 드러내며 중간계는 어둠의 위협에 휩싸인다. 평범한 호빗은 반지를 파괴해야 하는 사명을 떠안고 동료들과 길을 나선다. 여정 속에서 우정은 시험받고, 유혹과 두려움은 끊임없이 그를 흔든다. 인간과 엘프, 드워프는 서로 다른 이해관계를 넘어 연대한다. 작은 선택들이 전쟁의 흐름을 바꾸는 순간들이 반복된다. 희생을 통해 세계의 균형이 유지된다는 사실이 장대한 서사로 그려진다.",
    "cast": "일라이저 우드, 이안 맥켈런",
    "keywords": ["모험", "운명", "우정", "희생", "연대"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/99ca5e30-c22f-4da7-02a0-2ad1d375eb00/public"
  },
  {
    "name": "위플래쉬",
    "director": "데이미언 셔젤",
    "summary": "재능 있는 드러머 지망생은 최고의 연주자가 되겠다는 목표로 명문 음악 학교에 입학한다. 그는 완벽을 강요하는 교수의 가혹한 교육 방식 아래 놓인다. 칭찬과 모욕이 교차하는 환경은 그의 자존감을 점점 파괴한다. 연습은 즐거움이 아니라 생존을 위한 투쟁이 된다. 성공을 향한 집착은 인간관계와 일상을 잠식한다. 무대 위에서의 선택은 예술이 무엇을 요구하는지 잔인하게 드러낸다.",
    "cast": "마일즈 텔러, J.K. 시몬스",
    "keywords": ["집착", "완벽주의", "압박", "성취", "대립"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/088f553b-4ab0-4dbd-075f-1b5363439400/public"
  },
  {
    "name": "월·E",
    "director": "앤드루 스탠턴",
    "summary": "황폐해진 지구에 홀로 남은 로봇은 쓰레기를 정리하며 외로운 일상을 반복한다. 어느 날 하늘에서 내려온 탐사 로봇과의 만남은 그의 세계를 바꾼다. 작은 호기심은 감정으로 발전하고, 그는 처음으로 누군가를 지키고 싶다는 마음을 느낀다. 두 로봇은 우주로 향하는 여정에 오르게 된다. 인류가 버린 지구의 미래가 서서히 드러난다. 사랑과 책임이 인류의 생존을 다시 움직이기 시작한다.",
    "cast": "벤 버트, 엘리사 나이트",
    "keywords": ["고독", "사랑", "환경", "희망", "미래"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/0419fb2e-e3cd-4e1d-c279-caf3a7f11a00/public"
  },
  {
    "name": "트레인스포팅",
    "director": "대니 보일",
    "summary": "에든버러의 젊은이들은 마약과 무기력 속에서 하루하루를 버틴다. 쾌락과 자기혐오가 반복되는 삶은 점점 더 깊은 수렁으로 빠져든다. 친구들은 서로에게 의지가 되지만 동시에 파멸의 원인이 된다. 주인공은 이 삶에서 벗어나고자 여러 번 결심한다. 그러나 선택의 순간마다 과거는 그를 붙잡는다. 자유를 향한 탈출은 언제나 대가를 요구한다.",
    "cast": "이완 맥그리거, 로버트 칼라일",
    "keywords": ["중독", "청춘", "허무", "일탈", "선택"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/2c01010a-0cdc-48ba-260f-920ce84a8800/public"
  },
  {
    "name": "타이타닉",
    "director": "제임스 카메론",
    "summary": "1912년 4월, 귀족 가문의 딸 로즈는 초호화 여객선 타이타닉호에 승선한다. 원치 않는 결혼을 앞둔 그녀는 삶의 의미를 잃고 절망에 빠져 있다. 우연히 만난 가난한 화가 잭은 그녀에게 자유와 사랑을 알려준다. 짧은 시간 동안 두 사람은 신분의 벽을 넘어 깊이 사랑하게 된다. 그러나 거대한 사고가 배를 덮치며 모든 것이 뒤바뀐다. 사랑과 희생은 비극 속에서 더욱 선명해진다.",
    "cast": "레오나르도 디카프리오, 케이트 윈슬렛",
    "keywords": ["사랑", "비극", "계급", "희생", "운명"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/48c64557-9e26-4cd0-4e3e-f29e641aee00/public"
  },
  {
    "name": "노트북",
    "director": "닉 카사베츠",
    "summary": "서로 다른 배경을 지닌 두 젊은이는 한여름의 만남으로 사랑에 빠진다. 현실적인 장벽과 가족의 반대는 이들을 갈라놓는다. 시간이 흐르며 각자는 다른 삶을 살아가게 된다. 그러나 기억 속 감정은 쉽게 사라지지 않는다. 세월이 지나 다시 마주한 사랑은 과거를 되살린다. 사랑이 기억과 함께 어떻게 지속되는지를 조용히 보여준다.",
    "cast": "라이언 고슬링, 레이첼 맥아담스",
    "keywords": ["로맨스", "기억", "운명", "시간", "헌신"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/3743fbfd-cafb-4530-ad14-749d69f6f400/public"
  },
  {
    "name": "곡성",
    "director": "나홍진",
    "summary": "평화롭던 시골 마을에서 원인 불명의 사건들이 연이어 발생한다. 경찰은 기이한 외지인의 등장 이후 벌어진 일들에 주목한다. 소문과 공포는 점점 마을 전체를 잠식한다. 사람들은 종교와 미신에 의존하기 시작한다. 무엇이 진실인지 구분하기 어려워진다. 믿음에 대한 선택은 돌이킬 수 없는 결과를 낳는다.",
    "cast": "곽도원, 황정민",
    "keywords": ["공포", "불신", "미스터리", "종교", "혼란"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/44ecc9a3-102d-46c7-d809-831b73995800/public"
  },
  {
    "name": "트루먼 쇼",
    "director": "피터 위어",
    "summary": "한 남자는 자신의 삶이 어딘가 인위적이라는 의문을 품기 시작한다. 주변 사람들과 사건들은 지나치게 완벽하게 맞물려 돌아간다. 작은 이상 신호들은 점점 큰 의심으로 이어진다. 그는 진실을 확인하기 위해 행동하기 시작한다. 세계는 그를 붙잡으려 하지만 갈망은 커져만 간다. 자유를 향한 선택이 인생 최대의 시험이 된다.",
    "cast": "짐 캐리",
    "keywords": ["자유", "통제", "각성", "정체성", "감시"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/4075dc13-fcf3-464e-33e7-8e0390b0b400/public"
  },
  {
    "name": "소셜 네트워크",
    "director": "데이비드 핀처",
    "summary": "하버드 대학생은 분노와 열등감 속에서 새로운 아이디어를 떠올린다. 온라인 네트워크는 빠르게 확장되며 성공을 거둔다. 친구와 동업자는 점차 경쟁자와 적이 된다. 성공의 속도만큼 관계는 빠르게 무너진다. 법정 다툼은 과거의 선택을 되짚게 만든다. 연결의 시대 속에서 고립이 더욱 선명해진다.",
    "cast": "제시 아이젠버그, 앤드루 가필드",
    "keywords": ["야망", "배신", "성공", "고립", "권력"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/2fced00c-5a5c-4af7-08d8-cb282def5200/public"
  },
  {
    "name": "쇼생크 탈출",
    "director": "프랭크 다라본트",
    "summary": "억울한 누명을 쓴 은행원은 냉혹한 교도소에 수감된다. 폭력과 절망이 지배하는 환경 속에서도 그는 침착함을 잃지 않는다. 지식과 성실함은 동료 수감자들의 신뢰를 얻는다. 오랜 시간 동안 작은 희망을 포기하지 않는다. 우정은 감옥 생활을 견디게 하는 유일한 힘이 된다. 인내 끝에 자유는 뜻밖의 방식으로 다가온다.",
    "cast": "팀 로빈스, 모건 프리먼",
    "keywords": ["희망", "자유", "우정", "인내", "구원"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/bed34f54-3c86-4091-01f1-ff4ac009e100/public"
  },
  {
    "name": "레버넌트: 죽음에서 돌아온 자",
    "director": "알레한드로 곤살레스 이냐리투",
    "summary": "미개척지에서 사냥꾼은 치명적인 공격을 당하고 버려진다. 극한의 자연 속에서 그는 살아남기 위해 몸을 끌고 나아간다. 배신의 기억은 복수심으로 변한다. 생존과 분노는 그의 원동력이 된다. 자연은 적이자 시험이 된다. 인간의 집념과 원초적인 생존 본능이 적나라하게 드러난다.",
    "cast": "레오나르도 디카프리오",
    "keywords": ["생존", "복수", "자연", "집념", "고통"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/7edd3ea5-a588-417a-0d8a-5e83ca851200/public"
  },
  {
    "name": "노스맨",
    "director": "로버트 에거스",
    "summary": "어린 시절 왕이었던 아버지를 잃은 소년은 복수를 다짐한다. 성인이 된 그는 전사의 길을 걷는다. 운명과 신화는 그의 선택을 끊임없이 시험한다. 복수는 삶의 목적이 된다. 피와 전투 속에서 인간성은 점점 흐려진다. 폭력의 순환은 피할 수 없는 결말로 이어진다.",
    "cast": "알렉산더 스카스가드",
    "keywords": ["복수", "운명", "신화", "폭력", "비극"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/de493dce-7814-412d-f959-f833cca8b400/public"
  },
  {
    "name": "센과 치히로의 행방불명",
    "director": "미야자키 하야오",
    "summary": "이사 도중 낯선 세계에 들어선 소녀는 부모를 잃고 홀로 남는다. 인간이 아닌 존재들이 사는 공간에서 그녀는 일을 하며 살아남아야 한다. 두려움 속에서도 점차 용기를 배운다. 다양한 존재들과의 만남은 성장의 계기가 된다. 이름과 정체성을 지키는 것이 중요해진다. 집으로 돌아가기 위한 여정은 성숙으로 이어진다.",
    "cast": "히이라기 루미",
    "keywords": ["성장", "환상", "정체성", "용기", "여정"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/dd717ad0-539c-42a1-47c4-b3e9b921cc00/public"
  },
  {
    "name": "매트릭스",
    "director": "워쇼스키 자매",
    "summary": "평범한 일상을 살던 남자는 세계가 가짜일지도 모른다는 의문을 품는다. 비밀스러운 인물들과의 만남은 진실로 이어진다. 현실이라 믿던 세계는 거대한 시스템에 불과하다. 그는 선택의 기로에 선다. 각성은 고통을 동반한다. 자유를 위한 싸움이 시작된다.",
    "cast": "키아누 리브스",
    "keywords": ["각성", "자유", "현실", "저항", "선택"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/76be09ff-a1b1-4c0e-9e04-a702b64faa00/public"
  },
  {
    "name": "남산의 부장들",
    "director": "우민호",
    "summary": "권력의 핵심부에서 정보기관 수장은 점점 고립된다. 충성과 배신이 교차하는 정치적 긴장은 극에 달한다. 과거의 동료들은 위협적인 존재가 된다. 권력을 지키기 위한 선택은 점점 극단으로 치닫는다. 개인의 판단은 역사의 흐름에 영향을 미친다. 비극은 이미 예정된 듯 다가온다.",
    "cast": "이병헌, 이성민",
    "keywords": ["권력", "배신", "정치", "긴장", "비극"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/95f3c579-1818-4991-cc5c-d618da4cd600/public"
  },
  {
    "name": "더 랍스터",
    "director": "요르고스 란티모스",
    "summary": "사랑이 의무가 된 사회에서 홀로 남은 남자는 호텔에 수용된다. 정해진 기간 안에 짝을 찾지 못하면 동물로 변해야 한다. 사람들은 사랑을 생존 수단으로 이용한다. 규칙은 인간성을 점점 왜곡시킨다. 탈출은 또 다른 규범으로 이어진다. 사랑의 본질이 기묘하게 드러난다.",
    "cast": "콜린 퍼렐, 레이첼 와이즈",
    "keywords": ["부조리", "사랑", "규범", "고독", "풍자"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/e37e6ade-3221-49f3-8de3-598e30b25200/public"
  },
  {
    "name": "라이트하우스",
    "director": "로버트 에거스",
    "summary": "외딴 섬의 등대에서 두 남자는 함께 생활하게 된다. 고립된 환경은 점점 정신을 잠식한다. 권력과 복종의 관계는 균열을 만든다. 술과 환각은 현실과 망상을 흐리게 한다. 과거의 죄책감이 드러난다. 광기는 피할 수 없는 결말로 향한다.",
    "cast": "윌렘 대포, 로버트 패틴슨",
    "keywords": ["광기", "고립", "권력", "죄책감", "불안"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/effc4f37-3282-4b12-fa22-06186d6bfd00/public"
  },
  {
    "name": "킹스 스피치",
    "director": "톰 후퍼",
    "summary": "말더듬이라는 약점을 지닌 왕자는 갑작스럽게 왕위에 오른다. 그는 국가적 위기 속에서 연설을 해야 하는 상황에 놓인다. 언어 치료사와의 만남은 변화의 계기가 된다. 좌절과 훈련이 반복된다. 신뢰는 점차 쌓여간다. 목소리를 찾는 과정은 책임을 받아들이는 여정이 된다.",
    "cast": "콜린 퍼스, 제프리 러시",
    "keywords": ["극복", "책임", "우정", "성장", "용기"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/b30061dc-a931-439b-f126-abf60e61a000/public"
  },
  {
    "name": "이미테이션 게임",
    "director": "모튼 틸덤",
    "summary": "전쟁 중 암호 해독을 맡은 천재 수학자는 팀을 이끈다. 사회적 소통에 서툰 그는 갈등을 빚는다. 불가능해 보이던 암호는 집념 속에서 풀리기 시작한다. 성공은 수많은 생명을 구한다. 그러나 개인의 삶은 또 다른 차별에 직면한다. 공헌과 희생의 아이러니가 남는다.",
    "cast": "베네딕트 컴버배치, 키이라 나이틀리",
    "keywords": ["천재성", "전쟁", "희생", "차별", "집념"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/3bc25ed6-a506-41ef-bea8-79c684f1ca00/public"
  },
  {
    "name": "헌트",
    "director": "토마스 빈터베르그",
    "summary": "평범한 교사로 살아가던 남자는 한 아이의 거짓말로 인해 순식간에 의심의 대상이 된다. 작은 오해는 마을 전체로 퍼지며 걷잡을 수 없는 소문이 된다. 친구와 이웃들은 등을 돌리고, 일상은 붕괴된다. 그는 결백을 증명하려 하지만 사회는 이미 판단을 내려버린다. 고립 속에서 분노와 슬픔이 뒤섞인다. 진실보다 믿음이 더 큰 힘을 가지는 순간의 공포가 드러난다.",
    "cast": "매즈 미켈슨",
    "keywords": ["누명", "집단심리", "불신", "고립", "분노"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/b72a8a43-554d-4db8-48bc-51e09acf1200/public"
  },
  {
    "name": "아가씨",
    "director": "박찬욱",
    "summary": "일제강점기 조선에서 한 소녀는 귀족 여성을 속이기 위한 계획에 가담한다. 속임수로 시작된 관계는 점차 예측할 수 없는 감정으로 변한다. 계략과 욕망은 서로 얽히며 인물들의 진짜 목적을 드러낸다. 권력과 성적 지배 구조가 노골적으로 드러난다. 선택의 순간마다 배신은 반복된다. 억압 속에서 자유를 향한 탈출이 시도된다.",
    "cast": "김민희, 김태리, 하정우",
    "keywords": ["욕망", "배신", "해방", "권력", "관계"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/26054944-8522-47fe-7616-9b3f1120e600/public"
  },
  {
    "name": "그랜드 부다페스트 호텔",
    "director": "웨스 앤더슨",
    "summary": "유서 깊은 호텔의 전설적인 지배인은 젊은 로비 보이와 특별한 우정을 쌓는다. 갑작스러운 유산 상속 사건은 살인 누명을 불러온다. 두 사람은 쫓기며 유럽 전역을 넘나든다. 기묘한 인물들과 사건들이 연이어 등장한다. 시대의 변화는 호텔의 운명에도 영향을 미친다. 유쾌함 속에 사라져가는 세계에 대한 애수가 담긴다.",
    "cast": "랄프 파인즈, 토니 레볼로리",
    "keywords": ["우정", "모험", "향수", "유머", "상실"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/12e14e38-258b-40ae-2353-4c118c1cb200/public"
  },
  {
    "name": "프렌치 디스패치",
    "director": "웨스 앤더슨",
    "summary": "한 잡지사의 마지막 호를 구성하는 여러 이야기가 펼쳐진다. 기자들은 각자의 방식으로 세상을 기록한다. 예술, 정치, 인간 군상이 독특한 시선으로 묘사된다. 사실과 해석의 경계는 흐려진다. 개별 에피소드는 하나의 세계관으로 연결된다. 기록한다는 행위의 의미가 질문으로 남는다.",
    "cast": "베니시오 델 토로, 에이드리언 브로디",
    "keywords": ["기록", "예술", "관찰", "유머", "서사"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/d2b4fba4-e636-4b65-cb6a-a97ed7c4f300/public"
  },
  {
    "name": "플로리다 프로젝트",
    "director": "션 베이커",
    "summary": "관광지 근처 허름한 모텔에서 아이는 자유롭게 뛰놀며 여름을 보낸다. 어른들의 삶은 경제적 불안과 좌절로 가득 차 있다. 아이의 시선은 현실의 어두움을 희미하게 가린다. 관리인은 아이들을 조용히 보호하려 애쓴다. 무책임한 선택들은 점점 한계를 드러낸다. 순수함과 현실의 간극이 아프게 대비된다.",
    "cast": "브루클린 프린스, 윌렘 대포",
    "keywords": ["빈곤", "아동", "현실", "순수", "불안"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/c3d0592e-02e1-4ca4-5b1f-88693d40a400/public"
  },
  {
    "name": "더 페이버릿: 여왕의 여자",
    "director": "요르고스 란티모스",
    "summary": "권력의 정점에 선 여왕 곁에는 두 여인이 머문다. 총애를 얻기 위한 경쟁은 은밀하게 시작된다. 친절과 배려는 계산된 전략으로 변한다. 정치와 사적인 욕망은 분리되지 않는다. 승자는 바뀌고 패자는 버려진다. 권력의 공허함이 냉소적으로 드러난다.",
    "cast": "올리비아 콜먼, 엠마 스톤, 레이첼 와이즈",
    "keywords": ["권력", "야망", "질투", "정치", "풍자"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/4cc87599-ed4c-4992-5bf8-43b44ec70a00/public"
  },
  {
    "name": "클래식",
    "director": "곽재용",
    "summary": "어느 날 발견한 오래된 편지는 과거의 사랑 이야기를 불러낸다. 젊은 시절의 순수한 감정은 시대의 제약 속에서 흔들린다. 선택하지 못한 사랑은 아픔으로 남는다. 현재의 사랑은 과거와 겹쳐진다. 감정은 세대를 넘어 반복된다. 사랑의 기억은 쉽게 사라지지 않는다.",
    "cast": "손예진, 조승우",
    "keywords": ["첫사랑", "기억", "운명", "감성", "시간"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/76afa8b6-2a19-42dc-de7a-09bbe2561100/public"
  },
  {
    "name": "슬럼독 밀리어네어",
    "director": "대니 보일",
    "summary": "빈민가에서 자란 청년은 퀴즈 쇼에 출연해 연속으로 정답을 맞힌다. 의심을 받으며 조사를 받게 된다. 질문 하나하나는 그의 과거 경험과 연결된다. 가난과 폭력 속에서 살아남은 기억이 답이 된다. 사랑하는 여인을 향한 집념이 그를 움직인다. 운명과 우연이 교차한다.",
    "cast": "데브 파텔",
    "keywords": ["운명", "빈곤", "사랑", "생존", "기회"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/f3239944-8930-47fa-9b25-d74d3d22ef00/public"
  },
  {
    "name": "시카리오: 암살자의 도시",
    "director": "드니 빌뇌브",
    "summary": "마약 전쟁이 벌어지는 국경 지대로 요원이 파견된다. 정의를 믿던 원칙은 점점 흔들린다. 작전은 예상보다 잔혹하게 전개된다. 동료들의 진짜 목적은 숨겨져 있다. 폭력은 일상이 된다. 정의와 복수의 경계는 모호해진다.",
    "cast": "에밀리 블런트, 베니시오 델 토로",
    "keywords": ["폭력", "도덕", "전쟁", "경계", "냉혹"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/d8073763-d183-455f-cc1c-af9e7af51a00/public"
  },
  {
    "name": "그녀가 말했다",
    "director": "마리아 슈레이더",
    "summary": "두 기자는 거대한 권력 뒤에 숨겨진 진실을 추적한다. 피해자들은 오랜 침묵을 강요받아왔다. 인터뷰는 두려움과 용기를 동시에 요구한다. 증언은 하나둘 모이기 시작한다. 보도는 사회에 파문을 일으킨다. 말한다는 행위 자체가 투쟁이 된다.",
    "cast": "캐리 멀리건, 조이 카잔",
    "keywords": ["폭로", "용기", "진실", "권력", "연대"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/d83f964e-460c-4759-f1dc-bc83966a1900/public"
  },
  {
    "name": "서치",
    "director": "아니시 차간티",
    "summary": "어느 날 딸이 흔적도 없이 사라진다. 아버지는 컴퓨터와 스마트폰 속 기록을 뒤진다. 온라인 흔적은 예상치 못한 진실로 이어진다. 관계의 빈틈이 드러난다. 시간은 빠르게 흘러간다. 디지털 시대의 가족과 소통이 드러난다.",
    "cast": "존 조",
    "keywords": ["실종", "추적", "디지털", "부성", "긴박"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/6d78ba3c-3af6-41ef-0195-b0c860edef00/public"
  },
  {
    "name": "라이언 일병 구하기",
    "director": "스티븐 스필버그",
    "summary": "노르망디 상륙 작전 이후 한 부대는 특별한 임무를 부여받는다. 전사한 형제들 대신 살아 있는 병사를 찾아야 한다. 전쟁의 참혹함은 이동하는 내내 반복된다. 명령과 인간성 사이에서 갈등이 커진다. 희생은 당연한 것이 된다. 전쟁 속 개인의 가치는 질문으로 남는다.",
    "cast": "톰 행크스, 맷 데이먼",
    "keywords": ["전쟁", "희생", "동료애", "명령", "인간성"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/93076904-8730-4029-45a7-61bdd8122100/public"
  },
  {
    "name": "룸",
    "director": "레니 에이브러햄슨",
    "summary": "좁은 공간에서 아이는 세상의 전부를 배운다. 어머니는 그 안에서 아이를 지키며 살아간다. 탈출은 새로운 세상을 의미한다. 자유는 곧 혼란으로 다가온다. 트라우마는 쉽게 사라지지 않는다. 회복은 천천히 진행된다.",
    "cast": "브리 라슨, 제이콥 트렘블레이",
    "keywords": ["감금", "모성", "자유", "회복", "트라우마"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/a3a7c6a0-cfcf-4305-c143-3864d35aac00/public"
  },
  {
    "name": "프리즈너스",
    "director": "드니 빌뇌브",
    "summary": "아이들이 실종되며 부모들은 극한의 공포에 빠진다. 수사는 진전이 더디다. 절망 속에서 한 아버지는 직접 행동에 나선다. 정의와 폭력의 경계가 흐려진다. 선택은 되돌릴 수 없는 결과를 낳는다. 죄의 무게는 모두에게 남는다.",
    "cast": "휴 잭맨, 제이크 질렌할",
    "keywords": ["실종", "분노", "도덕", "복수", "절망"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/6e23dd03-b206-4be7-1a59-7ad63a341500/public"
  },
  {
    "name": "패터슨",
    "director": "짐 자무쉬",
    "summary": "버스 운전사로 살아가는 남자는 조용한 일상을 반복한다. 그는 시를 쓰며 하루를 기록한다. 작은 대화와 풍경이 영감이 된다. 특별한 사건은 일어나지 않는다. 평범함 속에서 의미가 발견된다. 삶은 잔잔하게 흐른다.",
    "cast": "아담 드라이버",
    "keywords": ["일상", "창작", "고요", "관찰", "삶"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/8289b344-f761-4d53-840e-deb005d65f00/public"
  },
  {
    "name": "기생충",
    "director": "봉준호",
    "summary": "가난한 가족은 부유한 집에 하나둘 스며든다. 작은 거짓말은 성공적으로 작동한다. 두 가족의 삶은 점점 얽힌다. 숨겨진 계층의 균열이 드러난다. 갈등은 폭력으로 폭발한다. 웃음 뒤에 불편한 현실이 남는다.",
    "cast": "송강호, 이선균",
    "keywords": ["계급", "불평등", "침투", "풍자", "비극"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/49a10863-4988-4df4-da5a-d83d04f63200/public"
  },
  {
    "name": "오직 사랑하는 이들만이 살아남는다",
    "director": "짐 자무쉬",
    "summary": "수백 년을 살아온 연인은 세상의 쇠락을 지켜본다. 인간 문명은 그들에게 피로감을 안긴다. 사랑은 유일한 위안이 된다. 과거와 현재가 겹친다. 불멸은 축복이자 저주다. 관계는 끊임없이 시험받는다.",
    "cast": "틸다 스윈튼, 톰 히들스턴",
    "keywords": ["불멸", "사랑", "권태", "예술", "시간"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/c4c1f5e7-382f-4407-c520-b908b62f0400/public"
  },
  {
    "name": "올드보이",
    "director": "박찬욱",
    "summary": "이유도 모른 채 한 남자는 오랜 시간 감금된다. 풀려난 뒤 그는 복수를 결심한다. 단서는 퍼즐처럼 흩어져 있다. 진실에 가까워질수록 고통은 커진다. 복수는 또 다른 비극을 낳는다. 인간의 잔혹함이 극단적으로 드러난다.",
    "cast": "최민식, 유지태",
    "keywords": ["복수", "비밀", "폭력", "비극", "집착"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/5f55be64-c073-4c40-2034-17f4e6d5c500/public"
  },
  {
    "name": "노매드랜드",
    "director": "클로이 자오",
    "summary": "경제적 붕괴 이후 한 여성은 집을 떠나 길 위의 삶을 선택한다. 임시 일자리와 이동이 일상이 된다. 만남은 짧고 이별은 잦다. 자연은 위안이 된다. 고정된 삶의 형태는 해체된다. 자유와 고독이 공존한다.",
    "cast": "프랜시스 맥도맨드",
    "keywords": ["유랑", "자유", "고독", "생존", "자연"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/16a0466c-5234-4991-8d6f-bdda4fd07000/public"
  },
  {
    "name": "노인을 위한 나라는 없다",
    "director": "코엔 형제",
    "summary": "우연히 거액의 돈을 발견한 남자는 돌이킬 수 없는 선택을 한다. 냉혹한 살인자는 흔적을 남기지 않고 추적을 시작한다. 법을 믿는 보안관은 점점 무력함을 느낀다. 폭력은 이유 없이 반복된다. 선과 악의 구분은 흐려진다. 세계는 더 이상 이해 가능한 질서로 보이지 않는다.",
    "cast": "하비에르 바르뎀, 토미 리 존스",
    "keywords": ["폭력", "허무", "운명", "추적", "무력감"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/d55b1b95-28c4-47f7-40ad-b58baaabde00/public"
  },
  {
    "name": "문라이즈 킹덤",
    "director": "웨스 앤더슨",
    "summary": "외딴 섬에서 두 아이는 서로에게서 유일한 이해를 찾는다. 어른들의 세계는 이들을 통제하려 한다. 아이들은 도망을 선택한다. 숲과 바다는 자유의 공간이 된다. 추격 속에서도 감정은 깊어진다. 첫사랑은 짧지만 강렬하게 남는다.",
    "cast": "자레드 길먼, 카라 헤이워드",
    "keywords": ["첫사랑", "탈출", "자유", "성장", "모험"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/1c01373c-32cd-44d6-fcc3-ff71a8e40f00/public"
  },
  {
    "name": "문라이트",
    "director": "배리 젠킨스",
    "summary": "가난한 동네에서 자란 소년은 자신의 정체성에 혼란을 느낀다. 폭력적인 환경은 침묵을 강요한다. 성장 과정에서 그는 사랑과 거리를 동시에 배운다. 관계는 단절과 재회를 반복한다. 성인이 된 그는 과거와 다시 마주한다. 정체성을 받아들이는 과정이 조용히 그려진다.",
    "cast": "트레반테 로즈, 마허샬라 알리",
    "keywords": ["정체성", "성장", "고독", "사랑", "침묵"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/16e35302-0f60-43b0-85cf-7b25c8ebf100/public"
  },
  {
    "name": "머니볼",
    "director": "베넷 밀러",
    "summary": "재정난에 시달리는 야구단 단장은 기존 방식을 거부한다. 통계와 데이터는 새로운 전략이 된다. 현장은 강한 반발을 보인다. 패배는 조롱으로 돌아온다. 그러나 결과는 서서히 증명된다. 변화는 숫자에서 시작된다.",
    "cast": "브래드 피트, 조나 힐",
    "keywords": ["혁신", "데이터", "도전", "조직", "신념"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/1d3c7d80-1195-4b13-2bef-548901bcc900/public"
  },
  {
    "name": "미나리",
    "director": "정이삭",
    "summary": "새로운 삶을 꿈꾸며 가족은 미국 남부로 이주한다. 농장은 희망과 불안을 동시에 안긴다. 문화와 세대의 차이는 갈등을 만든다. 할머니의 존재는 가족을 변화시킨다. 실패는 반복된다. 가족이라는 공동체는 그럼에도 유지된다.",
    "cast": "스티븐 연, 윤여정",
    "keywords": ["가족", "이주", "정착", "갈등", "회복"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/3e8565ba-476b-481e-6027-015af869fb00/public"
  },
  {
    "name": "미드소마",
    "director": "아리 애스터",
    "summary": "상실을 겪은 여성은 연인과 함께 외딴 공동체를 방문한다. 축제는 평화롭게 시작된다. 의식은 점점 기괴해진다. 외부인의 기준은 무력해진다. 관계는 균열을 드러낸다. 공포는 밝은 대낮에 펼쳐진다.",
    "cast": "플로렌스 퓨",
    "keywords": ["의식", "공동체", "상실", "공포", "붕괴"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/54816add-47de-4a7b-2c03-c5fc07576e00/public"
  },
  {
    "name": "미드나잇 인 파리",
    "director": "우디 앨런",
    "summary": "파리를 여행하던 작가는 밤마다 과거로 이동한다. 예술가들과의 만남은 영감을 준다. 현재의 삶은 점점 초라해 보인다. 이상화된 과거 역시 완전하지 않다는 사실을 깨닫는다. 선택은 현재로 돌아오는 것이다. 삶은 지금 이곳에서 이루어진다.",
    "cast": "오웬 윌슨",
    "keywords": ["향수", "예술", "시간", "선택", "현재"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/c3bce4d2-7cdd-4aa8-1b5e-3d2335457900/public"
  },
  {
    "name": "살인의 추억",
    "director": "봉준호",
    "summary": "시골 마을에서 연쇄 살인이 발생한다. 형사들은 경험과 직감에 의존한다. 수사는 번번이 막힌다. 폭력과 억압이 일상이 된다. 진실은 끝내 잡히지 않는다. 무력감만이 남는다.",
    "cast": "송강호, 김상경",
    "keywords": ["미제사건", "폭력", "무력감", "추적", "현실"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/a3a79576-8ffd-4b7d-95a1-a52665512500/public"
  },
  {
    "name": "멜랑콜리아",
    "director": "라스 폰 트리에",
    "summary": "결혼식 날 한 여성은 깊은 우울에 빠진다. 동시에 지구로 접근하는 행성이 발견된다. 주변 사람들은 공포에 휩싸인다. 그녀는 오히려 차분해진다. 종말은 피할 수 없다. 감정과 우주의 붕괴가 겹쳐진다.",
    "cast": "커스틴 던스트",
    "keywords": ["우울", "종말", "불안", "수용", "고독"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/c2cb4d38-71d0-4798-3239-ff5351b31900/public"
  },
  {
    "name": "매치 포인트",
    "director": "우디 앨런",
    "summary": "상류층 사회에 편입된 남자는 욕망을 숨긴다. 불륜은 일상이 된다. 우연은 선택을 바꾼다. 죄책감은 점점 사라진다. 성공은 유지된다. 도덕은 운 앞에서 무력해진다.",
    "cast": "조너선 리스 마이어스, 스칼렛 요한슨",
    "keywords": ["욕망", "우연", "도덕", "계급", "위선"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/c724fe11-868f-43e1-f71a-5bbb29cbd800/public"
  },
  {
    "name": "매그놀리아",
    "director": "폴 토마스 앤더슨",
    "summary": "서로 다른 인물들의 삶이 하루 동안 교차한다. 상처는 과거에서 비롯된다. 용서는 쉽게 이루어지지 않는다. 우연한 사건은 모두를 흔든다. 관계는 다시 연결된다. 삶은 설명되지 않은 채 흘러간다.",
    "cast": "톰 크루즈, 줄리안 무어",
    "keywords": ["우연", "가족", "용서", "상처", "연결"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/75539ce3-d3ed-49da-43bc-088a237f5100/public"
  },
  {
    "name": "매드맥스: 분노의 도로",
    "director": "조지 밀러",
    "summary": "황폐한 세계에서 독재자는 물과 생명을 통제한다. 한 여성은 탈출을 감행한다. 추격은 멈추지 않는다. 폭력은 속도감 있게 이어진다. 연대는 생존의 조건이 된다. 자유를 향한 질주는 계속된다.",
    "cast": "톰 하디, 샤를리즈 테론",
    "keywords": ["추격", "해방", "폭력", "연대", "생존"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/55391cb2-730e-45d0-895c-e82988e7b000/public"
  },
  {
    "name": "사랑도 통역이 되나요?",
    "director": "소피아 코폴라",
    "summary": "낯선 도시에서 두 사람은 우연히 만난다. 언어와 문화는 장벽이 된다. 고독은 공통된 감정이다. 짧은 시간 동안 깊은 교감이 형성된다. 이별은 예정되어 있다. 기억은 오래 남는다.",
    "cast": "빌 머레이, 스칼렛 요한슨",
    "keywords": ["고독", "교감", "여행", "이별", "침묵"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/60075a30-588d-416c-9a34-8d474b820500/public"
  },
  {
    "name": "레옹",
    "director": "뤽 베송",
    "summary": "고독한 킬러는 우연히 소녀를 보호하게 된다. 폭력적인 과거는 현재를 위협한다. 두 사람은 독특한 유대를 형성한다. 감정은 점점 깊어진다. 선택은 희생으로 이어진다. 사랑은 방식이 다를 뿐 존재한다.",
    "cast": "장 르노, 나탈리 포트만",
    "keywords": ["보호", "유대", "폭력", "희생", "고독"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/86607976-1a25-45fc-11de-b20fcf102800/public"
  },
  {
    "name": "라스트 나이트 인 소호",
    "director": "에드가 라이트",
    "summary": "패션을 꿈꾸는 소녀는 과거의 환영을 보기 시작한다. 화려한 꿈은 악몽으로 변한다. 시간의 경계는 무너진다. 과거의 폭력은 현재에 영향을 미친다. 진실은 뒤틀린다. 집착은 파괴로 이어진다.",
    "cast": "토마신 맥켄지, 안야 테일러조이",
    "keywords": ["환각", "집착", "과거", "공포", "정체성"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/01ead581-5290-4e0a-7f3d-a8aa54b87200/public"
  },
  {
    "name": "레이디 버드",
    "director": "그레타 거윅",
    "summary": "고등학생 소녀는 작은 도시를 벗어나고 싶어 한다. 어머니와의 갈등은 반복된다. 우정과 사랑은 불완전하다. 선택은 늘 서툴다. 성장 과정은 실수로 가득하다. 자아는 서서히 형성된다.",
    "cast": "시얼샤 로넌",
    "keywords": ["성장", "가족", "자아", "갈등", "청춘"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/b74ca9db-84ee-49a4-5208-5197a66adb00/public"
  },
  {
    "name": "라라랜드",
    "director": "데이미언 셔젤",
    "summary": "배우를 꿈꾸는 여성과 음악가는 우연히 만난다. 사랑과 꿈은 동시에 자라난다. 현실은 이상을 시험한다. 선택은 관계를 바꾼다. 성공은 이별을 동반한다. 남은 것은 가능성이었던 기억이다.",
    "cast": "엠마 스톤, 라이언 고슬링",
    "keywords": ["꿈", "사랑", "선택", "이별", "열정"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/045c6fef-2364-41af-1930-e4b35ee28300/public"
  },
  {
    "name": "조제",
    "director": "이누도 잇신",
    "summary": "우연한 만남으로 두 사람은 관계를 시작한다. 신체적 제약은 삶의 방식을 규정한다. 사랑은 보호와 의존 사이에서 흔들린다. 미래에 대한 시선은 다르다. 관계는 점점 부담이 된다. 이별은 성장으로 남는다.",
    "cast": "츠마부키 사토시, 이케와키 치즈루",
    "keywords": ["사랑", "의존", "현실", "이별", "성장"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/382c9fcb-ce65-409b-b61f-f690b9bb3200/public"
  },
  {
    "name": "조커",
    "director": "토드 필립스",
    "summary": "사회에서 배제된 남자는 점점 고립된다. 웃음은 고통의 표현이 된다. 폭력은 축적된다. 체제에 대한 분노가 폭발한다. 개인의 붕괴는 집단의 상징이 된다. 혼돈은 확산된다.",
    "cast": "호아킨 피닉스",
    "keywords": ["붕괴", "분노", "폭력", "고립", "혼돈"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/9ef93a68-451b-4172-66aa-dcc4f56b3c00/public"
  },
  {
    "name": "인터스텔라",
    "director": "크리스토퍼 놀란",
    "summary": "지구의 환경이 붕괴되며 인류의 생존은 한계에 다다른다. 전직 파일럿은 인류를 구하기 위한 우주 탐사 임무에 참여한다. 시공간의 왜곡은 시간의 흐름을 잔혹하게 바꾼다. 가족과의 약속은 점점 멀어진다. 선택은 개인적 희생을 요구한다. 사랑은 물리 법칙을 넘어서는 힘으로 남는다.",
    "cast": "매튜 맥커너히, 앤 해서웨이",
    "keywords": ["우주", "시간", "희생", "사랑", "생존"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/f9014bd6-3c65-4000-aa3d-9d24a6502800/public"
  },
  {
    "name": "인사이드 아웃",
    "director": "피트 닥터",
    "summary": "소녀의 머릿속에서는 여러 감정들이 조화를 이루며 하루를 운영한다. 새로운 환경은 감정의 균형을 무너뜨린다. 기쁨과 슬픔은 갈등을 겪는다. 기억은 사라지거나 변형된다. 감정의 역할은 재정의된다. 성장에는 복합적인 감정이 필요하다는 사실이 드러난다.",
    "cast": "에이미 폴러, 필리스 스미스",
    "keywords": ["감정", "성장", "기억", "변화", "자아"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/5be57a13-7a1b-4b04-a98c-c7dc9e3d3c00/public"
  },
  {
    "name": "내부자들",
    "director": "우민호",
    "summary": "정치와 언론, 재벌이 얽힌 비밀 거래가 드러난다. 권력을 쥔 자들은 서로를 이용한다. 배신당한 인물은 복수를 다짐한다. 정의는 쉽게 실현되지 않는다. 거래와 음모는 반복된다. 권력의 민낯이 적나라하게 드러난다.",
    "cast": "이병헌, 조승우",
    "keywords": ["권력", "비리", "복수", "정치", "거래"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/8a5c1a78-bb5e-4ddc-a1a1-d8fe3b178c00/public"
  },
  {
    "name": "인셉션",
    "director": "크리스토퍼 놀란",
    "summary": "타인의 꿈에 침투해 정보를 훔치는 전문가가 마지막 임무를 제안받는다. 목표는 생각을 심는 것이다. 꿈속의 층위는 점점 깊어진다. 과거의 죄책감이 임무를 위협한다. 현실과 환상의 경계는 흐려진다. 선택의 결과는 열린 결말로 남는다.",
    "cast": "레오나르도 디카프리오",
    "keywords": ["꿈", "기억", "죄책감", "현실", "선택"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/27b5e6d4-a533-40be-177d-0e611b589300/public"
  },
  {
    "name": "아이, 토냐",
    "director": "크레이그 질레스피",
    "summary": "피겨 스케이팅 선수는 가혹한 환경 속에서 성장한다. 성공은 논란과 함께 찾아온다. 주변 인물들은 갈등을 증폭시킨다. 사건은 미디어에 의해 왜곡된다. 진실은 단순하지 않다. 개인은 낙인 속에 남는다.",
    "cast": "마고 로비",
    "keywords": ["논란", "미디어", "성공", "낙인", "폭력"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/a5721f56-92d9-4c4c-129d-e3118a92a800/public"
  },
  {
    "name": "아이 엠 러브",
    "director": "루카 구아다니노",
    "summary": "부유한 가문의 아내는 안정된 삶을 살고 있다. 우연한 만남은 감정을 흔든다. 욕망은 억눌려 왔던 자아를 깨운다. 선택은 가족을 위협한다. 사랑은 파괴적일 수 있다. 해방은 대가를 요구한다.",
    "cast": "틸다 스윈튼",
    "keywords": ["욕망", "해방", "가족", "사랑", "파괴"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/ba47fee8-5821-4ce9-80a0-f33756f11600/public"
  },
  {
    "name": "그녀",
    "director": "스파이크 존즈",
    "summary": "외로운 남자는 인공지능 운영체제와 관계를 맺는다. 대화는 위로가 된다. 감정은 점점 깊어진다. 기술은 인간의 결핍을 드러낸다. 관계의 한계가 드러난다. 사랑의 정의는 다시 질문된다.",
    "cast": "호아킨 피닉스",
    "keywords": ["외로움", "사랑", "기술", "관계", "정체성"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/b8417fdb-ead3-4e10-0385-65203574b800/public"
  },
  {
    "name": "그린 북",
    "director": "피터 패럴리",
    "summary": "인종차별이 심한 시대, 두 남자는 함께 여행을 떠난다. 서로 다른 배경은 갈등을 낳는다. 음악은 다리를 놓는다. 편견은 서서히 허물어진다. 우정은 예상치 못한 방향으로 깊어진다. 변화는 관계에서 시작된다.",
    "cast": "비고 모텐슨, 마허샬라 알리",
    "keywords": ["우정", "편견", "여행", "이해", "성장"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/bf033998-066c-4280-4b44-adeb6144e000/public"
  },
  {
    "name": "나를 찾아줘",
    "director": "데이비드 핀처",
    "summary": "어느 날 아내가 사라진다. 남편은 의심의 중심에 선다. 언론은 사건을 소비한다. 진실은 계획된 거짓에 가려진다. 관계의 본질은 왜곡된다. 신뢰는 완전히 무너진다.",
    "cast": "벤 애플렉, 로자먼드 파이크",
    "keywords": ["조작", "심리전", "불신", "미디어", "결혼"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/992f83d6-f0be-4530-910e-edb0f263fa00/public"
  },
  {
    "name": "포레스트 검프",
    "director": "로버트 저메키스",
    "summary": "지적 장애를 지닌 남자는 평범하게 살아간다. 우연히 역사의 순간마다 등장한다. 사랑은 늘 곁에 있다. 성공은 의도하지 않은 결과다. 삶은 단순한 태도에서 빛난다. 순수함은 세상을 바꾼다.",
    "cast": "톰 행크스",
    "keywords": ["순수", "인생", "우연", "사랑", "성실"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/3fcdd84a-4124-4b67-dda0-cbf50b3eb000/public"
  },
  {
    "name": "플립",
    "director": "롭 라이너",
    "summary": "어린 시절부터 소녀는 한 소년을 좋아한다. 감정은 엇갈린다. 성장하며 관점은 바뀐다. 가족의 가치관이 영향을 미친다. 사소한 사건들이 관계를 바꾼다. 첫사랑은 성숙으로 이어진다.",
    "cast": "매들린 캐롤, 캘런 맥오리피",
    "keywords": ["첫사랑", "성장", "관점", "가족", "순수"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/328a9ea8-2153-482c-314c-fa0f394c1b00/public"
  },
  {
    "name": "에브리씽 에브리웨어 올 앳 원스",
    "director": "다니엘 콴, 다니엘 샤이너트",
    "summary": "평범한 일상은 멀티버스로 붕괴된다. 한 여성은 무수한 가능성의 자신을 마주한다. 선택하지 않은 삶들이 동시에 펼쳐진다. 혼란은 정체성의 위기로 이어진다. 가족과의 관계가 중심이 된다. 의미는 사소한 선택에서 발견된다.",
    "cast": "양자경",
    "keywords": ["멀티버스", "정체성", "가족", "혼돈", "선택"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/f210bf6b-1b0c-4f29-6174-36f4fb0af500/public"
  },
  {
    "name": "이터널 선샤인",
    "director": "미셸 공드리",
    "summary": "헤어진 연인은 기억을 지우는 선택을 한다. 기억은 하나씩 사라진다. 감정은 끝내 지워지지 않는다. 사랑은 기억보다 깊다. 후회는 남는다. 관계의 본질이 드러난다.",
    "cast": "짐 캐리, 케이트 윈슬렛",
    "keywords": ["기억", "사랑", "후회", "상실", "관계"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/b95c473c-5c76-4b37-15db-29f933489600/public"
  },
  {
    "name": "헤어질 결심",
    "director": "박찬욱",
    "summary": "형사는 한 사건의 용의자를 조사한다. 의심은 관심으로 변한다. 감정은 직업 윤리를 흔든다. 진실은 명확하지 않다. 사랑과 의무는 충돌한다. 선택은 침묵 속에서 이루어진다.",
    "cast": "박해일, 탕웨이",
    "keywords": ["집착", "사랑", "윤리", "미스터리", "침묵"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/9a33e0ea-392c-436f-9769-78e9c9e3a000/public"
  },
  {
    "name": "다크 나이트",
    "director": "크리스토퍼 놀란",
    "summary": "도시는 새로운 범죄자에 의해 혼란에 빠진다. 영웅은 도덕적 시험에 놓인다. 질서는 쉽게 무너진다. 선택은 희생을 요구한다. 정의는 모호해진다. 악은 체제를 흔든다.",
    "cast": "크리스찬 베일, 히스 레저",
    "keywords": ["혼돈", "도덕", "희생", "정의", "대립"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/ac0d47d4-2691-477c-ffb5-8849bae7f800/public"
  },
  {
    "name": "콜드 워",
    "director": "파벨 파블리코프스키",
    "summary": "전쟁 이후 유럽에서 두 사람은 사랑에 빠진다. 정치적 현실은 이들을 갈라놓는다. 재회와 이별은 반복된다. 감정은 극단적으로 흔들린다. 사랑은 시대에 맞서 싸운다. 선택은 비극으로 이어진다.",
    "cast": "요안나 쿨리그",
    "keywords": ["사랑", "이념", "이별", "시대", "비극"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/b08a5bf5-5c5f-4a9c-8254-26dbd6a15800/public"
  },
  {
    "name": "클로저",
    "director": "마이크 니콜스",
    "summary": "네 명의 남녀는 서로 얽히며 관계를 맺는다. 진실은 쉽게 왜곡된다. 욕망은 솔직하지만 잔인하다. 사랑은 거래처럼 변한다. 상처는 반복된다. 관계의 민낯이 드러난다.",
    "cast": "줄리아 로버츠, 주드 로",
    "keywords": ["욕망", "거짓", "관계", "상처", "집착"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/6f2994ce-3a33-4451-b317-4545d0827500/public"
  },
  {
    "name": "캐치 미 이프 유 캔",
    "director": "스티븐 스필버그",
    "summary": "어린 나이에 가출한 소년은 위조와 사기로 새로운 삶을 시작한다. 뛰어난 재능은 다양한 신분으로 그를 위장하게 만든다. 추적자는 집요하게 뒤를 쫓는다. 도망은 점점 외로움으로 바뀐다. 관계는 기묘한 유대가 된다. 자유는 결국 책임으로 이어진다.",
    "cast": "레오나르도 디카프리오, 톰 행크스",
    "keywords": ["사기", "추적", "재능", "자유", "성장"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/c0a6a430-c044-4753-3ea7-bc79c7152d00/public"
  },
  {
    "name": "캐스트 어웨이",
    "director": "로버트 저메키스",
    "summary": "비행기 사고로 한 남자는 무인도에 고립된다. 문명과의 연결은 완전히 끊긴다. 생존은 모든 사고의 중심이 된다. 외로움은 상상 속 동반자를 만든다. 시간은 다른 의미로 흐른다. 돌아온 세계는 더 이상 같지 않다.",
    "cast": "톰 행크스",
    "keywords": ["고립", "생존", "시간", "외로움", "변화"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/7f6d5f16-5396-4ada-7e1b-f319ef344e00/public"
  },
  {
    "name": "캐롤",
    "director": "토드 헤인즈",
    "summary": "1950년대 사회에서 두 여성은 조심스럽게 관계를 맺는다. 사랑은 숨겨져야 한다. 시선과 침묵이 감정을 대신한다. 사회적 제약은 선택을 어렵게 만든다. 관계는 위태롭다. 사랑은 용기를 요구한다.",
    "cast": "케이트 블란쳇, 루니 마라",
    "keywords": ["사랑", "억압", "침묵", "선택", "용기"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/65ad3c41-dc19-449d-e0ea-f8ceaa6d1a00/public"
  },
  {
    "name": "가버나움",
    "director": "나딘 라바키",
    "summary": "가난 속에서 태어난 소년은 세상에 분노한다. 보호받지 못한 삶은 분노를 키운다. 아이는 어른들의 선택을 고발한다. 법정은 그의 마지막 수단이다. 생존은 어린 나이에 강요된다. 인간 존엄에 대한 질문이 남는다.",
    "cast": "자인 알 라피아",
    "keywords": ["빈곤", "아동", "분노", "생존", "현실"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/bccfd4de-b0f6-4581-492b-477b77173300/public"
  },
  {
    "name": "콜 미 바이 유어 네임",
    "director": "루카 구아다니노",
    "summary": "여름의 이탈리아에서 한 소년은 감정을 깨닫는다. 지적 교류는 사랑으로 번진다. 감정은 조심스럽게 자란다. 시간은 제한적이다. 이별은 피할 수 없다. 첫사랑은 깊은 흔적으로 남는다.",
    "cast": "티모시 샬라메, 아미 해머",
    "keywords": ["첫사랑", "성장", "이별", "감정", "기억"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/13860590-c11a-4133-db6c-5432afea0d00/public"
  },
  {
    "name": "버닝",
    "director": "이창동",
    "summary": "우연한 재회로 세 사람은 묘한 관계를 형성한다. 말하지 않는 감정들이 쌓인다. 불확실한 사건은 의심을 낳는다. 계급과 공허함이 드러난다. 진실은 끝내 명확해지지 않는다. 분노는 조용히 폭발한다.",
    "cast": "유아인, 스티븐 연",
    "keywords": ["의심", "공허", "계급", "분노", "미스터리"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/868b9f66-f19b-4163-758e-1d519dae3200/public"
  },
  {
    "name": "브루클린",
    "director": "존 크롤리",
    "summary": "더 나은 삶을 위해 한 여성은 고향을 떠난다. 낯선 도시에서 외로움은 일상이 된다. 사랑은 새로운 선택지를 제시한다. 고향으로 돌아오며 갈등은 깊어진다. 정체성은 두 세계 사이에 놓인다. 선택은 성숙을 의미한다.",
    "cast": "시얼샤 로넌",
    "keywords": ["이주", "정체성", "사랑", "선택", "성장"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/26a7a94b-aa0d-4309-e830-8822077f0500/public"
  },
  {
    "name": "브로크백 마운틴",
    "director": "이안",
    "summary": "외딴 산에서 두 남자는 관계를 맺는다. 사회는 이를 허락하지 않는다. 감정은 숨겨진 채 지속된다. 각자의 삶은 다른 방향으로 흘러간다. 재회는 아픔을 동반한다. 사랑은 평생의 상처가 된다.",
    "cast": "히스 레저, 제이크 질렌할",
    "keywords": ["사랑", "억압", "상실", "고독", "시간"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/e2b33c5a-1420-4ab0-91b3-b0d6531db200/public"
  },
  {
    "name": "블루 발렌타인",
    "director": "데릭 시언프랜스",
    "summary": "한 부부의 사랑은 과거와 현재를 오간다. 설렘은 반복되는 일상에 닳아간다. 갈등은 누적된다. 대화는 점점 줄어든다. 사랑은 유지되지 않는다. 관계의 현실이 적나라하게 드러난다.",
    "cast": "라이언 고슬링, 미셸 윌리엄스",
    "keywords": ["관계", "현실", "사랑", "마모", "이별"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/6b0dd91f-63f1-4b63-08c4-7d9b2d19c200/public"
  },
  {
    "name": "블루 재스민",
    "director": "우디 앨런",
    "summary": "부유한 삶을 잃은 여성은 새로운 환경에 적응하려 한다. 과거는 끊임없이 따라다닌다. 허영은 버려지지 않는다. 현실은 냉정하다. 정신은 점점 불안정해진다. 몰락은 피할 수 없다.",
    "cast": "케이트 블란쳇",
    "keywords": ["몰락", "허영", "현실", "불안", "상실"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/e50f7132-d95e-4fc6-dc8e-783dd2a9fb00/public"
  },
  {
    "name": "파수꾼",
    "director": "윤성현",
    "summary": "한 소년의 죽음 이후 친구들은 기억을 되짚는다. 관계 속 폭력은 쉽게 드러나지 않는다. 책임은 모호하다. 후회는 늦게 찾아온다. 청춘의 상처는 깊다. 침묵은 또 다른 폭력이다.",
    "cast": "이제훈",
    "keywords": ["청춘", "폭력", "후회", "관계", "상실"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/06d0fe9a-3b2b-4cb7-19e3-b9eba7b10b00/public"
  },
  {
    "name": "블레이드 러너 2049",
    "director": "드니 빌뇌브",
    "summary": "복제 인간을 추적하는 임무는 새로운 의문을 낳는다. 기억은 진짜와 가짜를 구분하기 어렵게 만든다. 정체성은 흔들린다. 인간과 비인간의 경계는 흐려진다. 진실은 희생을 요구한다. 존재의 의미가 질문으로 남는다.",
    "cast": "라이언 고슬링, 해리슨 포드",
    "keywords": ["정체성", "기억", "존재", "미래", "질문"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/5fd46f63-ed41-4563-dfdb-a2499bac6700/public"
  },
  {
    "name": "블랙 스완",
    "director": "대런 아로노프스키",
    "summary": "완벽한 무용수가 되기 위해 한 여성은 자신을 몰아붙인다. 경쟁은 강박으로 변한다. 환각은 현실을 잠식한다. 자아는 분열된다. 완성은 파괴를 동반한다. 예술은 대가를 요구한다.",
    "cast": "나탈리 포트만",
    "keywords": ["강박", "완벽주의", "분열", "예술", "붕괴"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/3b2d5930-03d5-4c60-f633-3225e3d46a00/public"
  },
  {
    "name": "빌리 엘리어트",
    "director": "스티븐 달드리",
    "summary": "광산촌 소년은 발레에 재능을 보인다. 주변의 반대는 거세다. 춤은 탈출구가 된다. 가족은 갈등을 겪는다. 재능은 기회를 만든다. 꿈은 계급을 넘어선다.",
    "cast": "제이미 벨",
    "keywords": ["꿈", "재능", "계급", "성장", "열정"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/b128cee6-187d-4e55-a205-4ae07e80a600/public"
  },
  {
    "name": "비포 선셋",
    "director": "리처드 링클레이터",
    "summary": "수년 만에 다시 만난 두 사람은 파리에서 대화를 나눈다. 과거의 선택은 현재를 지배한다. 말하지 못한 감정이 흘러나온다. 시간은 제한적이다. 재회의 의미는 복잡하다. 관계는 열린 결말로 남는다.",
    "cast": "에단 호크, 줄리 델피",
    "keywords": ["재회", "대화", "시간", "후회", "사랑"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/f128e1e5-1449-4459-ab61-f5295494aa00/public"
  },
  {
    "name": "비포 선라이즈",
    "director": "리처드 링클레이터",
    "summary": "기차에서 만난 두 사람은 하룻밤을 함께 보낸다. 대화는 깊어진다. 시간은 짧다. 감정은 진실하다. 이별은 예정되어 있다. 순간은 평생의 기억이 된다.",
    "cast": "에단 호크, 줄리 델피",
    "keywords": ["만남", "대화", "시간", "설렘", "이별"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/3c29cd5a-0485-4619-cc64-a84b83084d00/public"
  },
  {
    "name": "비포 미드나잇",
    "director": "리처드 링클레이터",
    "summary": "오랜 관계를 이어온 두 사람은 함께 여행한다. 일상은 갈등을 만든다. 사랑은 이상이 아니다. 감정은 날카로워진다. 관계는 위기에 놓인다. 지속은 선택의 결과다.",
    "cast": "에단 호크, 줄리 델피",
    "keywords": ["관계", "현실", "갈등", "시간", "지속"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/b5d3faa4-f1cb-4fa6-acc4-782422dff300/public"
  },
  {
    "name": "바빌론",
    "director": "데이미언 셔젤",
    "summary": "할리우드의 황금기 속에서 꿈을 좇는 이들이 모인다. 성공은 빠르다. 몰락도 빠르다. 영화 산업은 잔혹하다. 욕망은 끝이 없다. 환상은 잔해로 남는다.",
    "cast": "브래드 피트, 마고 로비",
    "keywords": ["야망", "영화산업", "성공", "몰락", "광기"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/d3d0febf-95b2-4c0f-32e4-ef877b118100/public"
  },
  {
    "name": "어톤먼트",
    "director": "조 라이트",
    "summary": "어린 시절의 오해는 비극을 만든다. 사랑은 전쟁으로 갈라진다. 죄책감은 평생을 지배한다. 시간은 되돌릴 수 없다. 글쓰기는 속죄의 수단이 된다. 진실은 늦게 도착한다.",
    "cast": "키이라 나이틀리, 제임스 맥어보이",
    "keywords": ["오해", "속죄", "전쟁", "사랑", "후회"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/5ef3e736-2331-4445-316b-c3cd44db2200/public"
  },
  {
    "name": "컨택트",
    "director": "드니 빌뇌브",
    "summary": "전 세계 곳곳에 정체불명의 외계 물체가 출현한다. 언어학자는 그들과의 소통을 위해 투입된다. 언어를 해독하는 과정에서 시간에 대한 인식이 변화한다. 개인적 상실의 기억이 현재와 겹쳐진다. 선택은 미래를 이미 알고도 받아들이는 행위가 된다. 이해는 곧 존재의 방식이 된다.",
    "cast": "에이미 애덤스, 제레미 레너",
    "keywords": ["언어", "시간", "선택", "소통", "운명"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/920a90e4-84a0-42dd-c906-728115edfe00/public"
  },
  {
    "name": "건축학개론",
    "director": "이용주",
    "summary": "한 남자는 의뢰를 통해 과거의 첫사랑을 다시 만난다. 대학 시절의 기억은 설렘과 후회로 남아 있다. 서로의 감정은 명확히 표현되지 못했다. 현재와 과거는 건축 설계처럼 겹쳐진다. 말하지 못한 감정은 끝내 완성되지 않는다. 첫사랑은 기억 속에서만 완성된다.",
    "cast": "엄태웅, 한가인, 이제훈, 수지",
    "keywords": ["첫사랑", "기억", "후회", "시간", "감정"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/59ba56cf-4f79-47a0-b3b4-28ae28c72e00/public"
  },
  {
    "name": "아멜리에",
    "director": "장피에르 주네",
    "summary": "파리의 작은 카페에서 일하는 여성은 소소한 행복을 발견한다. 타인의 삶에 개입하며 작은 기적을 만든다. 상상력은 일상을 특별하게 바꾼다. 고독은 유머로 감싸진다. 사랑 앞에서는 여전히 서툴다. 행복은 스스로 선택하는 것임을 깨닫는다.",
    "cast": "오드리 토투",
    "keywords": ["행복", "상상력", "일상", "고독", "사랑"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/9bcce71d-9894-4ba0-108f-4ed4b9f6e200/public"
  },
  {
    "name": "애프터썬",
    "director": "샬럿 웰스",
    "summary": "어린 시절의 휴가 기억이 성인이 된 딸의 시점에서 재구성된다. 아버지는 평범한 여행 속에서도 불안정함을 드러낸다. 당시에는 인식하지 못했던 감정이 뒤늦게 이해된다. 기억은 단절된 장면들로 남아 있다. 사랑은 완전하지 않았음을 깨닫는다. 상실은 시간이 지나서야 명확해진다.",
    "cast": "폴 메스칼",
    "keywords": ["기억", "부성", "상실", "회상", "침묵"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/fe15b2bc-3773-407f-dd77-9c985df7f600/public"
  },
  {
    "name": "어바웃 타임",
    "director": "리처드 커티스",
    "summary": "한 남자는 시간을 되돌릴 수 있는 능력을 알게 된다. 그는 사랑과 일상을 더 나은 방향으로 바꾸려 한다. 반복되는 선택 속에서 완벽함은 사라진다. 가족과의 순간이 가장 소중해진다. 시간의 힘은 제한적이다. 삶은 현재를 충실히 사는 것임을 깨닫는다.",
    "cast": "도널 글리슨, 레이첼 맥아담스",
    "keywords": ["시간", "사랑", "가족", "선택", "일상"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/44fd4abb-e7bf-4b1b-4ca5-684ed023df00/public"
  },
  {
    "name": "싱글맨",
    "director": "톰 포드",
    "summary": "사랑하는 이를 잃은 남자는 하루를 버텨낸다. 일상은 공허하게 반복된다. 주변의 친절은 쉽게 닿지 않는다. 기억은 고통스럽게 선명하다. 삶을 끝내려는 계획은 흔들린다. 존재의 의미는 사소한 순간에서 다시 발견된다.",
    "cast": "콜린 퍼스, 줄리안 무어",
    "keywords": ["상실", "고독", "애도", "존재", "일상"],
    "url": "https://imagedelivery.net/qmdSe0AX6QIQWTpSPOJywA/0975ff76-305a-4b14-f4a2-1ea157de5900/public"
  }
]


def seed_movies_data(db_session=None):
    """
    영화 데이터 시드 (재사용 가능한 함수)

    Args:
        db_session: SQLAlchemy session (None이면 자동 생성)

    Returns:
        tuple: (added_count, total_count)
    """
    close_session = False
    if db_session is None:
        db_session = SyncSessionLocal()
        close_session = True

    try:
        # 기존 영화 개수 확인
        existing_count = db_session.query(Movie).count()
        print(f"현재 영화 개수: {existing_count}")

        # 영화 추가
        added_count = 0
        for movie_data in SAMPLE_MOVIES:
            # 중복 체크 (영화명 + 감독으로)
            existing = db_session.query(Movie).filter(
                Movie.name == movie_data["name"],
                Movie.director == movie_data["director"]
            ).first()

            if not existing:
                movie = Movie(**movie_data)
                db_session.add(movie)
                added_count += 1

        db_session.commit()
        total_count = db_session.query(Movie).count()
        print(f"{added_count}개의 영화가 추가되었습니다.")
        print(f"총 영화 개수: {total_count}")

        return added_count, total_count

    except Exception as e:
        print(f"에러 발생: {e}")
        db_session.rollback()
        raise
    finally:
        if close_session:
            db_session.close()


def seed_movies():
    """영화 데이터 시드 (스크립트 실행용)"""
    seed_movies_data()


if __name__ == "__main__":
    print("영화 데이터 시드를 시작합니다...")
    seed_movies()
    print("완료!")
