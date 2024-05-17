from ninja import Router
from .models import User, UserLikePaper
from .schemas import RegisterIn, LoginIn
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from gpt_simplify.models import Paper

user_authentication_api = Router()

@user_authentication_api.post("/register/")
def auth_register(request, payload: RegisterIn):
    if User.objects.filter(username=payload.username).exists():
        return {"msg": "Username already exists"}
    user = User.objects.create_user(username=payload.username, password=payload.password)
    return {"msg": "User created successfully", "username": user.username, "pwd": user.password}

@user_authentication_api.post("/login/")
def auth_login(request: HttpRequest, response: HttpResponse, payload: LoginIn): #这样用payload参数代表request body
    print(f"username: {payload.username}, password: {payload.password}")
    # authenticate()自动调用create_user()时同样的哈希计算
    user = authenticate(request, username=payload.username, password=payload.password) #就是检查用户名对应的口令
    print(user)
    print(type(user))
    if user is not None:
        login(request, user)
        response.set_cookie("cookie", "delicious") #浏览器还是没有cookie !!!(前端需要设置axios.defaults.withCredentials = true;)
        return {"msg": "Login successful", "username": user.username}
    else:
        return {"msg": "Invalid credentials"}
    
@user_authentication_api.get("/logout/")
def auth_logout(request, response: HttpResponse):
    logout(request) #把login()做的事情抵消了,session表删掉这个用户的session,删掉client的sessionid的cookie
    response.delete_cookie('cookie') #然后前端浏览器真的把这个cookie删了
    return {"msg": "Logout successfully"}


@user_authentication_api.post("/like/")
@login_required
def user_like_paper(request, paper_id: str):
    # 点击按钮收藏，再点取消
    # 如果已经收藏了，那就从数据库里删除
    existing_record = UserLikePaper.objects.filter(user_id=request.user.id, paper_id=paper_id).first()
    if existing_record:
        existing_record.delete()
    else:
        print(request.user.id)
        print(paper_id)
        # create参数严格要和数据库里的一样，和model定义的一样没用，按数据库的字段名为准
        UserLikePaper.objects.create(user_id_id=request.user.id, paper_id_id=paper_id)

@user_authentication_api.get("/likelist/")
@login_required
def user_like_list(request):
    liked_papers_id = UserLikePaper.objects.filter(user_id=request.user.id).values_list('paper_id', flat=True)
    print(liked_papers_id)
    # !!! __in查询
    liked_papers = Paper.objects.filter(paper_id__in=liked_papers_id)
    print(liked_papers)

    return_list = []
    for liked_paper in liked_papers:
        cur_paper = {}
        cur_paper["Paper_ID"] = liked_paper.paper_id
        cur_paper["Title_En"] = liked_paper.title_en
        cur_paper["Title_Ja"] = liked_paper.title_ja
        cur_paper["Authors"] = liked_paper.author
        cur_paper["Categories"] = liked_paper.categories
        cur_paper["Published"] = liked_paper.published
        cur_paper["Content_En"] = liked_paper.content_en
        cur_paper["Pdf_url"] = liked_paper.pdf_url
        return_list.append(cur_paper)
    return return_list

@user_authentication_api.get("/likelist_cnt/")
@login_required
def user_likedlist_cnt(request):
    return UserLikePaper.objects.filter(user_id=request.user.id).count()

