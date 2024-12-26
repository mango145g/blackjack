import random as rd

point=0 # 플레이어 포인트
maximum=0 #딜러 최대치
turn=0 #턴 수
DealMoney=0 #베팅 포인트
breaking=False #반복문 빠져나가기용
cards=['A','2','3','4','5','6','7','8','9','10','J','Q','K'] #카드
deal=[] #딜러 패
FakeDeal=[] #보여주기 용 딜러 패
play=[] #플레이어 패
DiffPt={'easy':50000,'normal':30000,'hard':20000} #난이도에 따른 포인트
DiffMax={'easy':16,'normal':17,'hard':18} #난이도에 따른 최대치
notice1=''' 
난이도를 선택해주세요.(easy/normal/hard)
(초기자금과 딜러가 멈추는 숫자에 차이가 있습니다.)
:''' #안내문1
notice2='''
원하시는 행동을 입력해주세요.
(point:포인트 확인 dealer:딜러 카드 보기,player:내 카드 보기,hit:힛,stay:스테이,double:더블다운(주의! 더블다운은 첫 턴에만 가능합니다.))
:''' #안내문2
wrong='잘못된 입력입니다.' #안내문 3
#카드 뽑기
def draw():
  num=rd.randrange(0,13)
  return cards[num]
#난이도 확인하기
def check(DiffIn):
  exp={'easy':'난이도:쉬움(초기자금:50000 pt,딜러 최대치:16)','normal':'난이도:보통(초기자금:30000 pt,딜러 최대치:17)','hard':'난이도:어려움(초기자금:20000 pt,딜러 최대치:18)'}
  add=exp.get(DiffIn)
  while True:
    ans=input('이 난이도가 맞습니까? %s (Y/N):'%add)
    if ans=='Y' or ans=='y':
      return True
    elif ans=='N' or ans=='n':
      return False
    else:
      print(wrong)
#합계 계산하기
def cal(deck:list):
  add=0
  ace=0
  for card in deck:
    if card.isdecimal():
      card=int(card)
      add+=card
    else:
      if card=='A':
        ace+=1
      else:
        add+=10
  if ace>0:
    add+= ace * 11
    while ace !=0 and add>21:
      add-=10
      ace-=1
    return add
  else: return add
#패 보여주기
def show(deck:list):
  if deck == FakeDeal or deck == deal:
    print('딜러의 패:',end='')
  elif deck == play:
    print('플레이어의 패:', end='')
  for card in deck:
    print(card, end=' ')
#베팅 금액 설정
def bet():
  global point,DealMoney
  while True:
    BetMoney= input('베팅할 포인트를 입력해주세요:')
    if not BetMoney.isdecimal():
      print(wrong)
      continue
    BetMoney= int(BetMoney)
    if BetMoney<100:
      print('최소 베팅 포인트는 100포인트입니다.')
    elif BetMoney>point:
      print('가지고 있는 포인트보다 많은 포인트를 베팅하셨습니다.')
    else:
      DealMoney += BetMoney
      point -= BetMoney
      break
#시작 여부 질문
def ready():
  global breaking
  while True:
    rea=input('시작하시겠습니까?(현재 자산: %d pt)(Y/N):' %point)
    if rea=='Y' or rea=='y':
      print('게임을 시작합니다.')
      break
    elif rea=='N' or rea=='n':
      print('게임을 끝내고 정산합니다.')
      breaking=True
      break
    else:
      print(wrong)
#난이도 설정
while True:
  diff=input(notice1)
  if diff=='easy' or diff=='normal' or diff=='hard':
    if check(diff):
      print('%s 난이도로 설정하셨습니다.'%diff)
      point=DiffPt.get(diff)
      maximum=DiffMax.get(diff)
      break
    else:
      print('다시 입력받습니다.')
  else:
    print(wrong)
#본게임
while True:
  if point<100:
    print('더이상 베팅할 수 없으므로 정산합니다.')
    break
  ready()
  if breaking:
    break
  DealMoney=0
  deal=[]
  FakeDeal=[]
  play=[]
  bet()
  turn=1
  print('딜러와 플레이어님이 두 장씩 뽑습니다.')
  deal.append(draw())
  deal.append(draw())
  play.append(draw())
  play.append(draw())
  FakeDeal.append(deal[0])
  FakeDeal.append('?')
  show(FakeDeal)
  show(play)
  while True:
    answer=input(notice2)
    if answer=='dealer':
      show(FakeDeal)
    elif answer=='player':
      show(play)
    elif answer=='point':
      print('가지고 계신 포인트:',point,'베팅하신 포인트:',DealMoney)
    elif answer=='hit':
      play.append(draw())
      print('카드 %s를 뽑으셨습니다' %play[-1])
      turn += 1
      if cal(play)>21:
        break
    elif answer=='double' and turn==1:
      if  DealMoney>point:
        print('돈이 모자릅니다')
        continue
      point -= DealMoney
      DealMoney *= 2
      play.append(draw())
      print('카드 %s를 뽑으셨습니다' %play[-1])
      break
    elif answer=='stay':
      print('스테이 하셨습니다')
      break
    else:
      print(wrong)
  print('플레이어님의 총합은 %s 입니다' %cal(play))
  if cal(play)>21:
    print('버스트하셔서 패배하셨습니다.')
    continue
  elif cal(play)==21:
    print('블랙잭입니다! 딜러가 블랙잭을 뽑지 않는다면 두배로 돈을 가져갑니다.')
  print('딜러의 패를 공개합니다')
  show(deal)
  while cal(deal)<maximum:
    print('딜러의 총합은 %s 입니다' %cal(deal))
    print('딜러가 카드를 뽑습니다')
    deal.append(draw())
    show(deal)
  print('딜러의 총합은 %s 입니다' %cal(deal))
  if cal(deal)>21:
    print('딜러가 버스트 하였으므로 당신의 승리입니다.')
  elif cal(deal)<cal(play):
    print('플레이어님이 21에 더 가까우므로 플레이어님의 승리입니다.')
  elif cal(deal)==cal(play):
    print('플레이어님과 딜러가 같은 값이므로 무승부입니다')
    print('베팅한 돈을 돌려받습니다')
    point += DealMoney
    continue
  else:
    print('딜러가 21에 더 가까우므로 플레이어님의 패배입니다.')
    continue
  if cal(play)==21:
    print('블랙잭이므로 베팅한 돈의 2배를 가져갑니다!')
    point += DealMoney * 2
  else:
    print('베팅한 돈의 1.5배를 가져갑니다!')
    point += int(DealMoney * 1.5)
#정산
profit=point-DiffPt.get(diff)
print('원래 포인트:%d pt 현재 포인트:%d pt 총 손익:%d pt'%(DiffPt.get(diff),point,profit)) 
