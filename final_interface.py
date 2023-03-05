import cv2
import math
import random
import numpy as np

# 소연이 테스트 파일
img1 = cv2.imread('image/test_img1.png', cv2.IMREAD_COLOR)
img2 = cv2.imread('image/test_img1.png', cv2.IMREAD_COLOR)
img3 = cv2.imread('image/test_img1.png', cv2.IMREAD_COLOR)
img4 = cv2.imread('image/test_img1.png', cv2.IMREAD_COLOR)
img5 = cv2.imread('image/test_img1.png', cv2.IMREAD_COLOR)
img6 = cv2.imread('image/test_img1.png', cv2.IMREAD_COLOR)
imgcolor = cv2.imread('image/test_newimg2.png', cv2.IMREAD_COLOR)

# 성아 테스트 파일
# img1 = cv2.imread('images/result2/test_img1.png', cv2.IMREAD_COLOR)
# img2 = cv2.imread('images/result2/test_img1.png', cv2.IMREAD_COLOR)
# img3 = cv2.imread('images/result2/test_img1.png', cv2.IMREAD_COLOR)
# img4 = cv2.imread('images/result2/test_img1.png', cv2.IMREAD_COLOR)
# img5 = cv2.imread('images/result2/test_img1.png', cv2.IMREAD_COLOR) # 잔주름 위치 지정할때 사용하기
# imgcolor = cv2.imread('images/result2/test_newimg2.png', cv2.IMREAD_COLOR)
# img1 = cv2.imread('images/result1/man32_normal_test_cut.png', cv2.IMREAD_COLOR)
# img2 = cv2.imread('images/result1/man32_normal_test_cut.png', cv2.IMREAD_COLOR)
# img3 = cv2.imread('images/result1/man32_normal_test_cut.png', cv2.IMREAD_COLOR)
# img4 = cv2.imread('images/result1/man32_normal_test_cut.png', cv2.IMREAD_COLOR)
# img5 = cv2.imread('images/result1/man32_normal_test_cut.png', cv2.IMREAD_COLOR) # 잔주름 위치 지정할때 사용하기
# imgcolor = cv2.imread('images/result1/man32_color_test_cut.png', cv2.IMREAD_COLOR)

h1, w1 = img1.shape[:2] # image1 size
normal_x1 = [] # image1 normal vector
normal_y1 = []
normal_z1 = []
normal_x2 = [] # image1 normal vector
normal_y2 = []
normal_z2 = []
colorx=[] #image1 color num
colory=[]
colorz=[]
draw_range = []
sin_name = 'bar'
pensize=20 # 펜 사이즈
pensizearg=[]
oldx = doly = -1
endpoint=[] # 중심 주름의 외곽 점들
blackline=[] #모든 검은 라인
blacklinemini=[] #모든 검은 라인의 가까운 부분들
blackmiddleline=[]  #가운데 라인
# 이미지 4에서는 두껍게 그려지고 이미지 3에서는 얇게 주름이 그려짐
blacklinechecknum=[] # 기존의 라인이 이미 생성되었는지 아닌지 판단하는 변수 1이면 지나감 img4에서 판단함
blacklinechecknum3=[] # 기존의 라인이 이미 생성되었는지 아닌지 판단하는 변수 1이면 지나감 img3에서 판단함
bluelinechecknum=[] # 기존의 라인이 이미 생성되었는지 아닌지 판단하는 변수 1이면 지나감 img4에서 판단함
bluelinechecknum3=[] # 기존의 라인이 이미 생성되었는지 아닌지 판단하는 변수 1이면 지나감 img3에서 판단함
end_neardispoint=[]  # 외곽 점에서 가장 가까운 주름 중심점 찾기
all_neardispoint=[] # 모든 점으로부터 가장 가까운 주름 중심점 찾기 - blackline
all_neardis=[] # 모든 점으로부터 가장 가까운 주름 중심점 거리 값 - blackline
leftright=[] # 주름을 반으로 나눴을때 어느쪽에 있고 거리가 얼마되는지 [0,거리] / [1, 거리]
findstarttwopoint=[] # 주름 외곽점의 시작점
findmiddletwopoint=[] # 주름의 중간점
findendtwopoint=[] # 주름 외곽점의 끝점
outbig_nearpoint=[] # outbig_nearpoint 큰 바깥 쪽 좌표 담긴 배열
outbig_neardispoint = [] # outbig_neardispoint 바깥 쪽 좌표와 가장 가까운 주름 중심선 좌표 담긴 배열
outbig_neardis = [] # outbig_neardis 바깥 쪽 좌표와 가장 가까운 주름 중심선과의 거리가 담긴 배열
linestren=[] # line 두께 - 라인 설정 값 0, 1, 2
line_age= [] # age 설정값
line_color_deep= [] # skin texture color 진하기 설정값
color_weight1 =[] # skin texture 가중치 1
color_weight2 =[] # skin texture 가중치 2
blackcheck=[] # 잔주름이 생성된 곳인지 아닌지 판단
startpoint=[] # 마우스 시작점
downupmouse_num = 0 #마우스로 그린 숫자 / 사용자가 그린 주름 스케치 갯수
mousestr = [] # 마우스 시작점 저장하는 곳
mouseend = [] # 마우스 끝점 저장하는 곳
pointmiddle=[] # 주름의 가운데 점 저장

global i
global strMX, strMY, endMY, endMX # 마우스 시작점 끝점
i=0

for i in range(h1):
    for j in range(w1):
        normal_x1.append((img1[i, j][2] / 255) * 2 - 1)
        normal_y1.append((img1[i, j][1] / 255) * 2 - 1)
        normal_z1.append((img1[i, j][0] / 255) * 2 - 1)
        normal_x2.append((img1[i, j][2] / 255) * 2 - 1)
        normal_y2.append((img1[i, j][1] / 255) * 2 - 1)
        normal_z2.append((img1[i, j][0] / 255) * 2 - 1)
        colorx.append(imgcolor[i, j][2])
        colory.append(imgcolor[i, j][1])
        colorz.append(imgcolor[i, j][0])
        blacklinechecknum.append(0)
        blacklinechecknum3.append(0)
        bluelinechecknum.append(0)
        bluelinechecknum3.append(0)
        blackcheck.append(0)

def on_mouse(event, x, y, flags, param):

    global oldx, oldy
    global strMX, strMY, endMY, endMX
    global downupmouse_num

    if event == cv2.EVENT_LBUTTONDOWN:
        strMX = y
        strMY = x
        oldx, oldy = x, y
        startpoint.append([strMX, strMY])
        mousestr.append([x, y])
        pensizearg.append(pensize)
        downupmouse_num = downupmouse_num + 1
        print('EVENT_DOWN: %d, %d' % (x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        endMX = y
        endMY = x
        mouseend.append([endMX, endMY])
        use() # 잔주름 만들때 사용하는 함수
        print('EVENT_UP: %d, %d' % (x, y))

    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            cv2.line(img1, (oldx, oldy), (x, y), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.line(img4, (oldx, oldy), (x, y), (0, 0, 0), pensize, cv2.LINE_AA)
            cv2.line(img3, (oldx, oldy), (x, y), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.line(img5, (oldx, oldy), (x, y), (0, 0, 255), 15, cv2.LINE_AA)
            oldx, oldy = x, y

    elif event == cv2.EVENT_RBUTTONDOWN:
        print('EVENT_RBUTTONDOWN')
        # img 1 사용자가 직접 그리는 곳
        # img 2 결과 나오는 곳
        # img 3 주름 중심 라인만 그려지게 얇은
        # img 4 두꺼운 주름 그려지는거
        # img 5 잔주름 그려지는 위치 정하기
        findblacknear()
        janline() # 잔주름 생성
        findoutline(blackline)
        find_end_nearpoint()
        find_all_nearpoint()
        find_last_two_point()
        findnear()
        matrixconvert()
        colorchange()
        cv2.imwrite('imgsave/facenormal.png', img2)
        cv2.imshow('img2', img2)
        cv2.imshow('img1', img1)
        cv2.imshow('colorimg', imgcolor)
        #save()

def save():
    src = cv2.imread('image/original.png', cv2.IMREAD_UNCHANGED) #원본 이미지
    for i in range(850):
        for j in range(600):
            src[800 + i, j][2] = img2[599 - j, i][2]
            src[800 + i, j][1] = img2[599 - j, i][1]
            src[800 + i, j][0] = img2[599 - j, i][0]
    save_file = "imgsave/img20.png"  # 저장 이름
    cv2.imwrite(save_file, src)

    src = cv2.imread('image/test_img2.png', cv2.IMREAD_UNCHANGED) #원본 이미지
    for i in range(850):
        for j in range(600):
            src[800 + i, j][2] = imgcolor[599 - j, i][2]
            src[800 + i, j][1] = imgcolor[599 - j, i][1]
            src[800 + i, j][0] = imgcolor[599 - j, i][0]
    save_file = "imgsave/img20color.png"  # 저장 이름
    cv2.imwrite(save_file, src)

def div_range_draw(): # 9분할하는거 img 6으로 확인하는 코드
    h_range1 = int(h1/3)
    h_range2 = int((h1 / 3)*2)
    w_range1 = int(w1/3)
    w_range2 = int((w1/3)*2)
    for i in range(h1):
        for j in range(w1):
            if (i == h_range1 or i == h_range2 or j == w_range1 or j == w_range2):
                img6[i, j][2] = 255
                img6[i, j][1] = 0
                img6[i, j][0] = 0

def div_range(x, y): # 그린 좌표가 몇 분할인지 계산해서 알려주는 코드
    range_num = 0
    h_range1 = int(h1/3)
    h_range2 = int((h1 / 3)*2)
    w_range1 = int(w1/3)
    w_range2 = int((w1/3)*2)
    if(x <= h_range1 and y <= w_range1):
        range_num = 1
    elif (x <= h_range1 and y <= w_range2):
        range_num = 2
    elif (x <= h_range1 and y > w_range2):
        range_num = 3
    elif (x <= h_range2 and y <= w_range1):
        range_num = 4
    elif (x <= h_range2 and y <= w_range2):
        range_num = 5
    elif (x <= h_range2 and y > w_range2):
        range_num = 6
    elif (x > h_range2 and y <= w_range1):
        range_num = 7
    elif (x > h_range2 and y <= w_range2):
        range_num = 8
    elif (x > h_range2 and y > w_range2):
        range_num = 9
    return range_num

def colorextraction(): #모든 검은 점 찾는 함수
    blackline.append([])
    blacklinemini.append([])
    for i in range(h1):
        for j in range(w1):
            if(img4[i, j][2]==0 and img4[i, j][1]==0 and img4[i, j][0]==0 and blacklinechecknum[i*w1+j]==0):
                blacklinechecknum[i * w1 + j]=1
                blackline[colorextraction.count1].append([i,j])
                # 잔주름 위치 지정할 때 쓰이는 범위 저장
                if (img5[i, j][2] == 255 and img5[i, j][1] == 0 and img5[i, j][0] == 0):
                    img4[i, j][2] = 255
                    img4[i, j][1] = 0
                    img4[i, j][0] = 0
                    # 가까이 있는 경우 - 아래 의미 없음 : 가까이 있는 경우 포함 X
                    n = 1
                else:
                    # 멀리 있는 경우 : 멀리 중에서 랜덤으로
                    blacklinemini[colorextraction.count1].append([i, j])
            if(img4[i, j][2]==0 and img4[i, j][1]==0 and img4[i, j][0]==255 and bluelinechecknum[i*w1+j]==0):
                blackline[colorextraction.count1].append([i, j])
                bluelinechecknum[i*w1+j]=1
    colorextraction.count1+=1

def colorextraction3(): #가운데 라인 찾는 함수
    blackmiddleline.append([])
    for i in range(h1):
        for j in range(w1):
            if(img3[i, j][2]==0 and img3[i, j][1]==0 and img3[i, j][0]==0 and blacklinechecknum3[i*w1+j]==0):
                blacklinechecknum3[i * w1 + j]=1
                blackmiddleline[colorextraction3.count2].append([i,j])
            if (img3[i, j][2] == 0 and img3[i, j][1] == 0 and img3[i, j][0] == 255 and bluelinechecknum3[i*w1+j]==0):
                blackmiddleline[colorextraction3.count2].append([i, j])
                bluelinechecknum3[i*w1+j]=1
    colorextraction3.count2+=1

def use():
    linestren.append(line_strength)
    line_age.append(age)
    line_color_deep.append(color_deep)
    colorextraction()
    colorextraction3()

def janline(): # 잔주름 생성하기
    for i in range(len(blackline)): # 선의 갯수만큼 도는 거
        if draw_range[i] == 2 or draw_range[i] == 4 or draw_range[i] == 6:
            print("나이: ", line_age[i])
            jannum = 0
            if (line_age[i] > 70):
                uu = random.randint(3, 4)
                jannum = uu
            elif (line_age[i] > 50):
                uu = random.randint(2, 3)
                jannum = uu
            elif (line_age[i] > 30):
                uu = random.randint(1, 2)
                jannum = uu
            elif (line_age[i] > 20):
                uu = random.randint(0, 1)
                jannum = uu
            else:
                jannum = 0
            for k in range(jannum):  # 잔주름 생성 갯수
                draw_range.append(draw_range[i])
                mousestr.append([mousestr[i][0], mousestr[i][1]])  # 주름 중심선 값 -> 같은 방향성이기 때문에
                mouseend.append([mouseend[i][0], mouseend[i][1]])
                a = len(blackmiddleline[i])  # 중심 주름선 점에서 랜덤으로 한 점 뽑아내기
                loop = random.randrange(30, 50)  # 잔주름 길이
                print("잔주름 길이 : ", loop, "잔주를 갯수 : ", jannum)
                if (a < loop):
                    rannum = 0
                    loop = a
                else:
                    rannum = random.randint(0, a - loop)
                b = len(blacklinemini[i])  # 잔주름 바깥 위치 지정할 때 사용
                rannum2 = random.randint(0, b)
                loopt = []
                print("따올 중심 주름의 위치 랜덤 숫자 : ", rannum, "잔주름 위치 랜덤 숫자 : ", rannum2)
                for kk in range(loop):  # 잔주름 길이만큼
                    for kkk in range(loop):  # rannum 중심으로 사각형 범위 저장
                        blackx = int(blackmiddleline[i][int(rannum)][0] + kk - (loop / 2))
                        blacky = int(blackmiddleline[i][int(rannum)][1] + kkk - (loop / 2))
                        loopt.append([blackx, blacky])
                        blackcheck[blackx * w1 + blacky] = 1
                dis = 0
                middlefirstx = startpoint[i][0]
                middlefirsty = startpoint[i][1]
                mindis = 100000  # 최소 거리 값
                firstpointx = 0  # 사각형 내부에서의 시작점
                firstpointy = 0
                simplemidline = []  # 사각형 내에 주름 중심선에 해당되는 부분들
                for kk in range(len(loopt)):  # 사각형 안에 있는 점들 위치값
                    # 사각형안에서 주름인 점을 저장 => 주름중심선만
                    if (img1[loopt[kk][0], loopt[kk][1]][2] == 0 and img1[loopt[kk][0], loopt[kk][1]][1] == 0 and
                            img1[loopt[kk][0], loopt[kk][1]][0] == 0):
                        dis = math.sqrt(((loopt[kk][0] - middlefirsty) * (loopt[kk][0] - middlefirsty)) + (
                        ((loopt[kk][1] - middlefirstx) * (loopt[kk][1] - middlefirstx))))
                        simplemidline.append([loopt[kk][1], loopt[kk][0]])
                        if mindis > dis:
                            mindis = dis
                            firstpointx = loopt[kk][1]
                            firstpointy = loopt[kk][0]
                # cv2.circle(img1, (middlefirstx, middlefirsty), 5, (0, 255, 0))
                #cv2.circle(img1, (int(blackmiddleline[i][int(rannum)][1]), int(blackmiddleline[i][int(rannum)][0])), 5,(0, 0, 255))
                #cv2.circle(img1, (firstpointx, firstpointy), 5, (255, 0, 0))
                # 주름 중심선 랜덤 값과 바깥 랜덤 값의 거리 차
                calx = blacklinemini[i][rannum2][0] - blackmiddleline[i][rannum][0]
                caly = blacklinemini[i][rannum2][1] - blackmiddleline[i][rannum][1]

                # 사각형 값들 바깥 랜덤 값 위치로 복사 복붙
                for kk in range(len(simplemidline)):
                    simplemidline[kk][0] += caly
                    simplemidline[kk][1] += calx

                # 이미지3, 4에서 잔주름 그려주기
                rex = simplemidline[0][0]
                rey = simplemidline[0][1]
                for kk in range(len(simplemidline)):
                    cv2.line(img3, (rex, rey), (simplemidline[kk][0], simplemidline[kk][1]), (255, 0, 0), 1,
                             cv2.LINE_AA)
                    cv2.line(img4, (rex, rey), (simplemidline[kk][0], simplemidline[kk][1]), (255, 0, 0), 30,
                             cv2.LINE_AA)
                pensizearg.append(30)
                use()

def findoutline(list): #외곽 찾는 함수
    # blackline 리스트 가 들어옴.
    print("list길이", len(list))
    for i in range(len(list)):

        endpoint.append([])
        # 외곽점 저장하기
        # 상하좌우 비교해서 검은 색이 아닌 점이라면 외곽점으로 판단
        # endpoint 생성
        for k in range(len(list[i])):
            pot = []
            check = 0
            pot.append([list[i][k][0] + 1, list[i][k][1] + 1])
            pot.append([list[i][k][0] - 1, list[i][k][1] + 1])
            pot.append([list[i][k][0] + 1, list[i][k][1] - 1])
            pot.append([list[i][k][0] - 1, list[i][k][1] - 1])
            for j in range(len(pot)):
                if (pot[j] not in list[i]):
                    check = 1
            if (check == 1):
                endpoint[i].append([list[i][k][0], list[i][k][1]])

def find_end_nearpoint(): #가운데 라인점으로 부터 외곽점과 가까운 점 찾기
    x=0
    y=0
    for i in range(len(endpoint)): # 제일 외곽점
        end_neardispoint.append([])
        for j in range(len(endpoint[i])):
            dis = 1000000
            for kk in range(len(blackmiddleline[i])):
                caldis = math.sqrt((blackmiddleline[i][kk][0] - endpoint[i][j][0]) * (
                            blackmiddleline[i][kk][0] - endpoint[i][j][0]) + (
                                               blackmiddleline[i][kk][1] - endpoint[i][j][1]) * (
                                               blackmiddleline[i][kk][1] - endpoint[i][j][1]))
                if caldis < dis:
                    dis = caldis
                    x = blackmiddleline[i][kk][0]
                    y = blackmiddleline[i][kk][1]
            end_neardispoint[i].append([x,y])

def find_all_nearpoint(): #모든 검은 점으로 부터 가까운 가운데라인 점 찾기
    x=0
    y=0
    for i in range(len(blackline)): # 선의 갯수
        all_neardispoint.append([])
        all_neardis.append([])
        maxdis = 0
        print(draw_range[i])
        for j in range(len(blackline[i])):

            dis = 1000000
            # 제일 가까운 주름 중심선 점 찾기
            for kk in range(len(blackmiddleline[i])):
                caldis = math.sqrt((blackmiddleline[i][kk][0] - blackline[i][j][0]) * (
                            blackmiddleline[i][kk][0] - blackline[i][j][0]) + (
                                               blackmiddleline[i][kk][1] - blackline[i][j][1]) * (
                                               blackmiddleline[i][kk][1] - blackline[i][j][1]))
                if (blackmiddleline[i][kk][0] == blackline[i][j][0] and blackmiddleline[i][kk][1] == blackline[i][j][1]):
                    caldis = dis
                if caldis < dis:
                    dis = caldis
                    x = blackmiddleline[i][kk][0]
                    y = blackmiddleline[i][kk][1]
            all_neardispoint[i].append([x,y])
            all_neardis[i].append(dis)
            if maxdis < dis:
                maxdis = dis
        # 한번더 값 수정
        if (draw_range[i] == 7 or draw_range[i] == 9):
            for j in range(len(all_neardis[i])):
                all_neardis[i][j] = (all_neardis[i][j] / maxdis) * 0.8

        maxdis2 = 0

        for j in range(len(all_neardispoint[i])):
            if (all_neardis[i][j] > 0):
                if (draw_range[i]==7 or draw_range[i]==9):
                    # 볼록의 가중치 정도
                    if (line_age[i] > 70):
                        weight = 0.3
                    elif (line_age[i] > 50):
                        weight = 0.5
                    elif (line_age[i] > 30):
                        weight = 0.7
                    elif (line_age[i] > 20):
                        weight = 0.8
                    else:
                        weight = 1
                    all_neardis[i][j] = ((all_neardis[i][j]) / ((all_neardis[i][j] * all_neardis[i][j]) + weight))
                else:
                    all_neardis[i][j] = math.log10(all_neardis[i][j])
            if maxdis2 < all_neardis[i][j]:
                maxdis2 = all_neardis[i][j]
        # maxdis 전체 선에 대한 최대길이값
        # 0~1 로 다시 수정
        for j in range(len(all_neardis[i])):
            all_neardis[i][j] = (all_neardis[i][j]/maxdis2)

def point2_distance(x1, y1,x2, y2): # 두 점에 대한 길이값 리턴
    a = x1 - x2
    b = y1 - y2
    d = math.sqrt((a*a)+(b*b))
    return d

def find_last_two_point():  #끝점2개 찾기
    for k in range(len(endpoint)): # 선의 갯수
        n = len(blackmiddleline[k]) #모든 점의 갯수
        # 주름 중심선에서 찾는 점들
        min_x = 100000  # 가장 작은 x 값
        min_x_point = 0 # 가장 작은 x 값을 가진 점
        max_x = 0 # 가장 큰 x 값
        max_x_point = 0 # 가장 큰 x 값을 가진 점
        min_y = 100000 # 가장 작은 y 값
        min_y_point = 0 # 가장 작은 y 값을 가진 점
        max_y = 0 # 가장 큰 y 값
        max_y_point = 0 # 가장 큰 y 값을 가진 점
        for j in range(len(blackmiddleline[k])):
            if min_x > blackmiddleline[k][j][1]:
                min_x = blackmiddleline[k][j][1]
                min_x_point = j
            if max_x < blackmiddleline[k][j][1]:
                max_x = blackmiddleline[k][j][1]
                max_x_point = j
            if min_y > blackmiddleline[k][j][0]:
                min_y = blackmiddleline[k][j][0]
                min_y_point = j
            if max_y < blackmiddleline[k][j][0]:
                max_y = blackmiddleline[k][j][0]
                max_y_point = j
        #cv2.circle(img1, (blackmiddleline[k][min_x_point][1], blackmiddleline[k][min_x_point][0]), 2, (255, 255, 0), thickness=-1)  # m1, m2 가 선 시작 부근의 끝점 x, y
        #cv2.circle(img1, (blackmiddleline[k][max_x_point][1], blackmiddleline[k][max_x_point][0]), 2, (255, 255, 0), thickness=-1)  # mm1, mm2 가 선 끝 부근의 끝점 x, y
        #cv2.circle(img1, (blackmiddleline[k][min_y_point][1], blackmiddleline[k][min_y_point][0]), 2, (255, 255, 0), thickness=-1)  # m1, m2 가 선 시작 부근의 끝점 x, y
        #cv2.circle(img1, (blackmiddleline[k][max_y_point][1], blackmiddleline[k][max_y_point][0]), 2, (255, 255, 0), thickness=-1)  # mm1, mm2 가 선 끝 부근의 끝점 x, y

        if abs(mousestr[k][0] - mouseend[k][0]) > abs(mousestr[k][1] - mouseend[k][1]):  # x 축 변화량 크다 위아래 선
            fx = blackmiddleline[k][min_y_point][1]  # 주름 중심선 첫번째
            fy = blackmiddleline[k][min_y_point][0]
            ex = blackmiddleline[k][max_y_point][1]  # 주름 중심선 끝점
            ey = blackmiddleline[k][max_y_point][0]
        else:  # y 축 변화량 크다 좌우 선
            fx = blackmiddleline[k][min_x_point][1]  # 주름 중심선 첫번째
            fy = blackmiddleline[k][min_x_point][0]
            ex = blackmiddleline[k][max_x_point][1]  # 주름 중심선 끝점
            ey = blackmiddleline[k][max_x_point][0]
        mmm = 0
        mmm2 = 0
        for kk in range(len(endpoint[k])): # 외곽점
            # 주름 중심선과 시작점 거리 < 펜사이즈/2
            if point2_distance(fx, fy, endpoint[k][kk][1], endpoint[k][kk][0]) < (pensizearg[k] / 2):
                if point2_distance(blackmiddleline[k][2][1], blackmiddleline[k][2][0], endpoint[k][kk][1], endpoint[k][kk][0]) > mmm:
                    mmm = point2_distance(blackmiddleline[k][2][1], blackmiddleline[k][2][0], endpoint[k][kk][1], endpoint[k][kk][0])
                    m1 = endpoint[k][kk][1]
                    m2 = endpoint[k][kk][0]
            if point2_distance(ex, ey, endpoint[k][kk][1], endpoint[k][kk][0]) < (pensizearg[k]/ 2):
                if point2_distance(blackmiddleline[k][n - 3][1], blackmiddleline[k][n - 3][0], endpoint[k][kk][1],
                                   endpoint[k][kk][0]) > mmm2:
                    mmm2 = point2_distance(blackmiddleline[k][n - 3][1], blackmiddleline[k][n - 3][0], endpoint[k][kk][1],
                                           endpoint[k][kk][0])
                    mm1 = endpoint[k][kk][1]
                    mm2 = endpoint[k][kk][0]
        findstarttwopoint.append([m1,m2]) # 전체 선에서 제일 첫번째 끝점
        findendtwopoint.append([mm1,mm2]) # 전체 선에서 제일 마지막 끝점
        #cv2.circle(img1, (m1, m2), 2, (0, 255, 0), thickness=-1) # m1, m2 가 선 시작 부근의 끝점 x, y
        #cv2.circle(img1, (mm1, mm2), 2, (0, 255, 0), thickness=-1) # mm1, mm2 가 선 끝 부근의 끝점 x, y
        middle_x = int((m1 + mm1) / 2)
        middle_y = int((m2 + mm2) / 2) # 위 두점 반띵한 중심 점
        min_x = 0
        min_y = 0
        min_dis = 10000000

        for kk in range(len(blackmiddleline[k])):
            if point2_distance(middle_x, middle_y, blackmiddleline[k][kk][1], blackmiddleline[k][kk][0]) < min_dis:
                min_x = blackmiddleline[k][kk][1]
                min_y = blackmiddleline[k][kk][0]
        findmiddletwopoint.append([min_x, min_y]) # 전체 선에서 제일 중심인 점

def findblacknear(): # 선의 중심점 찾아주기 (정확히 중심은 아니고 대량 중심...)

    for i in range(len(blackline)):  # 선의 갯수 만큼
        minus = 10000
        xpoint = 0
        ypoint = 0
        pointmiddle.append([])
        for j in range(len(blackline[i])):  # 전체 점 수
            dis1 = math.sqrt(
                (blackline[i][j][1] - mousestr[i][0]) * (blackline[i][j][1] - mousestr[i][0]) + (
                            blackline[i][j][0] - mousestr[i][1]) * (
                            blackline[i][j][0] - mousestr[i][1]))
            dis2 = math.sqrt(
                (blackline[i][j][1] - mouseend[i][1]) * (blackline[i][j][1] - mouseend[i][1]) + (
                            blackline[i][j][0] - mouseend[i][0]) * (blackline[i][j][0] - mouseend[i][0]))
            if (abs(dis1 - dis2) < minus):
                minus = abs(dis1 - dis2)
                xpoint = blackline[i][j][1]
                ypoint = blackline[i][j][0]
        cv2.circle(img1, (xpoint, ypoint), 2, (0, 0, 255), thickness=-1)
        pointmiddle[i].append([xpoint, ypoint])
        draw_range.append(div_range(ypoint, xpoint))



def findnear():
    one=0
    two=0
    big1=0
    big2=0
    for i in range(len(blackline)): # 선의 갯수 만큼
        leftright.append([])
        for j in range(len(blackline[i])): # 전체 점 수
            dis1 = math.sqrt((blackline[i][j][1]-findstarttwopoint[i][0])*(blackline[i][j][1]-findstarttwopoint[i][0])+(blackline[i][j][0]-findstarttwopoint[i][1])*(blackline[i][j][0]-findstarttwopoint[i][1]))
            dis2 = math.sqrt((blackline[i][j][1] - findendtwopoint[i][0]) * (blackline[i][j][1] - findendtwopoint[i][0]) + (blackline[i][j][0] - findendtwopoint[i][1]) * (blackline[i][j][0] - findendtwopoint[i][1]))

            # 왼쪽 오른쪽 판단
            if dis1<=dis2:
                leftright[i].append([0,dis1])

                #cv2.circle(img1, (blackline[i][j][1],blackline[i][j][0]), 1, (0, 0, 255), thickness=-1)
                if big1<dis1:
                    big1 = dis1
                one +=1
            else:
                leftright[i].append([1,dis2])
                #cv2.circle(img1, (blackline[i][j][1],blackline[i][j][0]), 1, (255, 0, 0), thickness=-1)
                if big2 < dis2:
                    big2 = dis2
                two+=1
    # 왼쪽 오른쪽 각각 제일 큰 거리값으로 나눠서 0~1 사이 만들어줌
    for i in range(len(blackline)):
        for j in range(len(blackline[i])):
            if leftright[i][j][0]==0:
                leftright[i][j][1] = leftright[i][j][1]/big1
            if leftright[i][j][0]==1:
                leftright[i][j][1] = leftright[i][j][1]/big2

def dis_re(): # 가장 안쪽이 0이 되지 않도록 0.3 더하고 값해줌
    for i in range(len(all_neardis)):
        for j in range(len(all_neardis[i])):
            all_neardis[i][j]+=0.3
            all_neardis[i][j]/=1.3

def matrixconvert():  #주요 계산
    #dis_re()
    for i in range(len(blackline)): # 선의 갯수만큼
        if (i >=downupmouse_num):
            print("잔주름")
        for j in range(len(blackline[i])): # 모든 점에서
            # 주름 중심선으로 향하는 벡터
            vectory = -(all_neardispoint[i][j][0] - blackline[i][j][0])
            vectorx = -(all_neardispoint[i][j][1] - blackline[i][j][1])
            vectorz = 0
            if abs(mousestr[i][0] - mouseend[i][0]) > abs(mousestr[i][1] - mouseend[i][1]):  # x 축 변화량 크다 위아래 선
                if blackline[i][j][0] < mousestr[i][0] or blackline[i][j][0] > mouseend[i][0]:
                    vectory = -(all_neardispoint[i][j][0] - blackline[i][j][0])
                    vectorx = -(all_neardispoint[i][j][1] - blackline[i][j][1])
                    vectorz = 0
                else:
                    vectory = 0
                    vectorx = -(all_neardispoint[i][j][1] - blackline[i][j][1])
                    vectorz = 0
            else: # y 축 변화량 크다 좌우 선
                #print(pensize)
                if blackline[i][j][1] < mousestr[i][1] or blackline[i][j][1] > mouseend[i][1]:
                    vectory = -(all_neardispoint[i][j][0] - blackline[i][j][0])
                    vectorx = -(all_neardispoint[i][j][1] - blackline[i][j][1])
                    vectorz = 0
                else:
                    vectory = -(all_neardispoint[i][j][0] - blackline[i][j][0])
                    vectorx = 0
                    vectorz = 0

            # 벡터의 길이 (단위벡터 만들때 쓸려고)
            unit = math.sqrt((vectorx * vectorx) + ((vectory * vectory)) + ((vectorz * vectorz)))

            # 단위벡터 만듬
            if unit == 0:
                unitx = vectorx
                unity = vectory
            else:
                unitx = (vectorx / unit)
                unity = (vectory / unit)
            unitz = 0

            # 그냥 normal 값을 단위벡터 다시 해준거
            unit2 = math.sqrt((normal_x1[blackline[i][j][0] * w1 + blackline[i][j][1]] * normal_x1[blackline[i][j][0] * w1 + blackline[i][j][1]]) + ((
                        normal_y1[blackline[i][j][0] * w1 + blackline[i][j][1]] * normal_y1[blackline[i][j][0] * w1 + blackline[i][j][1]])) + ((
                        normal_z1[blackline[i][j][0] * w1 + blackline[i][j][1]] * normal_z1[blackline[i][j][0] * w1 + blackline[i][j][1]])))
            unit2x = normal_x1[blackline[i][j][0] * w1 + blackline[i][j][1]] / unit2
            unit2y = normal_y1[blackline[i][j][0] * w1 + blackline[i][j][1]] / unit2
            unit2z = normal_z1[blackline[i][j][0] * w1 + blackline[i][j][1]]

            # 주름 연하게 만들고 싶으면 아래 주석처리 X
            # 잔주름 용
            if (i >=downupmouse_num):
                unitx = unitx * (0.6) + 0 * (1 - 0.6)
                unity = unity * (0.6) + 0 * (1 - 0.6)
                unitz = unitz * (0.6) + 1 * (1 - 0.6)
            # 연하게 용
            elif (linestren[i] == 1):
                unitx = unitx * (0.4) + 0 * (1 - 0.4)
                unity = unity * (0.4) + 0 * (1 - 0.4)
                unitz = unitz * (0.4) + 1 * (1 - 0.4)

            # 뾰족하게 만들어주는 식
            unitx = unitx * ((leftright[i][j][1])) + unit2x * (1 - (leftright[i][j][1]))
            unity = unity * ((leftright[i][j][1])) + unit2y * (1 - (leftright[i][j][1]))
            unitz = unitz * ((leftright[i][j][1])) + 1 * (1 - (leftright[i][j][1]))

            # 최종 normal 값 변경
            normal_x1[blackline[i][j][0] * w1 + blackline[i][j][1]] = normal_x1[blackline[i][j][0] * w1 + blackline[i][j][1]] * all_neardis[i][j] + unitx * (1 - all_neardis[i][j])
            normal_y1[blackline[i][j][0] * w1 + blackline[i][j][1]] = normal_y1[blackline[i][j][0] * w1 + blackline[i][j][1]] * all_neardis[i][j] + unity * (1 - all_neardis[i][j])
            normal_z1[blackline[i][j][0] * w1 + blackline[i][j][1]] = unit2z * all_neardis[i][j] + unitz * (1 - all_neardis[i][j])

    # 결과 이미지에 넣기
    for i in range(h1):
        for j in range(w1):
            # 범위 넘었을때
            if(normal_x1[i * w1 + j]>1 or normal_x1[i * w1 + j]<-1 or normal_y1[i * w1 + j]>1 or normal_y1[i * w1 + j]<-1 or normal_z1[i * w1 + j]>1 or normal_z1[i * w1 + j]<-1):
                print("주서봡")
            # 노말 값에서 컬러값으로 바꾸는 과정
            img2[i, j][2] = (((normal_x1[i * w1 + j])+1)/2)*255
            img2[i, j][1] = (((normal_y1[i * w1 + j])+1)/2)*255
    cv2.imshow('img2', img2)

def colorchange():
    for i in range(len(endpoint)): # 선의 갯수
        color_weight1.append([])
        color_weight2.append([])
        color_weight_max = 0
        color_weight_min = 10000000
        color_w = 0
        # 가중치 첫번째 구하는 방법
        # 주름의 시작점 끝점과의 가중치 구하는 방법
        for j in range(len(blackline[i])): # 전체 갯수만큼
            # 전체점의 시작점과의 거리
            cal_start = math.sqrt((findstarttwopoint[i][1] - blackline[i][j][0]) * (findstarttwopoint[i][1] - blackline[i][j][0]) +
                    (findstarttwopoint[i][0] - blackline[i][j][1]) * (findstarttwopoint[i][0] - blackline[i][j][1]))
            # 전체점의 끝점과의 거리
            cal_final = math.sqrt((findendtwopoint[i][1] - blackline[i][j][0]) * (findendtwopoint[i][1] - blackline[i][j][0]) +
                    (findendtwopoint[i][0] - blackline[i][j][1]) * (findendtwopoint[i][0] - blackline[i][j][1]))
            # 거리가 어디가 더 가까운가?
            # 거리가 더 가까운 쪽으로 가중치 주기
            if cal_start < cal_final:
                color_w = cal_start
            else :
                color_w = cal_final
            # 가중치 min, max 구하는거
            if color_w > color_weight_max:
                color_weight_max = color_w
            if color_w < color_weight_min:
                color_weight_min = color_w
            color_weight1[i].append(color_w)
        # 0~1 사이로 만들기
        for j in range(len(blackline[i])):
            color_weight1[i][j] = (color_weight1[i][j] -color_weight_min)/(color_weight_max-color_weight_min)
        # 가중치 두번째 구하는 방법
        # 주름 중심선의 중심과의 거리 가중치 구하는 방법
        color_weight_max = 0
        color_weight_min = 10000000
        for j in range(len(blackline[i])):
            color_w = math.sqrt((findmiddletwopoint[i][1] - blackline[i][j][0]) * (findmiddletwopoint[i][1] - blackline[i][j][0]) +
                (findmiddletwopoint[i][0] - blackline[i][j][1]) * (findmiddletwopoint[i][0] - blackline[i][j][1]))
            if color_w > color_weight_max:
                color_weight_max = color_w
            if color_w < color_weight_min:
                color_weight_min = color_w
            color_weight2[i].append(color_w)
        for j in range(len(blackline[i])):
            color_weight2[i][j] = (color_weight2[i][j]-color_weight_min)/(color_weight_max-color_weight_min)

    # 최종 가중치 값들 계산
    # 가중치 종류 1. 거리값 2. 주름 양쪽 끝점 가중치 값 3. 주름 중심부로부터의 거리값
    for i in range(len(blackline)):
        for j in range(len(blackline[i])):
            weight = (((1 - color_weight2[i][j]) * color_weight1[i][j] * (1 - all_neardis[i][j])) * color_deep)
            if (i >= downupmouse_num):
                weight = weight * 0.7
            colorx[blackline[i][j][0] * w1 + blackline[i][j][1]] = colorx[blackline[i][j][0] * w1 + blackline[i][j][1]] - weight
            colory[blackline[i][j][0] * w1 + blackline[i][j][1]] = colory[blackline[i][j][0] * w1 + blackline[i][j][1]] - weight
            colorz[blackline[i][j][0] * w1 + blackline[i][j][1]] = colorz[blackline[i][j][0] * w1 + blackline[i][j][1]] - weight

    # 이미지 계산
    for i in range(h1):
        for j in range(w1):
            imgcolor[i, j][2] = colorx[i * w1 + j]
            imgcolor[i, j][1] = colory[i * w1 + j]
            imgcolor[i, j][0] = colorz[i * w1 + j]

    cv2.imshow('colorimg', imgcolor)
    cv2.imwrite('imgsave/facecolor.png', imgcolor)

def onChange(x):
    pass

cv2.namedWindow("img1")
cv2.createTrackbar('age', 'img1', 0, 100, onChange)
cv2.createTrackbar('line', 'img1', 0, 1, onChange)
cv2.createTrackbar('color_deep', 'img1', 0, 100, onChange)
on_mouse.count=0
colorextraction.count1=0
colorextraction3.count2=0
colorextraction.check=0
on_mouse.startpointx=0
on_mouse.startpointy=0
find_last_two_point.startx = 0
find_last_two_point.starty = 0
find_last_two_point.endx = 0
find_last_two_point.endy = 0

while(True):
    age = cv2.getTrackbarPos('age', 'img1')
    color_deep = cv2.getTrackbarPos('color_deep', 'img1')
    line_strength = cv2.getTrackbarPos('line', 'img1')
    cv2.setMouseCallback('img1', on_mouse, img1)
    cv2.imshow('img1', img1)
    #cv2.imshow('img3', img3)
    #cv2.imshow('img4', img4)
    #cv2.imshow('img5', img5)
    if cv2.waitKey(20) & 0xFF == 0x1B:
        print(blackline)
        break

cv2.destroyAllWindows()